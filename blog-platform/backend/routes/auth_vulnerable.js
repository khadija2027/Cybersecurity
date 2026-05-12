const express = require('express');
const mysql = require('mysql2');
const router = express.Router();

const db = mysql.createConnection({
    host: process.env.DB_HOST || 'mysql',
    user: process.env.DB_USER || 'blog_user',
    password: process.env.DB_PASSWORD || 'blog_password',
    database: process.env.DB_NAME || 'blog_platform'
});

db.connect((err) => {
    if (err) {
        console.error('❌ DB connection error:', err);
    } else {
        console.log('⚠️ VULNERABLE MySQL connected - SQL Injection possible');
    }
});

// VULNERABLE LOGIN - SQL INJECTION!
router.post('/login', (req, res) => {
    const { username, password } = req.body;
    
    console.log('Login attempt:', { username, password });
    
    // VULNERABLE CODE - String concatenation allows SQL injection
    const query = `SELECT * FROM Users WHERE username='${username}' AND password='${password}'`;
    
    console.log('SQL Query:', query);
    
    db.query(query, (err, results) => {
        if (err) {
            return res.status(500).json({ 
                success: false, 
                error: err.message,
                sql: query
            });
        }
        
        if (results.length > 0) {
            const user = results[0];
            res.json({
                success: true,
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    role: user.role
                },
                sql: query
            });
        } else {
            res.status(401).json({ 
                success: false, 
                error: 'Invalid credentials' 
            });
        }
    });
});

module.exports = router;