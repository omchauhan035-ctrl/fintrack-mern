const express = require('express');
const router = express.Router();
const dashboardController = require('../controllers/dashboardController');
const auth = require('../middleware/auth');

router.use(auth);

router.get('/income-expenses', dashboardController.getIncomeExpenses);
router.get('/categories', dashboardController.getCategoryAnalytics);
router.get('/trends', dashboardController.getTrends);

module.exports = router;
