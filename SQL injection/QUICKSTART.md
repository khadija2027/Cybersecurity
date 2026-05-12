# SQL Injection Testing - QUICKSTART GUIDE

## Overview
Complete SQL injection testing framework with 9 progressive phases for the Blog Platform vulnerable endpoints.

## Prerequisites

### 1. Start the Blog Platform
```bash
cd blog-platform/blog-platform
docker-compose up
```

Wait for MySQL and Node.js containers to start. You should see:
```
⚠️  Vulnerable endpoints loaded at /api/vulnerable (for testing only)
```

### 2. Install Python Requirements
```bash
pip install requests
```

## Quick Start (30 seconds)

Run the complete attack orchestrator:
```bash
cd blog-platform/SQL\ injection
python attack.py
```

This will:
- Run all 9 phases sequentially
- Display live progress with color-coded output
- Save results to `captures/session_TIMESTAMP.json`
- Display summary statistics

## Running Individual Phases

### Phase 1: Error-Based SQL Injection
```bash
python phases/01_error_based.py
```
Extracts database version, name, and user through error messages and UNION SELECT.

### Phase 2: Authentication Bypass
```bash
python phases/02_auth_bypass.py
```
Demonstrates login bypass without valid credentials using OR conditions and SQL comments.

### Phase 3: Union-Based SQL Injection
```bash
python phases/03_union_based.py
```
Detects column count and extracts complete user and article data using UNION SELECT.

### Phase 4: Blind SQL Injection
```bash
python phases/04_blind_injection.py
```
Time-based and boolean-based blind injection when direct data extraction is not possible.

### Phase 5: Advanced Data Extraction
```bash
python phases/05_advanced_extraction.py
```
Uses CONCAT and GROUP_CONCAT for bulk data extraction in single query.

### Phase 6: Out-of-Band Injection
```bash
python phases/06_out_of_band.py
```
Placeholder for DNS/HTTP exfiltration techniques (requires external server setup).

### Phase 7: Second-Order Injection
```bash
python phases/07_second_order.py
```
Tests stored/second-order injection by registering payload and triggering during login.

### Phase 8: Stacked Queries
```bash
python phases/08_stacked_queries.py
```
Shows destructive techniques (INSERT admin, UPDATE passwords, DELETE, DROP) - does not execute without --execute flag.

### Phase 9: WAF Bypass Techniques
```bash
python phases/09_waf_bypass.py
```
Tests URL encoding, case variation, and comment obfuscation to bypass WAFs.

## Advanced Usage

### Run Specific Phase with Orchestrator
```bash
python attack.py --phase 3
python attack.py --phase 2
```

### Target Different URL
```bash
python attack.py --target http://attacker.com:5000
python phases/01_error_based.py --target http://custom-host:8080
```

### Verbose Output
```bash
python attack.py --verbose
python phases/03_union_based.py -v
```

### Database Discovery Tool
```bash
# Full database discovery
python explore_database.py --full

# Users only
python explore_database.py --users

# Tables and structure only
python explore_database.py --tables

# Verbose mode
python explore_database.py --full --verbose
```

This generates:
- `captures/database_discovery.json` - Complete data structure
- `captures/extracted_users.json` - All user credentials
- `captures/database_report.txt` - Readable report

## Vulnerable Endpoints

All endpoints located at `/api/vulnerable/`:

| Endpoint | Method | Parameters | Vulnerable Field |
|----------|--------|------------|------------------|
| `/login` | POST | username, password | username |
| `/register` | POST | username, email, password | All fields |
| `/search` | GET | search (query param) | search |
| `/user/:id` | GET | id (path param) | id |

## Testing Workflow

**Recommended sequence for learning:**

1. **Phase 1** - Start simple: extract database version
   ```bash
   python phases/01_error_based.py
   ```

2. **Phase 2** - Bypass authentication to understand OR logic
   ```bash
   python phases/02_auth_bypass.py
   ```

3. **Phase 3** - Learn UNION SELECT structure
   ```bash
   python phases/03_union_based.py
   ```

4. **Phase 5** - Extract bulk data efficiently
   ```bash
   python phases/05_advanced_extraction.py
   ```

5. **Explore** - Full database discovery
   ```bash
   python explore_database.py --full
   ```

## Expected Results

### Phase 1 Success
```
✓ Database Type - AND 1=1 (Status: 200)
✓ Extract Version (Status: 200)
✓ Extract Database Name (Status: 200)
```

### Phase 2 Success
```
✓ Admin Comment Bypass - AUTHENTICATION BYPASSED!
✓ Always True OR - AUTHENTICATION BYPASSED!
✓ Admin OR True - AUTHENTICATION BYPASSED!
```

### Phase 3 Success
```
✓ Column count: 9
✓ All Users
  Data length: 1500+
✓ Database Tables
```

### Phase 5 Success
```
✓ CONCAT All Users
  Data length: 2000+
✓ GROUP_CONCAT All Data
  Data length: 5000+
```

### Explore Success
```
DATABASE INFORMATION
  version: MySQL 8.x
  database: blog_db
  user: root@localhost

EXTRACTED USERS
  Username: admin
    Email: admin@blog.com
    Role: admin
    Password Hash: [hashed_password]

  Username: user1
    Email: user1@blog.com
    Role: user
```

## Viewing Results

### Real-time Results
All phases print colored output to terminal:
- ✅ Green = Success
- ❌ Red = Error
- ⚠️ Yellow = Warning
- ℹ️ Blue = Info

### Saved Results
After running attack.py, results are saved to:
```
captures/
├── session_20240101_120000.json      # Full test results
├── database_discovery.json            # Explored data
├── extracted_users.json               # User credentials
└── database_report.txt                # Readable report
```

View JSON results:
```bash
python -m json.tool captures/session_*.json | head -100
```

## Troubleshooting

### Connection Error
```
Error: Connection refused
```
**Solution:** Ensure Docker containers are running
```bash
docker ps  # Check running containers
docker-compose up  # Start if needed
```

### Timeout Error
```
Error: Timeout waiting for response
```
**Solution:** Reduce timeout or check backend:
```bash
curl http://localhost:5000/api/vulnerable/login -d '{"username":"test","password":"test"}'
```

### No Results
```
✗ Test Name (Status: 400)
```
**Solution:** Check vulnerable endpoint is loaded:
- Backend logs should show: `⚠️ Vulnerable endpoints loaded at /api/vulnerable`
- Verify endpoint is registered in `server.js`

### Authentication Bypass Not Working
**Reason:** Database may contain no admin user or incorrect schema
**Solution:** Check database contents:
```bash
python explore_database.py --users
```

## Safety Notes

⚠️ **WARNING**: This framework is for **educational purposes only** on intentionally vulnerable systems.

- **Phase 8** (Stacked Queries) is destructive - skipped by default
- Never test on production systems without authorization
- Database schema modifications are permanent
- All captures are saved to disk

## Defense Recommendations

After testing, implement these defenses:

1. **Use Parameterized Queries** (Prepared Statements)
   ```javascript
   // VULNERABLE
   const query = `SELECT * FROM Users WHERE username = '${username}'`;
   
   // SECURE
   const query = 'SELECT * FROM Users WHERE username = ?';
   db.query(query, [username]);
   ```

2. **Input Validation**
   - Whitelist allowed characters
   - Validate data types
   - Limit input length

3. **WAF/IDS**
   - ModSecurity rules
   - OWASP CRS
   - Rate limiting

4. **Logging & Monitoring**
   - Log suspicious queries
   - Alert on multiple failed attempts
   - Monitor response times

5. **Least Privilege**
   - Use read-only database users for searches
   - Restrict admin operations
   - Separate service accounts

## Files Reference

```
SQL injection/
├── README.md                 # Full documentation
├── QUICKSTART.md             # This file
├── payloads.json             # 60+ organized payloads
├── attack.py                 # Main orchestrator
├── explore_database.py       # Database discovery tool
├── phases/
│   ├── 01_error_based.py     # Phase 1 tests
│   ├── 02_auth_bypass.py     # Phase 2 tests
│   ├── 03_union_based.py     # Phase 3 tests
│   ├── 04_blind_injection.py # Phase 4 tests
│   ├── 05_advanced_extraction.py  # Phase 5 tests
│   ├── 06_out_of_band.py     # Phase 6 (placeholder)
│   ├── 07_second_order.py    # Phase 7 tests
│   ├── 08_stacked_queries.py # Phase 8 (destructive)
│   └── 09_waf_bypass.py      # Phase 9 tests
└── captures/
    ├── session_*.json        # Test results
    ├── database_discovery.json # Explored data
    └── extracted_users.json  # Credentials
```

## Next Steps

1. ✅ Start backend: `docker-compose up`
2. ✅ Install requirements: `pip install requests`
3. ✅ Run complete test: `python attack.py`
4. ✅ Explore database: `python explore_database.py --full`
5. ✅ Review results: Check `captures/` directory
6. ✅ Study payloads: Read `payloads.json` for injection techniques
7. ✅ Learn defenses: Review vulnerable code and recommended fixes

---

**Last Updated:** 2024
**Version:** 1.0
**Status:** Ready for testing
