const jwt = require('jsonwebtoken');
const User = require('../models/User');
const Category = require('../models/Category');

const generateToken = (userId) => {
  return jwt.sign({ userId }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '7d',
  });
};

const setCookieOptions = () => ({
  httpOnly: true,
  secure: process.env.COOKIE_SECURE === 'true',
  sameSite: process.env.COOKIE_SAMESITE || 'lax',
  maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
  path: '/',
});

// Default categories to seed for new users
const defaultCategories = [
  { name: 'Salary', type: 'income', color: '#22c55e', icon: 'briefcase' },
  { name: 'Freelance', type: 'income', color: '#3b82f6', icon: 'laptop' },
  { name: 'Investments', type: 'income', color: '#8b5cf6', icon: 'trending-up' },
  { name: 'Other Income', type: 'income', color: '#06b6d4', icon: 'plus-circle' },
  { name: 'Food & Dining', type: 'expense', color: '#f97316', icon: 'utensils' },
  { name: 'Transportation', type: 'expense', color: '#eab308', icon: 'car' },
  { name: 'Shopping', type: 'expense', color: '#ec4899', icon: 'shopping-bag' },
  { name: 'Bills & Utilities', type: 'expense', color: '#ef4444', icon: 'zap' },
  { name: 'Healthcare', type: 'expense', color: '#14b8a6', icon: 'heart' },
  { name: 'Entertainment', type: 'expense', color: '#a855f7', icon: 'film' },
  { name: 'Education', type: 'expense', color: '#6366f1', icon: 'book-open' },
  { name: 'Other', type: 'both', color: '#64748b', icon: 'tag' },
];

// @desc    Register a new user
// @route   POST /api/auth/register
exports.register = async (req, res, next) => {
  try {
    let { name, email, password } = req.body;
    if (email) email = email.trim().toLowerCase();

    // Check if user exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).json({
        success: false,
        message: 'An account with this email already exists.',
      });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      passwordHash: password,
    });

    // Seed default categories for the new user
    const categories = defaultCategories.map((cat) => ({
      ...cat,
      userId: user._id,
      isDefault: true,
    }));
    await Category.insertMany(categories);

    // Generate token and set cookie
    const token = generateToken(user._id);
    res.cookie('token', token, setCookieOptions());

    res.status(201).json({
      success: true,
      data: { user },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Login user
// @route   POST /api/auth/login
exports.login = async (req, res, next) => {
  try {
    let { email, password } = req.body;
    if (email) email = email.trim().toLowerCase();

    // Find user with password
    const user = await User.findOne({ email }).select('+passwordHash');
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Invalid email or password.',
      });
    }

    // Check password
    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({
        success: false,
        message: 'Invalid email or password.',
      });
    }

    // Generate token and set cookie
    const token = generateToken(user._id);
    res.cookie('token', token, setCookieOptions());

    res.json({
      success: true,
      data: { user },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Logout user
// @route   POST /api/auth/logout
exports.logout = async (req, res) => {
  res.cookie('token', '', {
    httpOnly: true,
    expires: new Date(0),
    path: '/',
  });

  res.json({
    success: true,
    message: 'Logged out successfully.',
  });
};

// @desc    Get current user
// @route   GET /api/auth/me
exports.getMe = async (req, res) => {
  res.json({
    success: true,
    data: { user: req.user },
  });
};

// @desc    Update profile
// @route   PATCH /api/auth/profile
exports.updateProfile = async (req, res, next) => {
  try {
    const { name, preferredCurrency, theme } = req.body;
    const updates = {};

    if (name !== undefined) updates.name = name;
    if (preferredCurrency !== undefined) updates.preferredCurrency = preferredCurrency;
    if (theme !== undefined) updates.theme = theme;

    const user = await User.findByIdAndUpdate(req.user._id, updates, {
      new: true,
      runValidators: true,
    });

    res.json({
      success: true,
      data: { user },
    });
  } catch (error) {
    next(error);
  }
};

// @desc    Change password
// @route   PATCH /api/auth/password
exports.changePassword = async (req, res, next) => {
  try {
    const { currentPassword, newPassword } = req.body;

    const user = await User.findById(req.user._id).select('+passwordHash');

    const isMatch = await user.comparePassword(currentPassword);
    if (!isMatch) {
      return res.status(400).json({
        success: false,
        message: 'Current password is incorrect.',
      });
    }

    user.passwordHash = newPassword;
    await user.save();

    // Regenerate token
    const token = generateToken(user._id);
    res.cookie('token', token, setCookieOptions());

    res.json({
      success: true,
      message: 'Password changed successfully.',
    });
  } catch (error) {
    next(error);
  }
};
