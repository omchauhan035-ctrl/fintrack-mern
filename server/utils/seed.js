require('dotenv').config();
const mongoose = require('mongoose');
const User = require('../models/User');
const Transaction = require('../models/Transaction');
const Category = require('../models/Category');
const Budget = require('../models/Budget');
const SavingsGoal = require('../models/SavingsGoal');
const GoalContribution = require('../models/GoalContribution');

const connectDB = require('../config/db');

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

const seedUsersData = [
  {
    name: 'Rahul Sharma',
    email: 'demo@fintrack.com',
    password: 'demo123456',
    role: 'Senior Tech Lead',
    currency: 'INR',
    theme: 'light',
    monthlySalary: 12000000, // ₹1,20,000
    freelanceBonus: 3500000,  // ₹35,000
    budgets: [
      { category: 'Food & Dining', amountMinor: 1800000 },
      { category: 'Transportation', amountMinor: 600000 },
      { category: 'Shopping', amountMinor: 1200000 },
      { category: 'Bills & Utilities', amountMinor: 800000 },
      { category: 'Entertainment', amountMinor: 500000 },
    ],
    goals: [
      {
        title: 'Emergency Reserve Fund',
        targetAmountMinor: 50000000, // ₹5,00,000
        currentAmountMinor: 32000000, // ₹3,20,000
        color: '#10b981',
        monthsAhead: 12,
      },
      {
        title: 'MacBook Pro M3 Max',
        targetAmountMinor: 25000000, // ₹2,50,000
        currentAmountMinor: 19000000, // ₹1,90,000
        color: '#6366f1',
        monthsAhead: 3,
      },
      {
        title: 'Japan Autumn Trip',
        targetAmountMinor: 35000000, // ₹3,50,000
        currentAmountMinor: 14000000, // ₹1,40,000
        color: '#ec4899',
        monthsAhead: 9,
      },
    ],
  },
  {
    name: 'Priya Patel',
    email: 'priya@fintrack.com',
    password: 'priya123456',
    role: 'Staff Product Designer',
    currency: 'INR',
    theme: 'dark',
    monthlySalary: 9500000, // ₹95,000
    freelanceBonus: 2800000, // ₹28,000
    budgets: [
      { category: 'Food & Dining', amountMinor: 1400000 },
      { category: 'Shopping', amountMinor: 1500000 },
      { category: 'Entertainment', amountMinor: 600000 },
      { category: 'Bills & Utilities', amountMinor: 700000 },
      { category: 'Education', amountMinor: 400000 },
    ],
    goals: [
      {
        title: 'Home Studio & Ergonomic Desk',
        targetAmountMinor: 15000000, // ₹1,50,000
        currentAmountMinor: 11000000,
        color: '#8b5cf6',
        monthsAhead: 4,
      },
      {
        title: 'Electric Vehicle Scooter',
        targetAmountMinor: 14000000, // ₹1,40,000
        currentAmountMinor: 8500000,
        color: '#06b6d4',
        monthsAhead: 6,
      },
      {
        title: 'Design Masterclass & Conference',
        targetAmountMinor: 8000000, // ₹80,000
        currentAmountMinor: 8000000, // 100% completed
        color: '#22c55e',
        monthsAhead: 1,
      },
    ],
  },
  {
    name: 'Alex Johnson',
    email: 'alex@fintrack.com',
    password: 'alex123456',
    role: 'E-commerce Entrepreneur',
    currency: 'INR',
    theme: 'light',
    monthlySalary: 18000000, // ₹1,80,000
    freelanceBonus: 6000000,  // ₹60,000
    budgets: [
      { category: 'Transportation', amountMinor: 1500000 },
      { category: 'Food & Dining', amountMinor: 2500000 },
      { category: 'Shopping', amountMinor: 2000000 },
      { category: 'Bills & Utilities', amountMinor: 1200000 },
      { category: 'Other', amountMinor: 1000000 },
    ],
    goals: [
      {
        title: 'Warehouse Expansion',
        targetAmountMinor: 120000000, // ₹12,00,000
        currentAmountMinor: 78000000, // ₹7,80,000
        color: '#f59e0b',
        monthsAhead: 14,
      },
      {
        title: 'Commercial Property Deposit',
        targetAmountMinor: 200000000, // ₹20,00,000
        currentAmountMinor: 115000000,
        color: '#3b82f6',
        monthsAhead: 20,
      },
    ],
  },
];

const seed = async () => {
  try {
    await connectDB();
    console.log('Cleaning up existing mock users...');

    for (const uData of seedUsersData) {
      const existing = await User.findOne({ email: uData.email });
      if (existing) {
        await Transaction.deleteMany({ userId: existing._id });
        await Category.deleteMany({ userId: existing._id });
        await Budget.deleteMany({ userId: existing._id });
        await SavingsGoal.deleteMany({ userId: existing._id });
        await GoalContribution.deleteMany({ userId: existing._id });
        await User.deleteOne({ _id: existing._id });
      }
    }

    console.log('Seeding fresh demo users and transactions...');
    const now = new Date();

    for (const uData of seedUsersData) {
      // 1. Create User
      const user = await User.create({
        name: uData.name,
        email: uData.email,
        passwordHash: uData.password,
        preferredCurrency: uData.currency,
        theme: uData.theme,
      });

      // 2. Create Categories
      const categories = defaultCategories.map((cat) => ({
        ...cat,
        userId: user._id,
        isDefault: true,
      }));
      await Category.insertMany(categories);

      // 3. Create Multi-Month Transactions (Last 6 Months)
      const transactions = [];

      for (let m = 5; m >= 0; m--) {
        const monthDate = new Date(now.getFullYear(), now.getMonth() - m, 1);
        const monthEnd = new Date(now.getFullYear(), now.getMonth() - m + 1, 0);
        const daysInMonth = monthEnd.getDate();

        // Main Monthly Income
        transactions.push({
          userId: user._id,
          title: 'Primary Monthly Compensation',
          amountMinor: uData.monthlySalary,
          type: 'income',
          category: 'Salary',
          date: new Date(monthDate.getFullYear(), monthDate.getMonth(), 1),
          paymentMethod: 'bank_transfer',
          notes: 'Direct salary deposit',
        });

        // Freelance or Consulting Income
        if (m % 2 === 0 || m === 1) {
          transactions.push({
            userId: user._id,
            title: 'Consulting Retainer & Bonus',
            amountMinor: uData.freelanceBonus + Math.floor(Math.random() * 500000),
            type: 'income',
            category: 'Freelance',
            date: new Date(monthDate.getFullYear(), monthDate.getMonth(), 14),
            paymentMethod: 'bank_transfer',
            notes: 'Client milestone bonus',
          });
        }

        // Investment dividend
        if (m % 3 === 0) {
          transactions.push({
            userId: user._id,
            title: 'Mutual Fund Dividend & Interest',
            amountMinor: 850000 + Math.floor(Math.random() * 400000),
            type: 'income',
            category: 'Investments',
            date: new Date(monthDate.getFullYear(), monthDate.getMonth(), 22),
            paymentMethod: 'bank_transfer',
            notes: 'Quarterly payout',
          });
        }

        // Variable Expense Distribution
        const expenseTemplates = [
          { title: 'Supermarket & Weekly Grocery', category: 'Food & Dining', min: 250000, max: 550000, method: 'upi' },
          { title: 'Cafe & Weekend Dining', category: 'Food & Dining', min: 120000, max: 350000, method: 'credit_card' },
          { title: 'Fuel & Cab Commute', category: 'Transportation', min: 80000, max: 200000, method: 'upi' },
          { title: 'Electricity & Water Bill', category: 'Bills & Utilities', min: 180000, max: 320000, method: 'bank_transfer' },
          { title: 'High-speed Fiber Broadband', category: 'Bills & Utilities', min: 110000, max: 150000, method: 'bank_transfer' },
          { title: 'Mobile Postpaid Bill', category: 'Bills & Utilities', min: 69900, max: 99900, method: 'upi' },
          { title: 'Clothing & Lifestyle Purchase', category: 'Shopping', min: 200000, max: 700000, method: 'credit_card' },
          { title: 'Streaming & Cloud Services', category: 'Entertainment', min: 49900, max: 149900, method: 'credit_card' },
          { title: 'Fitness Gym & Supplements', category: 'Healthcare', min: 150000, max: 350000, method: 'upi' },
          { title: 'Books & Skill Development', category: 'Education', min: 60000, max: 220000, method: 'credit_card' },
          { title: 'Home Maintenance & Miscellaneous', category: 'Other', min: 50000, max: 180000, method: 'upi' },
        ];

        expenseTemplates.forEach((tpl) => {
          const day = Math.floor(Math.random() * (daysInMonth - 2)) + 2;
          transactions.push({
            userId: user._id,
            title: tpl.title,
            amountMinor: tpl.min + Math.floor(Math.random() * (tpl.max - tpl.min)),
            type: 'expense',
            category: tpl.category,
            date: new Date(monthDate.getFullYear(), monthDate.getMonth(), day),
            paymentMethod: tpl.method,
            notes: '',
          });
        });
      }

      await Transaction.insertMany(transactions);

      // 4. Create Active Monthly Budgets
      const currentMonthStart = new Date(now.getFullYear(), now.getMonth(), 1);
      const currentMonthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59);

      await Budget.insertMany(
        uData.budgets.map((b) => ({
          userId: user._id,
          category: b.category,
          amountMinor: b.amountMinor,
          period: 'monthly',
          startDate: currentMonthStart,
          endDate: currentMonthEnd,
        }))
      );

      // 5. Create Savings Goals
      for (const g of uData.goals) {
        const targetDate = new Date(now);
        targetDate.setMonth(targetDate.getMonth() + g.monthsAhead);

        const goalDoc = await SavingsGoal.create({
          userId: user._id,
          title: g.title,
          targetAmountMinor: g.targetAmountMinor,
          currentAmountMinor: g.currentAmountMinor,
          targetDate,
          status: g.currentAmountMinor >= g.targetAmountMinor ? 'completed' : 'active',
          color: g.color,
          icon: 'target',
        });

        // Add 2 realistic contribution ledger entries
        if (g.currentAmountMinor > 0) {
          const half = Math.round(g.currentAmountMinor / 2);
          await GoalContribution.create([
            {
              userId: user._id,
              goalId: goalDoc._id,
              amountMinor: half,
              type: 'contribution',
              notes: 'Initial monthly deposit',
              createdAt: new Date(now.getFullYear(), now.getMonth() - 1, 5),
            },
            {
              userId: user._id,
              goalId: goalDoc._id,
              amountMinor: g.currentAmountMinor - half,
              type: 'contribution',
              notes: 'Bonus contribution',
              createdAt: new Date(now.getFullYear(), now.getMonth(), 2),
            },
          ]);
        }
      }

      console.log(`✅ Seeded profile for ${uData.name} (${uData.email}) with ${transactions.length} transactions, ${uData.budgets.length} budgets, and ${uData.goals.length} goals.`);
    }

    console.log('\n===========================================');
    console.log('🎉 SEED COMPLETED SUCCESSFULLY!');
    console.log('Available Demo Accounts:');
    seedUsersData.forEach((u) => {
      console.log(`- ${u.name.padEnd(16)} | Email: ${u.email.padEnd(20)} | Password: ${u.password}`);
    });
    console.log('===========================================\n');

    process.exit(0);
  } catch (error) {
    console.error('Seed error:', error);
    process.exit(1);
  }
};

seed();
