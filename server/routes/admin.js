const express = require('express');
const router = express.Router();
const auth = require('../middleware/auth');
const adminOnly = auth.adminOnly;
const adminController = require('../controllers/adminController');

// All routes require authentication and admin privileges
router.use(auth);
router.use(adminOnly);

// System overview stats
router.get('/stats', adminController.getStats);

// User management
router.get('/users', adminController.getUsers);
router.patch('/users/:id/status', adminController.updateUserStatus);
router.patch('/users/:id/role', adminController.updateUserRole);
router.delete('/users/:id', adminController.deleteUser);

// Global transactions
router.get('/transactions', adminController.getTransactions);
router.delete('/transactions/:id', adminController.deleteTransaction);

// Category management
router.get('/categories', adminController.getCategories);
router.post('/categories', adminController.createDefaultCategory);
router.delete('/categories/:id', adminController.deleteDefaultCategory);

// System health
router.get('/system', adminController.getSystemHealth);

module.exports = router;
