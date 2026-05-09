# Blog Platform - Complete Setup Instructions

## Project Structure
```
blog-platform/
├── backend/
│   ├── models/
│   │   ├── User.js
│   │   ├── Article.js
│   │   └── Comment.js
│   ├── routes/
│   │   ├── auth.js
│   │   ├── articles.js
│   │   ├── comments.js
│   │   └── admin.js
│   ├── middleware/
│   │   └── auth.js
│   ├── package.json
│   ├── .env
│   ├── server.js
│   └── Dockerfile
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── api.js
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── article.html
│   ├── create-article.html
│   ├── admin.html
│   └── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

## Features

### Authentication & User Roles
- ✅ User registration and login with JWT authentication
- ✅ Two user roles: Admin and Normal User
- ✅ Secure password hashing with bcrypt
- ✅ Session management with JWT tokens (7-day expiry)

### Blog Functionality
- ✅ Create, read, update, delete articles (CRUD)
- ✅ Article categories and metadata
- ✅ View tracking system
- ✅ Rich article display with formatting

### Comments System
- ✅ Add comments to articles
- ✅ Edit own comments
- ✅ Delete comments (author or admin)
- ✅ Real-time comment display

### Admin Dashboard
- ✅ User statistics (total users, active users, etc.)
- ✅ User management and deactivation
- ✅ Track user activity (articles, comments, last login)
- ✅ Articles and comments overview

## Prerequisites

- Docker and Docker Compose installed
- Windows, macOS, or Linux

## Quick Start (Docker)

### 1. Navigate to project directory
```bash
cd blog-platform
```

### 2. Build and start all services
```bash
docker-compose up -d
```

This will:
- Create and start MongoDB container
- Build and start backend API server
- Build and start frontend web server

### 3. Wait for services to be ready
```bash
docker-compose ps
```

All services should show "healthy" or "running"

### 4. Access the application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health
- **MongoDB**: localhost:27017 (user: admin, pass: admin123)

## User Credentials (for testing)

### Admin User
After first launch, you can create an admin account:
- Username: admin
- Email: admin@blog.com
- Password: Admin@123
- (Then manually change role to 'admin' in MongoDB or create via API)

### Regular User
- Username: testuser
- Email: user@blog.com
- Password: User@123

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Articles
- `GET /api/articles` - Get all published articles
- `GET /api/articles/:id` - Get single article
- `POST /api/articles` - Create article (authenticated)
- `PUT /api/articles/:id` - Update article (author/admin)
- `DELETE /api/articles/:id` - Delete article (author/admin)

### Comments
- `GET /api/comments/article/:articleId` - Get article comments
- `POST /api/comments` - Create comment (authenticated)
- `PUT /api/comments/:id` - Update comment (author)
- `DELETE /api/comments/:id` - Delete comment (author/admin)

### Admin
- `GET /api/admin/users` - Get all users (admin only)
- `GET /api/admin/stats` - Get platform statistics (admin only)
- `PUT /api/admin/users/:id/deactivate` - Deactivate user (admin only)
- `GET /api/admin/users/:id/activity` - Get user activity (admin only)

## Docker Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Rebuild containers
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Access MongoDB shell
```bash
docker exec -it blog-mongodb mongosh -u admin -p admin123
```

### View running containers
```bash
docker-compose ps
```

## Troubleshooting

### Port already in use
If ports 3000, 5000, or 27017 are in use, modify docker-compose.yml:
```yaml
ports:
  - "3001:3000"  # Change 3000 to any available port
  - "5001:5000"  # Change 5000 to any available port
```

### Backend cannot connect to MongoDB
- Ensure MongoDB container is running: `docker-compose ps`
- Check MongoDB logs: `docker-compose logs mongodb`
- Verify MONGODB_URI in backend/.env is correct

### Frontend cannot reach backend
- Ensure backend is running and healthy: `docker-compose ps`
- Check that ports are correctly exposed
- Backend API should be accessible at http://localhost:5000/api/health

### Clear database and restart
```bash
docker-compose down -v
docker-compose up -d
```

## Environment Variables

### Backend (.env)
```
PORT=5000
MONGODB_URI=mongodb://mongodb:27017/blog-platform
JWT_SECRET=your_super_secret_jwt_key_change_in_production_2024
NODE_ENV=production
```

## Security Notes

⚠️ **For Production Deployment:**
1. Change JWT_SECRET to a strong, unique value
2. Change MongoDB credentials
3. Use HTTPS/SSL certificates
4. Set NODE_ENV=production
5. Use a reverse proxy (nginx)
6. Enable CORS properly
7. Add rate limiting
8. Implement input validation
9. Add CSRF protection
10. Set secure cookie flags

## Development

### Local Development (without Docker)

#### Backend
```bash
cd backend
npm install
npm run dev
```

#### Frontend
Open `frontend/index.html` in browser or serve with http-server:
```bash
npm install -g http-server
cd frontend
http-server -p 3000
```

## Performance Tips

- MongoDB data is persisted in `mongodb_data` volume
- Frontend is served via http-server (lightweight)
- Backend uses Node.js clusters for better performance
- Health checks ensure services auto-restart on failure

## Support

For issues or questions, check:
1. Docker logs: `docker-compose logs`
2. Browser console for frontend errors
3. Backend API health: `http://localhost:5000/api/health`

---

Built with ❤️ for secure and professional blogging
