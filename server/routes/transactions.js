const express = require('express');
const router = express.Router();
const transactionController = require('../controllers/transactionController');
const auth = require('../middleware/auth');
const { validate, transactionRules } = require('../validators');

router.use(auth);

router.get('/', transactionController.getTransactions);
router.post('/', transactionRules, validate, transactionController.createTransaction);
router.get('/:id', transactionController.getTransaction);
router.patch('/:id', transactionController.updateTransaction);
router.delete('/:id', transactionController.deleteTransaction);

module.exports = router;
