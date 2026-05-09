# Quick Start Guide - Blog Platform

## 🚀 Start the Application (30 seconds)

### Step 1: Navigate to Project
```bash
cd c:\Users\user\Desktop\Cybersecurity\blog-platform
```

### Step 2: Start All Services
```bash
docker-compose up -d
```

### Step 3: Wait for Services (1-2 minutes)
```bash
docker-compose ps
```
All services should show "Up" and "healthy"

### Step 4: Open Application
Open browser to: **http://localhost:3000**

---

## 📝 Create Your First Account

1. Click **"Sign Up"** on homepage
2. Fill in:
   - Username: `john_doe`
   - Email: `john@example.com`
   - Password: `SecurePass123`
3. Click **"Sign Up"**
4. You're now logged in! ✅

---

## ✍️ Create Your First Article

1. Click **"Write"** button (top right)
2. Fill in:
   - Title: `My First Blog Post`
   - Category: `Technology`
   - Content: Write your article here
3. Click **"Publish Article"**
4. Your article is live! ✅

---

## 💬 Add a Comment

1. Go to any article
2. Scroll down to "Comments" section
3. Write your comment
4. Click **"Post Comment"**
5. Comment appears instantly! ✅

---

## 👨‍💼 Access Admin Dashboard

### Make User an Admin (via MongoDB)

```bash
# Access MongoDB
docker exec -it blog-mongodb mongosh -u admin -p admin123

# In MongoDB shell:
use blog-platform

# Update user role to admin
db.users.updateOne(
  { email: "john@example.com" },
  { $set: { role: "admin" } }
)

# Verify
db.users.findOne({ email: "john@example.com" })

# Exit
exit
```

### Access Admin Dashboard
1. Refresh browser
2. Click **"Dashboard"** in top menu
3. View statistics and manage users ✅

---

## 🔍 View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Press Ctrl+C to exit
```

---

## ⏹️ Stop the Application

```bash
docker-compose stop
```

---

## 🔄 Restart the Application

```bash
docker-compose start
```

---

## 🧹 Clean Everything (Reset)

```bash
docker-compose down -v
docker-compose up -d
```

---

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Web application |
| **Backend API** | http://localhost:5000/api | REST API |
| **Health Check** | http://localhost:5000/api/health | System status |
| **MongoDB** | localhost:27017 | Database |

---

## 📊 Test API with Examples

### Register User via API
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "Pass123"
  }'
```

### Login via API
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "Pass123"
  }'
```

### Get All Articles
```bash
curl http://localhost:5000/api/articles
```

### Create Article (with token)
```bash
curl -X POST http://localhost:5000/api/articles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Test Article",
    "content": "This is a test article",
    "category": "General"
  }'
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Page won't load | Check if port 3000 is available, restart: `docker-compose restart` |
| Can't register | Check backend logs: `docker-compose logs backend` |
| Database error | Verify MongoDB running: `docker-compose ps` |
| Lost login on refresh | Cookies/localStorage issue - try private/incognito mode |
| Port already in use | Change ports in `docker-compose.yml` |

---

## 🎯 Feature Checklist

- [x] User Registration
- [x] User Login
- [x] Create Articles
- [x] Read Articles
- [x] Update Articles
- [x] Delete Articles
- [x] Add Comments
- [x] View Comments
- [x] Admin Dashboard
- [x] User Management
- [x] Article Statistics
- [x] Comment Tracking

---

## 📁 Project Location

```
c:\Users\user\Desktop\Cybersecurity\blog-platform\
```

Key Files:
- `docker-compose.yml` - Container orchestration
- `backend/server.js` - API server
- `frontend/index.html` - Frontend home page
- `README.md` - Full documentation
- `DEPLOYMENT_GUIDE.md` - Detailed guide

---

## ⏱️ Typical Workflow

```
1. Start application
   docker-compose up -d

2. Wait 30 seconds for services to start
   docker-compose ps

3. Open browser
   http://localhost:3000

4. Register new account
   Click "Sign Up"

5. Create article
   Click "Write"

6. Browse articles
   Click article to view

7. Comment on article
   Scroll to comments section

8. Access admin
   (After promoting user to admin)
   Click "Dashboard"

9. Stop when done
   docker-compose stop
```

---

## 📞 Quick Help

```bash
# Current running containers
docker-compose ps

# Check if services are healthy
docker-compose ps

# View real-time logs
docker-compose logs -f

# Restart everything
docker-compose restart

# Reset everything
docker-compose down -v && docker-compose up -d

# Stop everything
docker-compose down
```

---

## 🎓 Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Node.js, Express.js
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Container**: Docker & Docker Compose
- **Security**: bcrypt password hashing

---

## ✅ What's Working

✅ User authentication with JWT  
✅ Secure password hashing  
✅ Create/Read/Update/Delete articles  
✅ Comments on articles  
✅ Admin dashboard  
✅ User tracking and activity logs  
✅ Article view counter  
✅ Responsive design  
✅ Docker deployment  
✅ Health checks  

---

**Happy Blogging! 📝✨**

For detailed information, see: `README.md` and `DEPLOYMENT_GUIDE.md`
