const User = require('../models/User');
const Transaction = require('../models/Transaction');
const Budget = require('../models/Budget');
const SavingsGoal = require('../models/SavingsGoal');
const GoalContribution = require('../models/GoalContribution');
const Category = require('../models/Category');

// @desc    Get system-wide overview statistics
// @route   GET /api/admin/stats
exports.getStats = async (req, res, next) => {
  try {
    const [
      totalUsers,
      activeUsers,
      blockedUsers,
      adminCount,
      totalTransactions,
      totalBudgets,
      totalGoals,
      volumeAggregate,
      recentUsers,
      recentTransactions,
      monthlyTrends,
    ] = await Promise.all([
      User.countDocuments(),
      User.countDocuments({ status: 'active' }),
      User.countDocuments({ status: 'blocked' }),
      User.countDocuments({ role: 'admin' }),
      Transaction.countDocuments(),
      Budget.countDocuments(),
      SavingsGoal.countDocuments(),

      // Aggregate overall platform volume
      Transaction.aggregate([
        {
          $group: {
            _id: '$type',
            totalAmountMinor: { $sum: '$amountMinor' },
            count: { $sum: 1 },
          },
        },
      ]),

      // Recent 5 users
      User.find()
        .sort({ createdAt: -1 })
        .limit(5)
        .select('name email role status createdAt'),

      // Recent 10 transactions
      Transaction.find()
        .sort({ date: -1, createdAt: -1 })
        .limit(10)
        .populate('userId', 'name email'),

      // Last 6 months platform transaction volume
      Transaction.aggregate([
        {
          $match: {
            date: {
              $gte: new Date(new Date().setMonth(new Date().getMonth() - 5, 1)),
            },
          },
        },
        {
          $group: {
            _id: {
              year: { $year: '$date' },
              month: { $month: '$date' },
              type: '$type',
            },
            totalMinor: { $sum: '$amountMinor' },
            count: { $sum: 1 },
          },
        },
        { $sort: { '_id.year': 1, '_id.month': 1 } },
      ]),
    ]);

    let totalIncomeMinor = 0;
    let totalExpenseMinor = 0;
    volumeAggregate.forEach((v) => {
      if (v._id === 'income') totalIncomeMinor = v.totalAmountMinor;
      if (v._id === 'expense') totalExpenseMinor = v.totalAmountMinor;
    });

    res.json({
      success: true,
      data: {
        users: {
          total: totalUsers,
          active: activeUsers,
          blocked: blockedUsers,
          admins: adminCount,
        },
        transactions: {
          total: totalTransactions,
          totalIncomeMinor,
          totalExpenseMinor,
          netFlowMinor: totalIncomeMinor - totalExpenseMinor,
        },
        budgets: {
          total: totalBudgets,
        },
        goals: {
          total: totalGoals,
        },
        recentUsers,
        recentTransactions,
        monthlyTrends,
      },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get all users with search, filter, and pagination
// @route   GET /api/admin/users
exports.getUsers = async (req, res, next) => {
  try {
    const { search, role, status, page = 1, limit = 20 } = req.query;

    const query = {};

    if (search) {
      query.$or = [
        { name: { $regex: search, $options: 'i' } },
        { email: { $regex: search, $options: 'i' } },
      ];
    }

    if (role && role !== 'all') {
      query.role = role;
    }

    if (status && status !== 'all') {
      query.status = status;
    }

    const skip = (parseInt(page) - 1) * parseInt(limit);
    const total = await User.countDocuments(query);

    const users = await User.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    // Calculate quick stats per user (transaction count, total spent)
    const userIds = users.map((u) => u._id);
    const txStats = await Transaction.aggregate([
      { $match: { userId: { $in: userIds } } },
      {
        $group: {
          _id: '$userId',
          txCount: { $sum: 1 },
          totalSpentMinor: {
            $sum: { $cond: [{ $eq: ['$type', 'expense'] }, '$amountMinor', 0] },
          },
          totalIncomeMinor: {
            $sum: { $cond: [{ $eq: ['$type', 'income'] }, '$amountMinor', 0] },
          },
        },
      },
    ]);

    const statsMap = {};
    txStats.forEach((s) => {
      statsMap[s._id.toString()] = s;
    });

    const enhancedUsers = users.map((u) => {
      const uObj = u.toJSON();
      const st = statsMap[u._id.toString()] || {
        txCount: 0,
        totalSpentMinor: 0,
        totalIncomeMinor: 0,
      };
      return {
        ...uObj,
        transactionCount: st.txCount,
        totalSpentMinor: st.totalSpentMinor,
        totalIncomeMinor: st.totalIncomeMinor,
      };
    });

    res.json({
      success: true,
      data: {
        users: enhancedUsers,
        pagination: {
          total,
          page: parseInt(page),
          pages: Math.ceil(total / parseInt(limit)) || 1,
          limit: parseInt(limit),
        },
      },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Update user status (active / blocked)
// @route   PATCH /api/admin/users/:id/status
exports.updateUserStatus = async (req, res, next) => {
  try {
    const { id } = req.params;
    const { status } = req.body;

    if (!['active', 'blocked'].includes(status)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid status. Must be active or blocked.',
      });
    }

    if (id === req.user._id.toString()) {
      return res.status(400).json({
        success: false,
        message: 'You cannot alter your own account status.',
      });
    }

    const user = await User.findByIdAndUpdate(
      id,
      { status },
      { new: true, runValidators: true }
    );

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found.',
      });
    }

    res.json({
      success: true,
      message: `User status updated to ${status}.`,
      data: { user },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Update user role (user / admin)
// @route   PATCH /api/admin/users/:id/role
exports.updateUserRole = async (req, res, next) => {
  try {
    const { id } = req.params;
    const { role } = req.body;

    if (!['user', 'admin'].includes(role)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid role. Must be user or admin.',
      });
    }

    if (id === req.user._id.toString()) {
      return res.status(400).json({
        success: false,
        message: 'You cannot change your own administrative role.',
      });
    }

    const user = await User.findByIdAndUpdate(
      id,
      { role },
      { new: true, runValidators: true }
    );

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found.',
      });
    }

    res.json({
      success: true,
      message: `User role updated to ${role}.`,
      data: { user },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Delete user and cascade delete their data
// @route   DELETE /api/admin/users/:id
exports.deleteUser = async (req, res, next) => {
  try {
    const { id } = req.params;

    if (id === req.user._id.toString()) {
      return res.status(400).json({
        success: false,
        message: 'You cannot delete your own admin account.',
      });
    }

    const user = await User.findById(id);
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found.',
      });
    }

    // Cascade delete user data
    await Promise.all([
      Transaction.deleteMany({ userId: id }),
      Budget.deleteMany({ userId: id }),
      SavingsGoal.deleteMany({ userId: id }),
      GoalContribution.deleteMany({ userId: id }),
      Category.deleteMany({ userId: id }),
      User.findByIdAndDelete(id),
    ]);

    res.json({
      success: true,
      message: `User ${user.name} and all associated records have been removed.`,
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get all transactions across the entire system
// @route   GET /api/admin/transactions
exports.getTransactions = async (req, res, next) => {
  try {
    const { search, type, category, page = 1, limit = 25 } = req.query;

    const query = {};

    if (search) {
      query.$or = [
        { title: { $regex: search, $options: 'i' } },
        { category: { $regex: search, $options: 'i' } },
        { paymentMethod: { $regex: search, $options: 'i' } },
      ];
    }

    if (type && type !== 'all') {
      query.type = type;
    }

    if (category && category !== 'all') {
      query.category = category;
    }

    const skip = (parseInt(page) - 1) * parseInt(limit);
    const total = await Transaction.countDocuments(query);

    const transactions = await Transaction.find(query)
      .sort({ date: -1, createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit))
      .populate('userId', 'name email');

    res.json({
      success: true,
      data: {
        transactions,
        pagination: {
          total,
          page: parseInt(page),
          pages: Math.ceil(total / parseInt(limit)) || 1,
          limit: parseInt(limit),
        },
      },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Delete any transaction
// @route   DELETE /api/admin/transactions/:id
exports.deleteTransaction = async (req, res, next) => {
  try {
    const { id } = req.params;
    const tx = await Transaction.findByIdAndDelete(id);

    if (!tx) {
      return res.status(404).json({
        success: false,
        message: 'Transaction not found.',
      });
    }

    res.json({
      success: true,
      message: 'Transaction removed successfully by administrator.',
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Get all categories across system
// @route   GET /api/admin/categories
exports.getCategories = async (req, res, next) => {
  try {
    const defaultCategories = await Category.find({ isDefault: true }).sort({ name: 1 });
    const customCategoriesCount = await Category.countDocuments({ isDefault: false });

    // Category usage statistics
    const usage = await Transaction.aggregate([
      {
        $group: {
          _id: '$category',
          count: { $sum: 1 },
          totalMinor: { $sum: '$amountMinor' },
        },
      },
      { $sort: { count: -1 } },
    ]);

    res.json({
      success: true,
      data: {
        defaultCategories,
        customCategoriesCount,
        categoryUsage: usage,
      },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Create a new global default category
// @route   POST /api/admin/categories
exports.createDefaultCategory = async (req, res, next) => {
  try {
    const { name, type, color, icon } = req.body;

    if (!name || !type) {
      return res.status(400).json({
        success: false,
        message: 'Category name and type are required.',
      });
    }

    const existing = await Category.findOne({ name, isDefault: true });
    if (existing) {
      return res.status(409).json({
        success: false,
        message: 'A default category with this name already exists.',
      });
    }

    const category = await Category.create({
      userId: null,
      name,
      type,
      color: color || '#6366f1',
      icon: icon || 'tag',
      isDefault: true,
    });

    res.status(201).json({
      success: true,
      message: 'Global default category created successfully.',
      data: { category },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Delete a default category
// @route   DELETE /api/admin/categories/:id
exports.deleteDefaultCategory = async (req, res, next) => {
  try {
    const { id } = req.params;
    const cat = await Category.findByIdAndDelete(id);

    if (!cat) {
      return res.status(404).json({
        success: false,
        message: 'Category not found.',
      });
    }

    res.json({
      success: true,
      message: 'Default category removed successfully.',
    });
  } catch (error) {
    next(error);
  }
};

// @desc    System health metrics
// @route   GET /api/admin/system
exports.getSystemHealth = async (req, res, next) => {
  try {
    const mem = process.memoryUsage();
    const uptimeSec = Math.floor(process.uptime());

    const days = Math.floor(uptimeSec / 86400);
    const hours = Math.floor((uptimeSec % 86400) / 3600);
    const minutes = Math.floor((uptimeSec % 3600) / 60);
    const seconds = uptimeSec % 60;

    const uptimeStr = `${days > 0 ? days + 'd ' : ''}${hours}h ${minutes}m ${seconds}s`;

    res.json({
      success: true,
      data: {
        serverTime: new Date().toISOString(),
        nodeVersion: process.version,
        platform: process.platform,
        uptime: uptimeStr,
        uptimeSeconds: uptimeSec,
        memory: {
          heapUsedMB: (mem.heapUsed / 1024 / 1024).toFixed(2),
          heapTotalMB: (mem.heapTotal / 1024 / 1024).toFixed(2),
          rssMB: (mem.rss / 1024 / 1024).toFixed(2),
        },
        database: {
          status: 'Connected',
          name: 'finance-tracker',
        },
        environment: process.env.NODE_ENV || 'development',
      },
    });
  } catch (error) {
    next(error);
  }
};
