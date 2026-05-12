const express = require('express');
const cors = require('cors');
const mysql = require('mysql2');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware - IMPORTANT: must be before routes
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// MySQL connection
const db = mysql.createConnection({
    host: process.env.DB_HOST || 'mysql',
    user: process.env.DB_USER || 'blog_user',
    password: process.env.DB_PASSWORD || 'blog_password',
    database: process.env.DB_NAME || 'blog_platform'
});

db.connect((err) => {
    if (err) {
        console.error('❌ DB error:', err);
    } else {
        console.log('✅ Vulnerable DB connected');
    }
});

// Health check
app.get('/api/health', (req, res) => {
    res.json({
        status: 'ok',
        version: 'VULNERABLE',
        message: 'SQL Injection enabled'
    });
});

// VULNERABLE LOGIN ENDPOINT
app.post('/api/vulnerable/login', (req, res) => {
    const { username, password } = req.body;

    console.log('Login attempt:', { username, password });

    // VULNERABLE - String concatenation allows SQL injection
    const query = `SELECT * FROM Users WHERE username = '${username}' AND password = '${password}'`;

    console.log('SQL Query:', query);

    db.query(query, (err, results) => {
        if (err) {
            console.error('SQL Error:', err);
            return res.status(500).json({
                success: false,
                error: err.message,
                sql: query
            });
        }

        if (results && results.length > 0) {
            const user = results[0];
            console.log('Login success:', user.username);
            res.json({
                success: true,
                message: 'Login successful',
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    role: user.role
                },
                sql: query
            });
        } else {
            console.log('Login failed: invalid credentials');
            res.status(401).json({
                success: false,
                error: 'Invalid credentials'
            });
        }
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`\n🔓 VULNERABLE SERVER RUNNING`);
    console.log(`📍 Port: ${PORT}`);
    console.log(`🎯 SQL Injection endpoint: http://localhost:${PORT}/api/vulnerable/login`);
    console.log(`💉 Try: username = admin' --, password = anything\n`);
});