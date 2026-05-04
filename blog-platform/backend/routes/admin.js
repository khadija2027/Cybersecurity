const express = require('express');
const User = require('../models/User');
const Article = require('../models/Article');
const Comment = require('../models/Comment');
const { authMiddleware, adminMiddleware } = require('../middleware/auth');

const router = express.Router();

// Get all users (admin only)
router.get('/users', authMiddleware, adminMiddleware, async (req, res) => {
  try {
    const users = await User.find().select('-password');
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user statistics (admin only)
router.get('/stats', authMiddleware, adminMiddleware, async (req, res) => {
  try {
    const totalUsers = await User.countDocuments();
    const totalArticles = await Article.countDocuments();
    const totalComments = await Comment.countDocuments();
    const activeUsers = await User.countDocuments({ isActive: true });

    const userStats = await User.aggregate([
      {
        $group: {
          _id: '$role',
          count: { $sum: 1 }
        }
      }
    ]);

    res.json({
      totalUsers,
      activeUsers,
      totalArticles,
      totalComments,
      usersByRole: userStats
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Deactivate user (admin only)
router.put('/users/:id/deactivate', authMiddleware, adminMiddleware, async (req, res) => {
  try {
    const user = await User.findByIdAndUpdate(
      req.params.id,
      { isActive: false },
      { new: true }
    );

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json({ message: 'User deactivated', user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user activity (admin only)
router.get('/users/:id/activity', authMiddleware, adminMiddleware, async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const articles = await Article.countDocuments({ author: req.params.id });
    const comments = await Comment.countDocuments({ author: req.params.id });

    res.json({
      user: user.toJSON(),
      articles,
      comments,
      lastLogin: user.lastLogin,
      createdAt: user.createdAt
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
