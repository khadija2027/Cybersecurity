const express = require('express');
const { Sequelize } = require('sequelize');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors({
  origin: ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5500', 'http://127.0.0.1:5500', 'http://localhost:7001', 'http://127.0.0.1:7001'],
  credentials: true,
  allowedHeaders: ['Content-Type', 'Authorization', 'X-CSRF-Token'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
}));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static('../frontend'));
app.options('*', cors());

// Initialize and start
async function startServer() {
  // Start server first (with routes that don't need DB)
  const PORT = process.env.PORT || 5000;

  // Health check endpoint (works even if DB is not ready)
  app.get('/api/health', (req, res) => {
    res.json({
      status: 'Backend is running',
      database: global.db ? 'connected' : 'connecting...'
    });
  });

  // Error handling
  app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).json({ error: 'Internal server error' });
  });

  const server = app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });

  // Initialize database with retries
  let retries = 0;
  const maxRetries = 300; // Retry for up to 10 minutes (300 * 2s)

  const initializeDatabase = async () => {
    try {
      console.log(`[${new Date().toISOString()}] Attempting database connection (attempt ${retries + 1})...`);
      console.log(`Connecting to: ${process.env.DB_HOST}:3306/${process.env.DB_NAME}`);

      // Initialize Sequelize
      const sequelize = new Sequelize(
        process.env.DB_NAME || 'blog_platform',
        process.env.DB_USER || 'blog_user',
        process.env.DB_PASSWORD || 'blog_password',
        {
          host: process.env.DB_HOST || 'localhost',
          dialect: 'mysql',
          port: 3306,
          logging: false
        }
      );

      // Authenticate
      await sequelize.authenticate();
      console.log('✓ MySQL connected');

      // Models
      const User = require('./models/User')(sequelize);
      const Article = require('./models/Article')(sequelize);
      const Comment = require('./models/Comment')(sequelize);

      // Define associations
      User.hasMany(Article, { foreignKey: 'authorId' });
      Article.belongsTo(User, { foreignKey: 'authorId' });
      User.hasMany(Comment, { foreignKey: 'authorId' });
      Comment.belongsTo(User, { foreignKey: 'authorId' });
      Article.hasMany(Comment, { foreignKey: 'articleId' });
      Comment.belongsTo(Article, { foreignKey: 'articleId' });

      // Make models available globally
      global.db = {
        sequelize,
        User,
        Article,
        Comment
      };

      // Sync database
      await sequelize.sync({ alter: false });
      console.log('✓ Database synced');

      // Register routes (only after DB is ready)
      app.use('/api/auth', require('./routes/auth'));
      app.use('/api/articles', require('./routes/articles'));
      app.use('/api/comments', require('./routes/comments'));
      app.use('/api/admin', require('./routes/admin'));

      // VULNERABLE ROUTES FOR SQL INJECTION TESTING
      app.use('/api/vulnerable', require('./routes/auth_vulnerable'));

      console.log('✓ All routes loaded');
      console.log('⚠️  Vulnerable endpoints loaded at /api/vulnerable (for testing only)');

    } catch (err) {
      retries++;
      console.error(`[${new Date().toISOString()}] Database connection attempt ${retries}/${maxRetries} failed:`, err.message);

      if (retries < maxRetries) {
        // Retry after 2 seconds
        console.log(`Retrying in 2 seconds...`);
        setTimeout(initializeDatabase, 2000);
      } else {
        console.error('✗ Max retries reached. Will keep trying...');
        // Keep retrying even after maxRetries
        setTimeout(initializeDatabase, 5000);
      }
    }
  };

  // Start attempting to connect to database
  initializeDatabase();
}

startServer();
