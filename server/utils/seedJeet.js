const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../.env') });
const mongoose = require('mongoose');
const connectDB = require('../config/db');
const User = require('../models/User');
const Category = require('../models/Category');
const Transaction = require('../models/Transaction');
const Budget = require('../models/Budget');
const SavingsGoal = require('../models/SavingsGoal');
const GoalContribution = require('../models/GoalContribution');

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

async function seedJeet() {
  try {
    await connectDB();
    console.log('MongoDB Connected successfully');

    let user = await User.findOne({ email: 'jeet@gmail.com' });
    if (!user) {
      console.log('Creating jeet@gmail.com user...');
      user = await User.create({
        name: 'Jeet Patel',
        email: 'jeet@gmail.com',
        passwordHash: 'jeet@123',
        role: 'user',
        status: 'active',
        preferredCurrency: 'INR',
        theme: 'light',
      });
    }

    const userId = user._id;
    console.log(`Seeding data for Jeet (ID: ${userId})...`);

    // 1. Ensure categories exist
    const existingCats = await Category.find({ userId });
    if (existingCats.length === 0) {
      console.log('Seeding default categories...');
      const catsToInsert = defaultCategories.map((c) => ({
        ...c,
        userId,
        isDefault: true,
      }));
      await Category.insertMany(catsToInsert);
    }

    // 2. Clear old transactions, budgets, goals for clean state
    await Transaction.deleteMany({ userId });
    await Budget.deleteMany({ userId });
    await SavingsGoal.deleteMany({ userId });
    await GoalContribution.deleteMany({ userId });
    console.log('Cleared existing transactions, budgets, goals');

    // 3. Transactions dataset
    const transactions = [
      // September Income
      { title: 'Monthly Software Engineer Salary', amountMinor: 6500000, type: 'income', category: 'Salary', date: new Date('2026-09-01T10:00:00Z'), paymentMethod: 'bank_transfer', notes: 'Monthly payroll deposit' },
      { title: 'Freelance React Dashboard Project', amountMinor: 2200000, type: 'income', category: 'Freelance', date: new Date('2026-09-18T15:30:00Z'), paymentMethod: 'upi', notes: 'Client milestone 2 payment' },
      { title: 'Stock Market Dividend Payout', amountMinor: 350000, type: 'income', category: 'Investments', date: new Date('2026-09-25T11:00:00Z'), paymentMethod: 'bank_transfer', notes: 'TCS quarterly dividend' },

      // September Expenses
      { title: 'Apartment Rent - Sept', amountMinor: 1600000, type: 'expense', category: 'Bills & Utilities', date: new Date('2026-09-02T09:00:00Z'), paymentMethod: 'bank_transfer', notes: 'Monthly house rent' },
      { title: 'Whole Foods & Supermarket Haul', amountMinor: 425000, type: 'expense', category: 'Food & Dining', date: new Date('2026-09-05T18:30:00Z'), paymentMethod: 'debit_card', notes: 'Monthly groceries and household items' },
      { title: 'Petrol / Fuel Refill', amountMinor: 180000, type: 'expense', category: 'Transportation', date: new Date('2026-09-08T08:45:00Z'), paymentMethod: 'upi', notes: 'Full tank fuel' },
      { title: 'Netflix & Spotify Premium', amountMinor: 99900, type: 'expense', category: 'Entertainment', date: new Date('2026-09-10T12:00:00Z'), paymentMethod: 'credit_card', notes: 'Digital entertainment subscriptions' },
      { title: 'Weekend Dining with Friends', amountMinor: 280000, type: 'expense', category: 'Food & Dining', date: new Date('2026-09-14T20:15:00Z'), paymentMethod: 'upi', notes: 'Dinner at Barbeque Nation' },
      { title: 'Electricity & Water Utility Bill', amountMinor: 215000, type: 'expense', category: 'Bills & Utilities', date: new Date('2026-09-16T14:20:00Z'), paymentMethod: 'upi', notes: 'Sept power bill' },
      { title: 'Amazon Electronics & Accessories', amountMinor: 540000, type: 'expense', category: 'Shopping', date: new Date('2026-09-20T17:10:00Z'), paymentMethod: 'credit_card', notes: 'Mechanical keyboard and mouse' },
      { title: 'Pharmacy & Wellness Vitamins', amountMinor: 120000, type: 'expense', category: 'Healthcare', date: new Date('2026-09-22T16:00:00Z'), paymentMethod: 'cash', notes: 'Supplements and medicines' },
      { title: 'Metro Smart Card Recharge', amountMinor: 110000, type: 'expense', category: 'Transportation', date: new Date('2026-09-26T09:15:00Z'), paymentMethod: 'upi', notes: 'Commute metro card balance' },

      // October Income
      { title: 'Monthly Software Engineer Salary', amountMinor: 6500000, type: 'income', category: 'Salary', date: new Date('2026-10-01T10:00:00Z'), paymentMethod: 'bank_transfer', notes: 'Monthly payroll deposit' },
      { title: 'API Integration Consulting', amountMinor: 1800000, type: 'income', category: 'Freelance', date: new Date('2026-10-15T16:45:00Z'), paymentMethod: 'upi', notes: 'Backend Node.js consulting' },
      { title: 'Mutual Fund Capital Gains', amountMinor: 420000, type: 'income', category: 'Investments', date: new Date('2026-10-28T11:30:00Z'), paymentMethod: 'bank_transfer', notes: 'Quarterly mutual fund SIP redemption' },

      // October Expenses
      { title: 'Apartment Rent - Oct', amountMinor: 1600000, type: 'expense', category: 'Bills & Utilities', date: new Date('2026-10-02T09:00:00Z'), paymentMethod: 'bank_transfer', notes: 'Monthly house rent' },
      { title: 'Monthly Grocery Superstore', amountMinor: 510000, type: 'expense', category: 'Food & Dining', date: new Date('2026-10-04T19:00:00Z'), paymentMethod: 'debit_card', notes: 'Groceries, dairy, and veggies' },
      { title: 'Car Servicing & Synthetic Oil', amountMinor: 380000, type: 'expense', category: 'Transportation', date: new Date('2026-10-09T11:20:00Z'), paymentMethod: 'credit_card', notes: 'Annual vehicle maintenance' },
      { title: 'IMAX Cinema Tickets & Popcorn', amountMinor: 145000, type: 'expense', category: 'Entertainment', date: new Date('2026-10-12T18:40:00Z'), paymentMethod: 'upi', notes: 'Weekend movie with family' },
      { title: 'WiFi Fiber Broadband Bill', amountMinor: 109900, type: 'expense', category: 'Bills & Utilities', date: new Date('2026-10-16T13:10:00Z'), paymentMethod: 'upi', notes: 'Airtel Xstream 200Mbps' },
      { title: 'Autumn Festival Festive Clothes', amountMinor: 680000, type: 'expense', category: 'Shopping', date: new Date('2026-10-22T16:30:00Z'), paymentMethod: 'credit_card', notes: 'Diwali shopping at lifestyle store' },
      { title: 'Cafe Coffee Day Work Session', amountMinor: 165000, type: 'expense', category: 'Food & Dining', date: new Date('2026-10-25T15:00:00Z'), paymentMethod: 'upi', notes: 'Coffee and snacks while working' },
      { title: 'Annual Gym Membership Renewal', amountMinor: 250000, type: 'expense', category: 'Healthcare', date: new Date('2026-10-27T10:30:00Z'), paymentMethod: 'debit_card', notes: 'Cult.fit fitness pass' },

      // November Income
      { title: 'Monthly Software Engineer Salary', amountMinor: 6500000, type: 'income', category: 'Salary', date: new Date('2026-11-01T10:00:00Z'), paymentMethod: 'bank_transfer', notes: 'Monthly payroll deposit' },
      { title: 'Freelance Code Review Session', amountMinor: 850000, type: 'income', category: 'Freelance', date: new Date('2026-11-02T14:15:00Z'), paymentMethod: 'upi', notes: 'Code audit for fintech startup' },

      // November Expenses (Current Month)
      { title: 'Apartment Rent - Nov', amountMinor: 1600000, type: 'expense', category: 'Bills & Utilities', date: new Date('2026-11-02T09:00:00Z'), paymentMethod: 'bank_transfer', notes: 'Monthly house rent' },
      { title: 'Weekly Organic Grocery Basket', amountMinor: 185000, type: 'expense', category: 'Food & Dining', date: new Date('2026-11-03T11:00:00Z'), paymentMethod: 'cash', notes: 'Fresh fruits and organic vegetables' },
      { title: 'Mobile Postpaid & DTH Recharges', amountMinor: 79900, type: 'expense', category: 'Bills & Utilities', date: new Date('2026-11-03T13:45:00Z'), paymentMethod: 'upi', notes: 'Airtel postpaid family plan' },
      { title: 'Uber Commute to Client Office', amountMinor: 48000, type: 'expense', category: 'Transportation', date: new Date('2026-11-03T16:20:00Z'), paymentMethod: 'upi', notes: 'Cab fare' },
    ];

    const txDocs = transactions.map((t) => ({ ...t, userId }));
    await Transaction.insertMany(txDocs);
    console.log(`Inserted ${txDocs.length} transactions for Jeet`);

    // 4. Budgets for Current Month (November 2026)
    const startOfNov = new Date('2026-11-01T00:00:00Z');
    const endOfNov = new Date('2026-11-30T23:59:59Z');

    const budgets = [
      { userId, category: 'Food & Dining', amountMinor: 1500000, period: 'monthly', startDate: startOfNov, endDate: endOfNov },
      { userId, category: 'Bills & Utilities', amountMinor: 2200000, period: 'monthly', startDate: startOfNov, endDate: endOfNov },
      { userId, category: 'Transportation', amountMinor: 600000, period: 'monthly', startDate: startOfNov, endDate: endOfNov },
      { userId, category: 'Shopping', amountMinor: 1000000, period: 'monthly', startDate: startOfNov, endDate: endOfNov },
      { userId, category: 'Entertainment', amountMinor: 400000, period: 'monthly', startDate: startOfNov, endDate: endOfNov },
    ];
    await Budget.insertMany(budgets);
    console.log(`Inserted ${budgets.length} budgets for Jeet`);

    // 5. Savings Goals & Contributions
    const goalsData = [
      {
        title: 'Emergency Rainy Day Fund',
        targetAmountMinor: 15000000,
        currentAmountMinor: 9500000,
        targetDate: new Date('2027-03-31T00:00:00Z'),
        status: 'active',
        color: '#10b981',
        icon: 'shield',
        contributions: [
          { amountMinor: 4000000, date: new Date('2026-09-03T10:00:00Z'), notes: 'Initial emergency fund transfer' },
          { amountMinor: 3000000, date: new Date('2026-10-05T10:00:00Z'), notes: 'October savings contribution' },
          { amountMinor: 2500000, date: new Date('2026-11-02T10:00:00Z'), notes: 'November salary savings' },
        ],
      },
      {
        title: 'MacBook Pro M3 Max',
        targetAmountMinor: 18000000,
        currentAmountMinor: 12000000,
        targetDate: new Date('2027-01-15T00:00:00Z'),
        status: 'active',
        color: '#6366f1',
        icon: 'laptop',
        contributions: [
          { amountMinor: 5000000, date: new Date('2026-09-19T16:00:00Z'), notes: 'Freelance project 1 savings' },
          { amountMinor: 4000000, date: new Date('2026-10-16T18:00:00Z'), notes: 'Consulting gig allocation' },
          { amountMinor: 3000000, date: new Date('2026-11-02T17:00:00Z'), notes: 'Code review earnings allocation' },
        ],
      },
      {
        title: 'Goa Holiday with Family',
        targetAmountMinor: 4500000,
        currentAmountMinor: 3500000,
        targetDate: new Date('2026-12-25T00:00:00Z'),
        status: 'active',
        color: '#f59e0b',
        icon: 'plane',
        contributions: [
          { amountMinor: 2000000, date: new Date('2026-09-28T12:00:00Z'), notes: 'Advance hotel booking fund' },
          { amountMinor: 1500000, date: new Date('2026-10-29T14:00:00Z'), notes: 'Flight ticket savings' },
        ],
      },
      {
        title: 'New Electric Scooter',
        targetAmountMinor: 12000000,
        currentAmountMinor: 4500000,
        targetDate: new Date('2027-06-30T00:00:00Z'),
        status: 'active',
        color: '#06b6d4',
        icon: 'car',
        contributions: [
          { amountMinor: 2500000, date: new Date('2026-09-15T11:00:00Z'), notes: 'Initial vehicle deposit' },
          { amountMinor: 2000000, date: new Date('2026-10-20T11:00:00Z'), notes: 'Monthly scooter fund installment' },
        ],
      },
    ];

    for (const g of goalsData) {
      const { contributions, ...goalFields } = g;
      const createdGoal = await SavingsGoal.create({ ...goalFields, userId });
      const contribDocs = contributions.map((c) => ({
        userId,
        goalId: createdGoal._id,
        amountMinor: c.amountMinor,
        type: 'contribution',
        notes: c.notes,
        date: c.date,
      }));
      await GoalContribution.insertMany(contribDocs);
    }
    console.log(`Inserted ${goalsData.length} savings goals with contribution records`);

    console.log('\n======================================================');
    console.log('JEET PATEL ACCOUNT SEED SUMMARY (MongoDB):');
    console.log('  Email:        jeet@gmail.com');
    console.log(`  Transactions: ${transactions.length}`);
    console.log(`  Budgets:      ${budgets.length}`);
    console.log(`  Goals:        ${goalsData.length}`);
    console.log('======================================================\n');
    process.exit(0);
  } catch (error) {
    console.error('Seed Error:', error);
    process.exit(1);
  }
}

seedJeet();

