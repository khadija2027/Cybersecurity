const express = require('express');
const { Comment, User } = global.db;
const { authMiddleware } = require('../middleware/auth');

const router = express.Router();

// Get comments for article
router.get('/article/:articleId', async (req, res) => {
  try {
    const comments = await Comment.findAll({
      where: { articleId: req.params.articleId },
      include: [{ model: User, attributes: ['username'] }],
      order: [['createdAt', 'DESC']]
    });
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

    const comment = await Comment.create({
      content,
      articleId,
      authorId: req.user.id,
      authorName: req.user.username
    });

    res.status(201).json({ message: 'Comment created', comment });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update comment (author only)
router.put('/:id', authMiddleware, async (req, res) => {
  try {
    const comment = await Comment.findOne({
      where: { id: req.params.id }
    });

    if (!comment) {
      return res.status(404).json({ error: 'Comment not found' });
    }

    if (comment.authorId !== req.user.id) {
      return res.status(403).json({ error: 'Not authorized' });
    }

    if (req.body.content) {
      comment.content = req.body.content;
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
    const comment = await Comment.findOne({
      where: { id: req.params.id }
    });

    if (!comment) {
      return res.status(404).json({ error: 'Comment not found' });
    }

    if (comment.authorId !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Not authorized' });
    }

    await Comment.destroy({ where: { id: req.params.id } });
    res.json({ message: 'Comment deleted' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
