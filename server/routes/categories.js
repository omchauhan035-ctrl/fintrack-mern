const express = require('express');
const router = express.Router();
const categoryController = require('../controllers/categoryController');
const auth = require('../middleware/auth');
const { validate, categoryRules } = require('../validators');

router.use(auth);

router.get('/', categoryController.getCategories);
router.post('/', categoryRules, validate, categoryController.createCategory);
router.patch('/:id', categoryController.updateCategory);
router.delete('/:id', categoryController.deleteCategory);

module.exports = router;
