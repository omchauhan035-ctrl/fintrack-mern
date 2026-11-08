require('dotenv').config();
const mongoose = require('mongoose');
const User = require('../models/User');
const Transaction = require('../models/Transaction');
const Budget = require('../models/Budget');
const SavingsGoal = require('../models/SavingsGoal');
const GoalContribution = require('../models/GoalContribution');
const Category = require('../models/Category');
const connectDB = require('../config/db');

const populate = async () => {
  try {
    await connectDB();
    const user = await User.findOne({ email: 'om40@gmail.com' });
    if (!user) {
      console.error('User om40@gmail.com not found!');
      process.exit(1);
    }

    console.log(`Populating financial data for ${user.name} (${user.email})...`);

    // Clean existing transactions, budgets, goals for this user
    await Transaction.deleteMany({ userId: user._id });
    await Budget.deleteMany({ userId: user._id });
    await SavingsGoal.deleteMany({ userId: user._id });
    await GoalContribution.deleteMany({ userId: user._id });

    const now = new Date();
    const transactions = [];

    // Monthly salary & income over the last 6 months
    const monthlySalary = 11000000; // ₹1,10,000 per month

    for (let m = 5; m >= 0; m--) {
      const monthDate = new Date(now.getFullYear(), now.getMonth() - m, 1);
      const monthEnd = new Date(now.getFullYear(), now.getMonth() - m + 1, 0);
      const daysInMonth = monthEnd.getDate();

      // Monthly Salary
      transactions.push({
        userId: user._id,
        title: 'Monthly Engineering Salary',
        amountMinor: monthlySalary,
        type: 'income',
        category: 'Salary',
        date: new Date(monthDate.getFullYear(), monthDate.getMonth(), 1),
        paymentMethod: 'bank_transfer',
        notes: 'Tech Corp monthly salary deposit',
      });

      // Freelance / Side Projects
      if (m % 2 === 0 || m === 1) {
        transactions.push({
          userId: user._id,
          title: 'Full Stack Web App Freelance Project',
          amountMinor: 3200000 + Math.floor(Math.random() * 800000), // ~₹32,000 - ₹40,000
          type: 'income',
          category: 'Freelance',
          date: new Date(monthDate.getFullYear(), monthDate.getMonth(), 12),
          paymentMethod: 'bank_transfer',
          notes: 'Client milestone delivery',
        });
      }

      // Investment Returns
      if (m % 2 === 1) {
        transactions.push({
          userId: user._id,
          title: 'Index Fund Dividends & Returns',
          amountMinor: 650000 + Math.floor(Math.random() * 250000), // ~₹6,500 - ₹9,000
          type: 'income',
          category: 'Investments',
          date: new Date(monthDate.getFullYear(), monthDate.getMonth(), 24),
          paymentMethod: 'bank_transfer',
          notes: 'Quarterly dividend reinvestment',
        });
      }

      // Diverse Realistic Expenses
      const expenseCatalog = [
        { title: 'Supermarket Grocery Run', category: 'Food & Dining', min: 280000, max: 480000, method: 'upi' },
        { title: 'Swiggy / Zomato Food Delivery', category: 'Food & Dining', min: 90000, max: 240000, method: 'upi' },
        { title: 'Weekend Dining & Cafe', category: 'Food & Dining', min: 140000, max: 320000, method: 'credit_card' },
        { title: 'Uber & Auto Rides', category: 'Transportation', min: 60000, max: 150000, method: 'upi' },
        { title: 'Vehicle Fuel Refill', category: 'Transportation', min: 120000, max: 220000, method: 'credit_card' },
        { title: 'Electricity Bill', category: 'Bills & Utilities', min: 160000, max: 280000, method: 'bank_transfer' },
        { title: 'Airtel Broadband Internet', category: 'Bills & Utilities', min: 117900, max: 117900, method: 'bank_transfer' },
        { title: 'Mobile Postpaid Recharge', category: 'Bills & Utilities', min: 79900, max: 99900, method: 'upi' },
        { title: 'Amazon Electronics & Accessories', category: 'Shopping', min: 180000, max: 550000, method: 'credit_card' },
        { title: 'Clothing & Footwear', category: 'Shopping', min: 150000, max: 420000, method: 'credit_card' },
        { title: 'Netflix & Spotify Premium', category: 'Entertainment', min: 84800, max: 84800, method: 'credit_card' },
        { title: 'Cinema Movie Tickets & Snacks', category: 'Entertainment', min: 70000, max: 160000, method: 'upi' },
        { title: 'Gym Membership & Whey Protein', category: 'Healthcare', min: 180000, max: 320000, method: 'upi' },
        { title: 'Udemy / Coursera Tech Courses', category: 'Education', min: 69900, max: 189900, method: 'credit_card' },
      ];

      expenseCatalog.forEach((exp) => {
        const day = Math.floor(Math.random() * (daysInMonth - 3)) + 2;
        transactions.push({
          userId: user._id,
          title: exp.title,
          amountMinor: exp.min + Math.floor(Math.random() * (exp.max - exp.min + 1)),
          type: 'expense',
          category: exp.category,
          date: new Date(monthDate.getFullYear(), monthDate.getMonth(), day),
          paymentMethod: exp.method,
          notes: '',
        });
      });
    }

    await Transaction.insertMany(transactions);
    console.log(`Created ${transactions.length} transactions.`);

    // Current Month Budgets
    const currentMonthStart = new Date(now.getFullYear(), now.getMonth(), 1);
    const currentMonthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59);

    const budgets = [
      { category: 'Food & Dining', amountMinor: 1600000 },  // ₹16,000
      { category: 'Shopping', amountMinor: 1000000 },       // ₹10,000
      { category: 'Transportation', amountMinor: 500000 },  // ₹5,000
      { category: 'Bills & Utilities', amountMinor: 700000 },// ₹7,000
      { category: 'Entertainment', amountMinor: 400000 },   // ₹4,000
    ];

    await Budget.insertMany(
      budgets.map((b) => ({
        userId: user._id,
        category: b.category,
        amountMinor: b.amountMinor,
        period: 'monthly',
        startDate: currentMonthStart,
        endDate: currentMonthEnd,
      }))
    );
    console.log(`Created ${budgets.length} monthly budgets.`);

    // Savings Goals
    const goalsList = [
      {
        title: 'New Gaming & Workstation PC',
        targetAmountMinor: 18000000, // ₹1,80,000
        currentAmountMinor: 13000000, // ₹1,30,000 (72% achieved)
        monthsAhead: 4,
        color: '#6366f1',
      },
      {
        title: 'Emergency Reserve Fund (6 Months)',
        targetAmountMinor: 45000000, // ₹4,50,000
        currentAmountMinor: 31500000, // ₹3,15,000 (70% achieved)
        monthsAhead: 10,
        color: '#10b981',
      },
      {
        title: 'Himalayan Bike Roadtrip',
        targetAmountMinor: 6000000, // ₹60,000
        currentAmountMinor: 4800000, // ₹48,000 (80% achieved)
        monthsAhead: 3,
        color: '#f59e0b',
      },
    ];

    for (const g of goalsList) {
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

      // Add contribution records
      const p1 = Math.round(g.currentAmountMinor * 0.6);
      const p2 = g.currentAmountMinor - p1;

      await GoalContribution.create([
        {
          userId: user._id,
          goalId: goalDoc._id,
          amountMinor: p1,
          type: 'contribution',
          notes: 'Primary monthly savings deposit',
          createdAt: new Date(now.getFullYear(), now.getMonth() - 1, 10),
        },
        {
          userId: user._id,
          goalId: goalDoc._id,
          amountMinor: p2,
          type: 'contribution',
          notes: 'Freelance bonus allocation',
          createdAt: new Date(now.getFullYear(), now.getMonth(), 3),
        },
      ]);
    }

    console.log(`Created ${goalsList.length} savings goals with contribution ledgers.`);
    console.log('\n🎉 Successfully populated all data for om40@gmail.com!\n');
    process.exit(0);
  } catch (err) {
    console.error('Population error:', err);
    process.exit(1);
  }
};

populate();
