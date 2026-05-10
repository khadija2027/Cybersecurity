const express = require('express');
const jwt = require('jsonwebtoken');
const { Op } = require('sequelize');
const { User } = global.db;

const router = express.Router();

function authCookies(user, token) {
  const publicUser = encodeURIComponent(JSON.stringify({
    id: user.id,
    username: user.username,
    email: user.email,
    role: user.role
  }));

  return [
    `authToken=${encodeURIComponent(token)}; Path=/; HttpOnly; SameSite=Lax; Max-Age=604800`,
    `currentUser=${publicUser}; Path=/; SameSite=Lax; Max-Age=604800`
  ];
}

function clearAuthCookies() {
  return [
    'authToken=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0',
    'currentUser=; Path=/; SameSite=Lax; Max-Age=0'
  ];
}

// Register
router.post('/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;

    // Validation
    if (!username || !email || !password) {
      return res.status(400).json({ error: 'All fields required' });
    }

    // Check if user exists
    const existingUser = await User.findOne({
      where: {
        [Op.or]: [{ email }, { username }]
      }
    });
    if (existingUser) {
      return res.status(400).json({ error: 'User already exists' });
    }

    // Create user
    const user = await User.create({ username, email, password });

    // Generate token
    const token = jwt.sign(
      { id: user.id, username: user.username, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.setHeader('Set-Cookie', authCookies(user, token));
    res.status(201).json({
      message: 'User registered successfully',
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Login
router.post('/login', async (req, res) => {
  try {
    const { email, username, password } = req.body;

    // Accept either email or username
    if (!password || (!email && !username)) {
      return res.status(400).json({ error: 'Username/Email and password required' });
    }

    // Find user by email or username
    const user = await User.findOne({
      where: email ? { email } : { username }
    });

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    const isMatch = await user.comparePassword(password);
    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Update last login
    user.lastLogin = new Date();
    await user.save();

    const token = jwt.sign(
      { id: user.id, username: user.username, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: '7d' }
    );

    res.setHeader('Set-Cookie', authCookies(user, token));
    res.json({
      message: 'Login successful',
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Current user from cookie
router.get('/me', async (req, res) => {
  try {
    const cookieHeader = req.headers.cookie || '';
    const cookies = Object.fromEntries(
      cookieHeader
        .split(';')
        .map((part) => part.trim().split('='))
        .filter(([key, value]) => key && value)
        .map(([key, value]) => [key, decodeURIComponent(value)])
    );

    if (!cookies.authToken) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    const decoded = jwt.verify(cookies.authToken, process.env.JWT_SECRET);
    const user = await User.findByPk(decoded.id, {
      attributes: { exclude: ['password'] }
    });

    if (!user) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    res.json({ user });
  } catch (error) {
    res.status(401).json({ error: 'Not authenticated' });
  }
});

// Logout
router.post('/logout', (req, res) => {
  res.setHeader('Set-Cookie', clearAuthCookies());
  res.json({ message: 'Logged out' });
});

// Intentionally CSRF-vulnerable lab endpoint.
router.post('/change-password', async (req, res) => {
  try {
    const cookieHeader = req.headers.cookie || '';
    const cookies = Object.fromEntries(
      cookieHeader
        .split(';')
        .map((part) => part.trim().split('='))
        .filter(([key, value]) => key && value)
        .map(([key, value]) => [key, decodeURIComponent(value)])
    );

    if (!cookies.authToken) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    const decoded = jwt.verify(cookies.authToken, process.env.JWT_SECRET);
    const user = await User.findByPk(decoded.id);
    const { newPassword } = req.body;

    if (!user || !newPassword || newPassword.length < 6) {
      return res.status(400).json({ error: 'New password must be at least 6 characters' });
    }

    user.password = newPassword;
    await user.save();

    res.json({ message: 'Password changed by CSRF lab endpoint' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
