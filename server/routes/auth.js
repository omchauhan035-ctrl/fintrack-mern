const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const auth = require('../middleware/auth');
const { validate, registerRules, loginRules } = require('../validators');

router.post('/register', registerRules, validate, authController.register);
router.post('/login', loginRules, validate, authController.login);
router.post('/logout', authController.logout);
router.get('/me', auth, authController.getMe);
router.patch('/profile', auth, authController.updateProfile);
router.patch('/password', auth, authController.changePassword);

module.exports = router;
