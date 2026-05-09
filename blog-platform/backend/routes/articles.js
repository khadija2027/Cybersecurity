const express = require('express');
const { Op } = require('sequelize');
const { Article, User } = global.db;
const { authMiddleware, adminMiddleware } = require('../middleware/auth');

const router = express.Router();

// Get all articles (public) with filtering and search
router.get('/', async (req, res) => {
  try {
    const { search, category, startDate, endDate } = req.query;
    let where = { published: true };

    // Search filter (search in title and content)
    if (search) {
      where[Op.or] = [
        { title: { [Op.like]: `%${search}%` } },
        { content: { [Op.like]: `%${search}%` } }
      ];
    }

    // Category filter
    if (category && category !== 'All') {
      where.category = category;
    }

    // Date range filter
    if (startDate || endDate) {
      where.createdAt = {};
      if (startDate) {
        where.createdAt[Op.gte] = new Date(startDate);
      }
      if (endDate) {
        const end = new Date(endDate);
        end.setHours(23, 59, 59, 999);
        where.createdAt[Op.lte] = end;
      }
    }

    const articles = await Article.findAll({
      where,
      include: [{ model: User, attributes: ['username', 'email'] }],
      order: [['createdAt', 'DESC']]
    });

    res.json(articles);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get single article
router.get('/:id', async (req, res) => {
  try {
    const article = await Article.findOne({
      where: { id: req.params.id },
      include: [{ model: User, attributes: ['username', 'email'] }]
    });
    
    if (!article) {
      return res.status(404).json({ error: 'Article not found' });
    }

    // Increment views
    article.views += 1;
    await article.save();

    res.json(article);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Create article (authenticated)
router.post('/', authMiddleware, async (req, res) => {
  try {
    const { title, content, category, image } = req.body;

    if (!title || !content) {
      return res.status(400).json({ error: 'Title and content required' });
    }

    const article = await Article.create({
      title,
      content,
      category: category || 'General',
      authorId: req.user.id,
      authorName: req.user.username,
      image: image || null
    });

    res.status(201).json({ message: 'Article created', article });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update article (author or admin)
router.put('/:id', authMiddleware, async (req, res) => {
  try {
    const article = await Article.findOne({
      where: { id: req.params.id }
    });

    if (!article) {
      return res.status(404).json({ error: 'Article not found' });
    }

    if (article.authorId !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Not authorized' });
    }

    const { title, content, category, image } = req.body;
    if (title) article.title = title;
    if (content) article.content = content;
    if (category) article.category = category;
    if (image !== undefined) article.image = image;

    await article.save();
    res.json({ message: 'Article updated', article });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete article (author or admin)
router.delete('/:id', authMiddleware, async (req, res) => {
  try {
    const article = await Article.findOne({
      where: { id: req.params.id }
    });

    if (!article) {
      return res.status(404).json({ error: 'Article not found' });
    }

    if (article.authorId !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Not authorized' });
    }

    await Article.destroy({ where: { id: req.params.id } });
    res.json({ message: 'Article deleted' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
