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
