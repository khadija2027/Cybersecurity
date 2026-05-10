# CSRF Training Lab

This folder contains a local CSRF demo. It does not steal usernames, old passwords, cookies, or tokens.

This folder now targets the real local `blog-platform` app after you switch it to cookie-based lab auth.

The lab uses two local sites:

- Victim blog-platform: `http://localhost:5000`
- Attacker lab: `http://localhost:7001`

## Run

From this folder:

```powershell
.\start-lab.ps1
```

Or run the attacker server manually:

```powershell
node attacker-server.js
```

## Exercise

1. Make sure the blog-platform backend is running on `http://localhost:5000`.
2. Open `http://localhost:5000/login.html` and log in as the victim.
3. For the admin-promotion attack, make sure an account named `attacker` exists first.
4. Open `http://localhost:7001`.
5. Pick one of the attack actions and generate a link.
6. Open the generated link in the same browser.
7. Go back to `http://localhost:5000` and notice that the selected action happened through the victim session.
8. Check the `captures` folder. It records only the visit proof, user agent, timestamp, and selected training payload.

## Attack Options

- Create article: submits a hidden form to `POST /api/articles`.
- Delete article: submits a hidden form to `POST /api/articles/:id/delete`.
- Change password: submits a hidden form to `POST /api/auth/change-password`. This changes the current victim password to the value you chose; it never reads the old password.
- Make attacker admin: submits a hidden form to `POST /api/admin/promote`. This demonstrates CSRF combined with intentionally broken access control.

## Why This Is CSRF

The modified blog-platform uses a session cookie and accepts state-changing `POST` requests without a CSRF token. When the logged-in browser visits the attacker page, the browser automatically includes the blog-platform cookie with the forged form request.

## How To Fix Cookie-Based CSRF

- Use `SameSite=Lax` or `SameSite=Strict` cookies where possible.
- Require a CSRF token for every state-changing request.
- Reject unexpected `Origin` or `Referer` headers.
- Avoid using `GET` requests for actions that change data.
- Keep sensitive data out of attacker-visible URLs and logs.
