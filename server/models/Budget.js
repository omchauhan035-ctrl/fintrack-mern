const mongoose = require('mongoose');

const budgetSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      index: true,
    },
    category: {
      type: String,
      required: [true, 'Category is required'],
      trim: true,
    },
    amountMinor: {
      type: Number,
      required: [true, 'Budget amount is required'],
      min: [1, 'Budget amount must be positive'],
    },
    period: {
      type: String,
      required: true,
      enum: ['monthly', 'weekly', 'yearly'],
      default: 'monthly',
    },
    startDate: {
      type: Date,
      required: true,
    },
    endDate: {
      type: Date,
      required: true,
    },
  },
  {
    timestamps: true,
  }
);

// Prevent duplicate budgets for same category in overlapping periods
budgetSchema.index({ userId: 1, category: 1, startDate: 1, endDate: 1 });

module.exports = mongoose.model('Budget', budgetSchema);
