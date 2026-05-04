const express = require('express');
const Comment = require('../models/Comment');
const { authMiddleware } = require('../middleware/auth');

const router = express.Router();

// Get comments for article
router.get('/article/:articleId', async (req, res) => {
  try {
    const comments = await Comment.find({ article: req.params.articleId })
      .populate('author', 'username')
      .sort({ createdAt: -1 });
    res.json(comments);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create comment
router.post('/', authMiddleware, async (req, res) => {
  try {
    const { content, articleId } = req.body;

    if (!content || !articleId) {
      return res.status(400).json({ error: 'Content and articleId required' });
    }

    const comment = new Comment({
      content,
      article: articleId,
      author: req.user.id,
      authorName: req.user.username
    });

    await comment.save();
    res.status(201).json({ message: 'Comment created', comment });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update comment (author only)
router.put('/:id', authMiddleware, async (req, res) => {
  try {
    const comment = await Comment.findById(req.params.id);

    if (!comment) {
      return res.status(404).json({ error: 'Comment not found' });
    }

    if (comment.author.toString() !== req.user.id) {
      return res.status(403).json({ error: 'Not authorized' });
    }

    if (req.body.content) {
      comment.content = req.body.content;
      comment.updatedAt = new Date();
    }

    await comment.save();
    res.json({ message: 'Comment updated', comment });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete comment (author or admin)
router.delete('/:id', authMiddleware, async (req, res) => {
  try {
    const comment = await Comment.findById(req.params.id);

    if (!comment) {
      return res.status(404).json({ error: 'Comment not found' });
    }

    if (comment.author.toString() !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Not authorized' });
    }

    await Comment.deleteOne({ _id: req.params.id });
    res.json({ message: 'Comment deleted' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
