const Transaction = require('../models/Transaction');

// @desc    Get dashboard summary
// @route   GET /api/dashboard/summary
exports.getDashboardSummary = async (req, res, next) => {
  try {
    const { startDate, endDate } = req.query;
    const userId = req.user._id;

    const dateFilter = {};
    if (startDate) dateFilter.$gte = new Date(startDate);
    if (endDate) dateFilter.$lte = new Date(endDate);

    const matchStage = { userId };
    if (Object.keys(dateFilter).length > 0) {
      matchStage.date = dateFilter;
    }

    const [summary] = await Transaction.aggregate([
      { $match: matchStage },
      {
        $group: {
          _id: null,
          totalIncome: {
            $sum: {
              $cond: [{ $eq: ['$type', 'income'] }, '$amountMinor', 0],
            },
          },
          totalExpenses: {
            $sum: {
              $cond: [{ $eq: ['$type', 'expense'] }, '$amountMinor', 0],
            },
          },
          transactionCount: { $sum: 1 },
        },
      },
    ]);

    const totalIncome = summary?.totalIncome || 0;
    const totalExpenses = summary?.totalExpenses || 0;
    const balance = totalIncome - totalExpenses;
    const savingsRate = totalIncome > 0
      ? Math.round(((totalIncome - totalExpenses) / totalIncome) * 10000) / 100
      : 0;

    // Recent transactions
    const recentTransactions = await Transaction.find({ userId })
      .sort({ date: -1 })
      .limit(5);

    // Monthly data for chart (last 6 months)
    const sixMonthsAgo = new Date();
    sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 5);
    sixMonthsAgo.setDate(1);
    sixMonthsAgo.setHours(0, 0, 0, 0);

    const monthlyData = await Transaction.aggregate([
      {
        $match: {
          userId,
          date: { $gte: sixMonthsAgo },
        },
      },
      {
        $group: {
          _id: {
            year: { $year: '$date' },
            month: { $month: '$date' },
            type: '$type',
          },
          total: { $sum: '$amountMinor' },
        },
      },
      { $sort: { '_id.year': 1, '_id.month': 1 } },
    ]);

    // Category breakdown for expenses
    const categoryBreakdown = await Transaction.aggregate([
      {
        $match: {
          ...matchStage,
          type: 'expense',
        },
      },
      {
        $group: {
          _id: '$category',
          total: { $sum: '$amountMinor' },
          count: { $sum: 1 },
        },
      },
      { $sort: { total: -1 } },
      { $limit: 8 },
    ]);

    res.json({
      success: true,
      data: {
        totalIncome,
        totalExpenses,
        balance,
        savingsRate,
        transactionCount: summary?.transactionCount || 0,
        recentTransactions,
        monthlyData,
        categoryBreakdown,
      },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get income vs expenses analytics
// @route   GET /api/analytics/income-expenses
exports.getIncomeExpenses = async (req, res, next) => {
  try {
    const { startDate, endDate, months = 12 } = req.query;
    const userId = req.user._id;

    let matchDate;
    if (startDate && endDate) {
      matchDate = { $gte: new Date(startDate), $lte: new Date(endDate) };
    } else {
      const start = new Date();
      start.setMonth(start.getMonth() - parseInt(months) + 1);
      start.setDate(1);
      start.setHours(0, 0, 0, 0);
      matchDate = { $gte: start };
    }

    const data = await Transaction.aggregate([
      {
        $match: {
          userId,
          date: matchDate,
        },
      },
      {
        $group: {
          _id: {
            year: { $year: '$date' },
            month: { $month: '$date' },
            type: '$type',
          },
          total: { $sum: '$amountMinor' },
          count: { $sum: 1 },
        },
      },
      { $sort: { '_id.year': 1, '_id.month': 1 } },
    ]);

    res.json({
      success: true,
      data,
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get category analytics
// @route   GET /api/analytics/categories
exports.getCategoryAnalytics = async (req, res, next) => {
  try {
    const { startDate, endDate, type = 'expense' } = req.query;
    const userId = req.user._id;

    const matchStage = { userId, type };
    if (startDate || endDate) {
      matchStage.date = {};
      if (startDate) matchStage.date.$gte = new Date(startDate);
      if (endDate) matchStage.date.$lte = new Date(endDate);
    }

    const data = await Transaction.aggregate([
      { $match: matchStage },
      {
        $group: {
          _id: '$category',
          total: { $sum: '$amountMinor' },
          count: { $sum: 1 },
          avgAmount: { $avg: '$amountMinor' },
        },
      },
      { $sort: { total: -1 } },
    ]);

    const grandTotal = data.reduce((sum, cat) => sum + cat.total, 0);
    const enriched = data.map((cat) => ({
      ...cat,
      category: cat._id,
      percentage: grandTotal > 0 ? Math.round((cat.total / grandTotal) * 10000) / 100 : 0,
    }));

    res.json({
      success: true,
      data: enriched,
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get savings trends
// @route   GET /api/analytics/trends
exports.getTrends = async (req, res, next) => {
  try {
    const { months = 12 } = req.query;
    const userId = req.user._id;

    const start = new Date();
    start.setMonth(start.getMonth() - parseInt(months) + 1);
    start.setDate(1);
    start.setHours(0, 0, 0, 0);

    const data = await Transaction.aggregate([
      {
        $match: {
          userId,
          date: { $gte: start },
        },
      },
      {
        $group: {
          _id: {
            year: { $year: '$date' },
            month: { $month: '$date' },
          },
          income: {
            $sum: {
              $cond: [{ $eq: ['$type', 'income'] }, '$amountMinor', 0],
            },
          },
          expenses: {
            $sum: {
              $cond: [{ $eq: ['$type', 'expense'] }, '$amountMinor', 0],
            },
          },
        },
      },
      { $sort: { '_id.year': 1, '_id.month': 1 } },
      {
        $project: {
          year: '$_id.year',
          month: '$_id.month',
          income: 1,
          expenses: 1,
          savings: { $subtract: ['$income', '$expenses'] },
          savingsRate: {
            $cond: [
              { $gt: ['$income', 0] },
              {
                $round: [
                  { $multiply: [{ $divide: [{ $subtract: ['$income', '$expenses'] }, '$income'] }, 100] },
                  2,
                ],
              },
              0,
            ],
          },
        },
      },
    ]);

    res.json({
      success: true,
      data,
    });
  } catch (error) {
    next(error);
  }
};
