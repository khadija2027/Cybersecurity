const API_URL = 'http://localhost:5000/api';
let currentUser = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  loadUserFromStorage();
  updateNavigation();
});

// Cookie-backed session state for the intentionally CSRF-vulnerable lab.
function saveUserToStorage(user) {
  currentUser = user;
}

function loadUserFromStorage() {
  const cookie = document.cookie
    .split('; ')
    .find((row) => row.startsWith('currentUser='));

  if (cookie) {
    try {
      currentUser = JSON.parse(decodeURIComponent(cookie.split('=')[1]));
    } catch (error) {
      currentUser = null;
    }
  }
}

async function logout() {
  try {
    await apiCall('/auth/logout', { method: 'POST' });
  } catch (error) {
    console.warn(error.message);
  }
  currentUser = null;
  updateNavigation();
  window.location.href = 'login.html';
}

// API Calls
async function apiCall(endpoint, options = {}) {
  const url = `${API_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };

  const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'include'
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'API Error');
  }

  return await response.json();
}

// Register
async function register(username, email, password) {
  try {
    const data = await apiCall('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    });
    saveUserToStorage(data.user);
    showNotification('Registration successful!', 'success');
    window.location.href = 'home.html';
  } catch (error) {
    showNotification(error.message, 'error');
  }
}

// Login
async function login(email, password) {
  try {
    const data = await apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    saveUserToStorage(data.user);
    showNotification('Login successful!', 'success');
    window.location.href = 'home.html';
  } catch (error) {
    showNotification(error.message, 'error');
  }
}

// Login with username
async function loginWithUsername(username, password) {
  try {
    const data = await apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    saveUserToStorage(data.user);
    showNotification('Login successful!', 'success');
    window.location.href = 'home.html';
  } catch (error) {
    showNotification(error.message, 'error');
  }
}

// Articles
async function getArticles() {
  try {
    return await apiCall('/articles');
  } catch (error) {
    showNotification(error.message, 'error');
    return [];
  }
}

// Get articles with filters
async function getArticlesFiltered(search = '', category = '', startDate = '', endDate = '') {
  try {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (category && category !== 'All') params.append('category', category);
    if (startDate) params.append('startDate', startDate);
    if (endDate) params.append('endDate', endDate);
    
    const queryString = params.toString();
    const endpoint = queryString ? `/articles?${queryString}` : '/articles';
    return await apiCall(endpoint);
  } catch (error) {
    showNotification(error.message, 'error');
    return [];
  }
}

async function getArticle(id) {
  try {
    return await apiCall(`/articles/${id}`);
  } catch (error) {
    showNotification(error.message, 'error');
    return null;
  }
}

async function createArticle(title, content, category, imageData = null) {
  try {
    const data = await apiCall('/articles', {
      method: 'POST',
      body: JSON.stringify({ title, content, category, image: imageData })
    });
    showNotification('Article created successfully!', 'success');
    return data.article;
  } catch (error) {
    showNotification(error.message, 'error');
    return null;
  }
}

async function updateArticle(id, title, content, category, imageData = null) {
  try {
    const payload = { title, content, category };
    if (imageData) payload.image = imageData;
    const data = await apiCall(`/articles/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload)
    });
    showNotification('Article updated successfully!', 'success');
    return data.article;
  } catch (error) {
    showNotification(error.message, 'error');
    return null;
  }
}

async function deleteArticle(id) {
  try {
    await apiCall(`/articles/${id}`, { method: 'DELETE' });
    showNotification('Article deleted successfully!', 'success');
    return true;
  } catch (error) {
    showNotification(error.message, 'error');
    return false;
  }
}

// Comments
async function getComments(articleId) {
  try {
    return await apiCall(`/comments/article/${articleId}`);
  } catch (error) {
    showNotification(error.message, 'error');
    return [];
  }
}

async function createComment(content, articleId) {
  try {
    const data = await apiCall('/comments', {
      method: 'POST',
      body: JSON.stringify({ content, articleId })
    });
    showNotification('Comment added!', 'success');
    return data.comment;
  } catch (error) {
    showNotification(error.message, 'error');
    return null;
  }
}

async function deleteComment(id) {
  try {
    await apiCall(`/comments/${id}`, { method: 'DELETE' });
    showNotification('Comment deleted!', 'success');
    return true;
  } catch (error) {
    showNotification(error.message, 'error');
    return false;
  }
}

// Admin
async function getUsers() {
  try {
    return await apiCall('/admin/users');
  } catch (error) {
    showNotification(error.message, 'error');
    return [];
  }
}

async function getStats() {
  try {
    return await apiCall('/admin/stats');
  } catch (error) {
    showNotification(error.message, 'error');
    return null;
  }
}

async function deactivateUser(userId) {
  try {
    await apiCall(`/admin/users/${userId}/deactivate`, { method: 'PUT' });
    showNotification('User deactivated!', 'success');
    return true;
  } catch (error) {
    showNotification(error.message, 'error');
    return false;
  }
}

// UI Helpers
function updateNavigation() {
  const userMenu = document.getElementById('userMenu');
  if (!userMenu) return;

  if (currentUser) {
    userMenu.innerHTML = `
      <span>${currentUser.username}</span>
      ${currentUser.role === 'admin' ? '<a href="admin.html" class="nav-link">Dashboard</a>' : ''}
      <a href="create-article.html" class="nav-link">Write</a>
      <button onclick="logout()" class="btn btn-primary">Logout</button>
    `;
  } else {
    userMenu.innerHTML = `
      <a href="login.html" class="nav-link">Login</a>
      <a href="register.html" class="btn btn-primary">Sign Up</a>
    `;
  }
}

function checkAuth() {
  if (!currentUser) {
    window.location.href = 'login.html';
    return false;
  }
  return true;
}

function checkAdmin() {
  if (!currentUser || currentUser.role !== 'admin') {
    window.location.href = 'home.html';
    return false;
  }
  return true;
}

function showNotification(message, type = 'info') {
  const container = document.getElementById('notifications') || createNotificationContainer();
  const alert = document.createElement('div');
  alert.className = `alert alert-${type}`;
  alert.innerHTML = `
    <span>${message}</span>
    <button class="alert-close" onclick="this.parentElement.remove()">×</button>
  `;
  container.appendChild(alert);

  setTimeout(() => alert.remove(), 5000);
}

function createNotificationContainer() {
  const container = document.createElement('div');
  container.id = 'notifications';
  container.style.cssText = 'position: fixed; top: 80px; right: 20px; z-index: 999; width: 300px;';
  document.body.appendChild(container);
  return container;
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}
