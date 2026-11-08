const Budget = require('../models/Budget');
const Transaction = require('../models/Transaction');

// @desc    Get all budgets with spending
// @route   GET /api/budgets
exports.getBudgets = async (req, res, next) => {
  try {
    const userId = req.user._id;
    const budgets = await Budget.find({ userId }).sort({ startDate: -1 });

    // Calculate actual spending for each budget
    const budgetsWithSpending = await Promise.all(
      budgets.map(async (budget) => {
        const spent = await Transaction.aggregate([
          {
            $match: {
              userId,
              type: 'expense',
              category: budget.category,
              date: {
                $gte: budget.startDate,
                $lte: budget.endDate,
              },
            },
          },
          {
            $group: {
              _id: null,
              total: { $sum: '$amountMinor' },
              count: { $sum: 1 },
            },
          },
        ]);

        const spentAmount = spent[0]?.total || 0;
        const remaining = budget.amountMinor - spentAmount;
        const percentage = budget.amountMinor > 0
          ? Math.round((spentAmount / budget.amountMinor) * 10000) / 100
          : 0;

        return {
          ...budget.toObject(),
          spentAmount,
          remaining,
          percentage,
          status: percentage >= 100 ? 'exceeded' : percentage >= 80 ? 'warning' : 'normal',
        };
      })
    );

    res.json({
      success: true,
      data: { budgets: budgetsWithSpending },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Create budget
// @route   POST /api/budgets
exports.createBudget = async (req, res, next) => {
  try {
    const { category, amount, period, startDate, endDate } = req.body;
    const userId = req.user._id;

    // Check for overlapping budget
    const existing = await Budget.findOne({
      userId,
      category,
      $or: [
        {
          startDate: { $lte: new Date(endDate) },
          endDate: { $gte: new Date(startDate) },
        },
      ],
    });

    if (existing) {
      return res.status(409).json({
        success: false,
        message: 'A budget for this category already exists in the selected period.',
      });
    }

    const budget = await Budget.create({
      userId,
      category,
      amountMinor: Math.round(amount * 100),
      period,
      startDate: new Date(startDate),
      endDate: new Date(endDate),
    });

    res.status(201).json({
      success: true,
      data: { budget },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Update budget
// @route   PATCH /api/budgets/:id
exports.updateBudget = async (req, res, next) => {
  try {
    const { amount, category, period, startDate, endDate } = req.body;
    const updates = {};

    if (amount !== undefined) updates.amountMinor = Math.round(amount * 100);
    if (category !== undefined) updates.category = category;
    if (period !== undefined) updates.period = period;
    if (startDate !== undefined) updates.startDate = new Date(startDate);
    if (endDate !== undefined) updates.endDate = new Date(endDate);

    const budget = await Budget.findOneAndUpdate(
      { _id: req.params.id, userId: req.user._id },
      updates,
      { new: true, runValidators: true }
    );

    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found.',
      });
    }

    res.json({
      success: true,
      data: { budget },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Delete budget
// @route   DELETE /api/budgets/:id
exports.deleteBudget = async (req, res, next) => {
  try {
    const budget = await Budget.findOneAndDelete({
      _id: req.params.id,
      userId: req.user._id,
    });

    if (!budget) {
      return res.status(404).json({
        success: false,
        message: 'Budget not found.',
      });
    }

    res.json({
      success: true,
      message: 'Budget deleted successfully.',
    });
  } catch (error) {
    next(error);
  }
};
