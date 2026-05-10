const http = require('http');
const crypto = require('crypto');
const { URLSearchParams } = require('url');

const PORT = 7000;
const sessions = new Map();
const users = {
  victim: {
    username: 'victim',
    role: 'user',
    passwordLabel: 'training-only',
    passwordChangedAt: null,
  },
  attacker: {
    username: 'attacker',
    role: 'user',
    passwordLabel: 'attacker-lab-password',
    passwordChangedAt: null,
  },
};
let nextArticleId = 3;
const articles = [
  {
    id: 1,
    title: 'Welcome to the lab',
    content: 'Use this article ID to test the delete-article CSRF option.',
    author: 'victim',
    createdAt: new Date().toISOString(),
  },
  {
    id: 2,
    title: 'Second sample article',
    content: 'This gives you another harmless target for delete testing.',
    author: 'victim',
    createdAt: new Date().toISOString(),
  },
];

function parseCookies(header = '') {
  return Object.fromEntries(
    header
      .split(';')
      .map((part) => part.trim().split('='))
      .filter(([key, value]) => key && value)
      .map(([key, value]) => [key, decodeURIComponent(value)])
  );
}

function readBody(req) {
  return new Promise((resolve) => {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk;
      if (body.length > 1_000_000) req.destroy();
    });
    req.on('end', () => resolve(body));
  });
}

function send(res, status, contentType, body, headers = {}) {
  res.writeHead(status, {
    'Content-Type': contentType,
    ...headers,
  });
  res.end(body);
}

function htmlPage(title, body) {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title}</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main>
    ${body}
  </main>
</body>
</html>`;
}

function currentUser(req) {
  const cookies = parseCookies(req.headers.cookie);
  const session = cookies.sessionId && sessions.get(cookies.sessionId);
  return session ? users[session.username] : null;
}

function renderHome(req) {
  const user = currentUser(req);
  const articleList = articles
    .map(
      (article) => `<article>
        <h3>#${article.id}: ${escapeHtml(article.title)}</h3>
        <p>${escapeHtml(article.content)}</p>
        <small>Created by ${escapeHtml(article.author)} at ${escapeHtml(article.createdAt)}</small>
        <form method="post" action="/articles/delete" class="inline-form">
          <input type="hidden" name="id" value="${article.id}">
          <button type="submit">Delete article #${article.id}</button>
        </form>
      </article>`
    )
    .join('');
  const userRows = Object.values(users)
    .map(
      (account) => `<tr>
        <td>${escapeHtml(account.username)}</td>
        <td>${escapeHtml(account.role)}</td>
        <td>${escapeHtml(account.passwordLabel)}</td>
        <td>${escapeHtml(account.passwordChangedAt || 'never')}</td>
      </tr>`
    )
    .join('');

  return htmlPage(
    'Vulnerable Victim Blog',
    `<header>
      <h1>Vulnerable Victim Blog</h1>
      <p>This intentionally vulnerable training app uses cookie auth without a CSRF token.</p>
      ${
        user
          ? `<p class="status">Logged in as <strong>${escapeHtml(user.username)}</strong></p>
             <form method="post" action="/logout"><button type="submit">Log out</button></form>`
          : `<p><a class="button" href="/login">Log in as the victim</a></p>`
      }
    </header>

    <section>
      <h2>Create Article</h2>
      <form method="post" action="/articles">
        <label>Title <input name="title" required minlength="5"></label>
        <label>Content <textarea name="content" required minlength="10"></textarea></label>
        <button type="submit">Publish</button>
      </form>
    </section>

    <section>
      <h2>Account Settings</h2>
      <form method="post" action="/account/password">
        <label>New lab password label <input name="newPassword" value="changed-by-csrf" required></label>
        <button type="submit">Change my password label</button>
      </form>
    </section>

    <section>
      <h2>Lab Users</h2>
      <table>
        <thead>
          <tr><th>Username</th><th>Role</th><th>Password label</th><th>Password changed</th></tr>
        </thead>
        <tbody>${userRows}</tbody>
      </table>
      <p class="warning">The promote endpoint is intentionally broken: any logged-in user can promote any username.</p>
    </section>

    <section>
      <h2>Articles</h2>
      ${articleList || '<p>No articles yet.</p>'}
    </section>`
  );
}

function renderLogin() {
  return htmlPage(
    'Victim Login',
    `<h1>Victim Login</h1>
    <p>Use any password. This lab stores no real credentials.</p>
    <form method="post" action="/login">
      <label>Username <input name="username" value="victim" required></label>
      <label>Password <input name="password" type="password" value="training-only" required></label>
      <button type="submit">Log in</button>
    </form>`
  );
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

const css = `
body { font-family: Arial, sans-serif; background: #f5f7fb; color: #1f2937; margin: 0; }
main { max-width: 860px; margin: 32px auto; padding: 0 20px; }
header, section, article { background: white; border: 1px solid #d8dee9; border-radius: 8px; padding: 20px; margin-bottom: 18px; }
h1, h2, h3 { margin-top: 0; }
label { display: block; margin: 14px 0; font-weight: 700; }
input, textarea { box-sizing: border-box; display: block; width: 100%; margin-top: 6px; padding: 10px; border: 1px solid #b8c1d1; border-radius: 6px; font: inherit; }
textarea { min-height: 110px; resize: vertical; }
button, .button { display: inline-block; border: 0; border-radius: 6px; background: #2563eb; color: white; padding: 10px 14px; font-weight: 700; text-decoration: none; cursor: pointer; }
.status { background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 6px; padding: 10px; }
.warning { background: #fff7ed; border: 1px solid #fed7aa; border-radius: 6px; padding: 10px; }
.inline-form { margin-top: 12px; }
table { width: 100%; border-collapse: collapse; }
th, td { border-bottom: 1px solid #d8dee9; padding: 9px; text-align: left; }
small { color: #64748b; }
`;

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/style.css') {
    return send(res, 200, 'text/css', css);
  }

  if (req.method === 'GET' && req.url === '/') {
    return send(res, 200, 'text/html', renderHome(req));
  }

  if (req.method === 'GET' && req.url === '/login') {
    return send(res, 200, 'text/html', renderLogin());
  }

  if (req.method === 'POST' && req.url === '/login') {
    const form = new URLSearchParams(await readBody(req));
    const username = form.get('username') || 'victim';
    if (!users[username]) return send(res, 401, 'text/plain', 'Unknown lab user');
    const sessionId = crypto.randomBytes(18).toString('hex');
    sessions.set(sessionId, { username });
    return send(res, 302, 'text/plain', 'Logged in', {
      'Set-Cookie': `sessionId=${encodeURIComponent(sessionId)}; Path=/; HttpOnly`,
      Location: '/',
    });
  }

  if (req.method === 'POST' && req.url === '/logout') {
    const cookies = parseCookies(req.headers.cookie);
    if (cookies.sessionId) sessions.delete(cookies.sessionId);
    return send(res, 302, 'text/plain', 'Logged out', {
      'Set-Cookie': 'sessionId=; Path=/; Max-Age=0; HttpOnly',
      Location: '/',
    });
  }

  if (req.method === 'POST' && req.url === '/articles') {
    const user = currentUser(req);
    if (!user) return send(res, 401, 'text/plain', 'Log in first');

    const form = new URLSearchParams(await readBody(req));
    const title = form.get('title');
    const content = form.get('content');
    if (!title || !content) return send(res, 400, 'text/plain', 'Missing title or content');

    articles.unshift({
      id: nextArticleId++,
      title,
      content,
      author: user.username,
      createdAt: new Date().toISOString(),
    });

    return send(res, 302, 'text/plain', 'Article created', { Location: '/' });
  }

  if (req.method === 'POST' && req.url === '/articles/delete') {
    const user = currentUser(req);
    if (!user) return send(res, 401, 'text/plain', 'Log in first');

    const form = new URLSearchParams(await readBody(req));
    const id = Number(form.get('id'));
    const index = articles.findIndex((article) => article.id === id);
    if (index === -1) return send(res, 404, 'text/plain', 'Article not found');

    articles.splice(index, 1);
    return send(res, 302, 'text/plain', 'Article deleted', { Location: '/' });
  }

  if (req.method === 'POST' && req.url === '/account/password') {
    const user = currentUser(req);
    if (!user) return send(res, 401, 'text/plain', 'Log in first');

    const form = new URLSearchParams(await readBody(req));
    const newPassword = form.get('newPassword');
    if (!newPassword) return send(res, 400, 'text/plain', 'Missing new password label');

    user.passwordLabel = newPassword;
    user.passwordChangedAt = new Date().toISOString();
    return send(res, 302, 'text/plain', 'Password label changed', { Location: '/' });
  }

  if (req.method === 'POST' && req.url === '/admin/promote') {
    const user = currentUser(req);
    if (!user) return send(res, 401, 'text/plain', 'Log in first');

    const form = new URLSearchParams(await readBody(req));
    const username = form.get('username');
    if (!username || !users[username]) return send(res, 404, 'text/plain', 'Lab user not found');

    users[username].role = 'admin';
    return send(res, 302, 'text/plain', 'User promoted', { Location: '/' });
  }

  return send(res, 404, 'text/plain', 'Not found');
});

server.listen(PORT, () => {
  console.log(`Victim blog running at http://localhost:${PORT}`);
});
