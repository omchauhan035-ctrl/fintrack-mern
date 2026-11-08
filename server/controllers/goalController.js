const SavingsGoal = require('../models/SavingsGoal');
const GoalContribution = require('../models/GoalContribution');

// @desc    Get all savings goals
// @route   GET /api/goals
exports.getGoals = async (req, res, next) => {
  try {
    const { status } = req.query;
    const query = { userId: req.user._id };
    if (status) query.status = status;

    const goals = await SavingsGoal.find(query).sort({ createdAt: -1 });

    // Get contributions for each goal
    const goalsWithDetails = await Promise.all(
      goals.map(async (goal) => {
        const contributions = await GoalContribution.find({ goalId: goal._id })
          .sort({ date: -1 })
          .limit(5);

        const percentage = goal.targetAmountMinor > 0
          ? Math.round((goal.currentAmountMinor / goal.targetAmountMinor) * 10000) / 100
          : 0;

        const remaining = goal.targetAmountMinor - goal.currentAmountMinor;

        return {
          ...goal.toObject(),
          percentage,
          remaining,
          recentContributions: contributions,
        };
      })
    );

    res.json({
      success: true,
      data: { goals: goalsWithDetails },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Create savings goal
// @route   POST /api/goals
exports.createGoal = async (req, res, next) => {
  try {
    const { title, targetAmount, targetDate, color, icon } = req.body;

    const goal = await SavingsGoal.create({
      userId: req.user._id,
      title,
      targetAmountMinor: Math.round(targetAmount * 100),
      targetDate: targetDate ? new Date(targetDate) : null,
      color: color || '#6366f1',
      icon: icon || 'target',
    });

    res.status(201).json({
      success: true,
      data: { goal },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Update savings goal
// @route   PATCH /api/goals/:id
exports.updateGoal = async (req, res, next) => {
  try {
    const { title, targetAmount, targetDate, status, color, icon } = req.body;
    const updates = {};

    if (title !== undefined) updates.title = title;
    if (targetAmount !== undefined) updates.targetAmountMinor = Math.round(targetAmount * 100);
    if (targetDate !== undefined) updates.targetDate = targetDate ? new Date(targetDate) : null;
    if (status !== undefined) updates.status = status;
    if (color !== undefined) updates.color = color;
    if (icon !== undefined) updates.icon = icon;

    const goal = await SavingsGoal.findOneAndUpdate(
      { _id: req.params.id, userId: req.user._id },
      updates,
      { new: true, runValidators: true }
    );

    if (!goal) {
      return res.status(404).json({
        success: false,
        message: 'Savings goal not found.',
      });
    }

    res.json({
      success: true,
      data: { goal },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Delete savings goal
// @route   DELETE /api/goals/:id
exports.deleteGoal = async (req, res, next) => {
  try {
    const goal = await SavingsGoal.findOneAndDelete({
      _id: req.params.id,
      userId: req.user._id,
    });

    if (!goal) {
      return res.status(404).json({
        success: false,
        message: 'Savings goal not found.',
      });
    }

    // Also delete all contributions for this goal
    await GoalContribution.deleteMany({ goalId: goal._id });

    res.json({
      success: true,
      message: 'Savings goal deleted successfully.',
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Add contribution to goal
// @route   POST /api/goals/:id/contributions
exports.addContribution = async (req, res, next) => {
  try {
    const { amount, notes } = req.body;
    const amountMinor = Math.round(amount * 100);

    const goal = await SavingsGoal.findOne({
      _id: req.params.id,
      userId: req.user._id,
    });

    if (!goal) {
      return res.status(404).json({
        success: false,
        message: 'Savings goal not found.',
      });
    }

    if (goal.status !== 'active') {
      return res.status(400).json({
        success: false,
        message: 'Cannot add contributions to a non-active goal.',
      });
    }

    // Create contribution record
    const contribution = await GoalContribution.create({
      userId: req.user._id,
      goalId: goal._id,
      amountMinor,
      type: 'contribution',
      notes,
    });

    // Update goal's current amount
    goal.currentAmountMinor += amountMinor;
    if (goal.currentAmountMinor >= goal.targetAmountMinor) {
      goal.status = 'completed';
    }
    await goal.save();

    res.status(201).json({
      success: true,
      data: { contribution, goal },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Withdraw from goal
// @route   POST /api/goals/:id/withdrawals
exports.addWithdrawal = async (req, res, next) => {
  try {
    const { amount, notes } = req.body;
    const amountMinor = Math.round(amount * 100);

    const goal = await SavingsGoal.findOne({
      _id: req.params.id,
      userId: req.user._id,
    });

    if (!goal) {
      return res.status(404).json({
        success: false,
        message: 'Savings goal not found.',
      });
    }

    if (amountMinor > goal.currentAmountMinor) {
      return res.status(400).json({
        success: false,
        message: 'Withdrawal amount exceeds current savings.',
      });
    }

    // Create withdrawal record
    const contribution = await GoalContribution.create({
      userId: req.user._id,
      goalId: goal._id,
      amountMinor,
      type: 'withdrawal',
      notes,
    });

    // Update goal's current amount
    goal.currentAmountMinor -= amountMinor;
    if (goal.status === 'completed' && goal.currentAmountMinor < goal.targetAmountMinor) {
      goal.status = 'active';
    }
    await goal.save();

    res.json({
      success: true,
      data: { contribution, goal },
    });
  } catch (error) {
    next(error);
  }
};
