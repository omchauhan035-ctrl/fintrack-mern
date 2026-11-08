const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '../.env') });
const mongoose = require('mongoose');
const User = require('../models/User');
const Category = require('../models/Category');
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

const seedAdmin = async () => {
  try {
    await connectDB();

    console.log('--- Ensuring Administrator Accounts ---');

    // 1. Primary Admin User: om40@gmail.com
    const primaryAdminEmail = 'om40@gmail.com';
    let omUser = await User.findOne({ email: primaryAdminEmail });

    if (!omUser) {
      console.log(`Creating primary admin: ${primaryAdminEmail}`);
      omUser = await User.create({
        name: 'Om Chauhan',
        email: primaryAdminEmail,
        passwordHash: 'om@123',
        role: 'admin',
        status: 'active',
        preferredCurrency: 'INR',
        theme: 'dark',
      });

      const categories = defaultCategories.map((cat) => ({
        ...cat,
        userId: omUser._id,
        isDefault: true,
      }));
      await Category.insertMany(categories);
      console.log('[SUCCESS] Admin user created with email: om40@gmail.com / password: om@123');
    } else {
      omUser.role = 'admin';
      omUser.status = 'active';
      omUser.passwordHash = 'om@123';
      await omUser.save();
      console.log('[SUCCESS] Admin user updated: om40@gmail.com / password: om@123 (Role: admin)');
    }

    // 2. Also keep secondary admin active
    const adminEmail = 'admin@fintrack.com';
    let admin = await User.findOne({ email: adminEmail });
    if (admin) {
      admin.role = 'admin';
      admin.status = 'active';
      await admin.save();
    }

    console.log('\n======================================================');
    console.log('ADMIN PANEL CREDENTIALS:');
    console.log('  Email:    om40@gmail.com');
    console.log('  Password: om@123');
    console.log('  Role:     admin');
    console.log('  URL:      http://localhost:5173/admin');
    console.log('======================================================\n');

    process.exit(0);
  } catch (error) {
    console.error('Error seeding admin:', error);
    process.exit(1);
  }
};

seedAdmin();
