const jwt = require('jsonwebtoken');

const parseCookies = (header = '') => Object.fromEntries(
  header
    .split(';')
    .map((part) => part.trim().split('='))
    .filter(([key, value]) => key && value)
    .map(([key, value]) => [key, decodeURIComponent(value)])
);

// Authentication middleware
const authMiddleware = (req, res, next) => {
  try {
    const cookies = parseCookies(req.headers.cookie);
    const bearerToken = req.headers.authorization?.split(' ')[1];
    const token = cookies.authToken || bearerToken;

    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};

const adminMiddleware = (req, res, next) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Admin access required' });
  }
  next();
};

module.exports = { authMiddleware, adminMiddleware };
