const express = require('express');
const { User, Article, Comment } = global.db;
const { authMiddleware, adminMiddleware } = require('../middleware/auth');

const router = express.Router();

// Get all users (admin only)
router.get('/users', authMiddleware, adminMiddleware, async (req, res) => {
  try {
    const users = await User.findAll({
      attributes: { exclude: ['password'] }
    });
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user statistics (admin only)
router.get('/stats', authMiddleware, adminMiddleware, async (req, res) => {
  try {
    const totalUsers = await User.count();
    const totalArticles = await Article.count();
    const totalComments = await Comment.count();
    const activeUsers = await User.count({ where: { isActive: true } });

    res.json({
      totalUsers,
      activeUsers,
      totalArticles,
      totalComments
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Deactivate user (admin only)
router.put('/users/:id/deactivate', authMiddleware, adminMiddleware, async (req, res) => {
  try {
    const user = await User.findOne({
      where: { id: req.params.id }
    });

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    user.isActive = false;
    await user.save();

    res.json({ message: 'User deactivated', user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Intentionally CSRF-vulnerable and access-control-broken lab endpoint.
// Any logged-in victim can be tricked into promoting an existing attacker user.
router.post('/promote', authMiddleware, async (req, res) => {
  try {
    const { username, email } = req.body;

    if (!username && !email) {
      return res.status(400).json({ error: 'Username or email required' });
    }

    const user = await User.findOne({
      where: username ? { username } : { email }
    });

    if (!user) {
      return res.status(404).json({ error: 'User to promote not found' });
    }

    user.role = 'admin';
    await user.save();

    res.json({ message: 'User promoted by CSRF lab endpoint', user: { id: user.id, username: user.username, role: user.role } });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user activity (admin only)
router.get('/users/:id/activity', authMiddleware, adminMiddleware, async (req, res) => {
  try {
    const user = await User.findOne({
      where: { id: req.params.id },
      attributes: { exclude: ['password'] }
    });

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const articles = await Article.count({ where: { authorId: req.params.id } });
    const comments = await Comment.count({ where: { authorId: req.params.id } });

    res.json({
      user,
      articles,
      comments
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
