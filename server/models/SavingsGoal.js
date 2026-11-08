const mongoose = require('mongoose');

const savingsGoalSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      index: true,
    },
    title: {
      type: String,
      required: [true, 'Goal title is required'],
      trim: true,
      maxlength: [100, 'Title cannot exceed 100 characters'],
    },
    targetAmountMinor: {
      type: Number,
      required: [true, 'Target amount is required'],
      min: [1, 'Target amount must be positive'],
    },
    currentAmountMinor: {
      type: Number,
      default: 0,
      min: [0, 'Current amount cannot be negative'],
    },
    targetDate: {
      type: Date,
      default: null,
    },
    status: {
      type: String,
      enum: ['active', 'completed', 'archived'],
      default: 'active',
    },
    color: {
      type: String,
      default: '#6366f1',
    },
    icon: {
      type: String,
      default: 'target',
    },
  },
  {
    timestamps: true,
  }
);

savingsGoalSchema.index({ userId: 1, status: 1 });

module.exports = mongoose.model('SavingsGoal', savingsGoalSchema);
