const express = require('express');
const router = express.Router();
const budgetController = require('../controllers/budgetController');
const auth = require('../middleware/auth');
const { validate, budgetRules } = require('../validators');

router.use(auth);

router.get('/', budgetController.getBudgets);
router.post('/', budgetRules, validate, budgetController.createBudget);
router.patch('/:id', budgetController.updateBudget);
router.delete('/:id', budgetController.deleteBudget);

module.exports = router;
