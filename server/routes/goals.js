const express = require('express');
const router = express.Router();
const goalController = require('../controllers/goalController');
const auth = require('../middleware/auth');
const { validate, goalRules, contributionRules } = require('../validators');

router.use(auth);

router.get('/', goalController.getGoals);
router.post('/', goalRules, validate, goalController.createGoal);
router.patch('/:id', goalController.updateGoal);
router.delete('/:id', goalController.deleteGoal);
router.post('/:id/contributions', contributionRules, validate, goalController.addContribution);
router.post('/:id/withdrawals', contributionRules, validate, goalController.addWithdrawal);

module.exports = router;
