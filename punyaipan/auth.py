import json
import os
import hashlib
import datetime
import getpass


USER_FILE = os.path.join(os.path.dirname(__file__), "user.json")


def load_users():
	if not os.path.exists(USER_FILE):
		return {}
	with open(USER_FILE, "r", encoding="utf-8") as f:
		try:
			return json.load(f)
		except Exception:
			return {}


def save_users(users: dict):
	with open(USER_FILE, "w", encoding="utf-8") as f:
		json.dump(users, f, indent=2, ensure_ascii=False)


def hash_password(password: str) -> str:
	return hashlib.sha256(password.encode("utf-8")).hexdigest()


def validate_username(username: str) -> tuple[bool, str]:
	if not username or not username.strip():
		return False, "Username tidak boleh kosong"
	return True, ""


def validate_password(password: str) -> tuple[bool, str]:
	if len(password) < 6:
		return False, "Password minimal 6 karakter"
	return True, ""


def register_user():
	users = load_users()
	username = input("Username: ").strip()
	ok, msg = validate_username(username)
	if not ok:
		print("Gagal: ", msg)
		return
	if username in users:
		print("Gagal: Username sudah terdaftar")
		return
	password = getpass.getpass("Password: ")
	ok, msg = validate_password(password)
	if not ok:
		print("Gagal: ", msg)
		return
	password2 = getpass.getpass("Konfirmasi Password: ")
	if password != password2:
		print("Gagal: Password tidak cocok")
		return
	users[username] = {
		"password": hash_password(password),
		"created_at": datetime.datetime.utcnow().isoformat() + "Z",
	}
	save_users(users)
	print("Registrasi berhasil. Anda dapat login sekarang.")


def login_user():
	users = load_users()
	username = input("Username: ").strip()
	if username not in users:
		print("Gagal: Username tidak ditemukan")
		return
	password = getpass.getpass("Password: ")
	if users[username]["password"] == hash_password(password):
		print(f"Login berhasil. Selamat datang, {username}!")
	else:
		print("Gagal: Password salah")


def main():
	while True:
		print("\nPilih aksi:")
		print("1) Registrasi")
		print("2) Login")
		print("3) Keluar")
		choice = input("Masukkan pilihan (1/2/3): ").strip()
		if choice == "1":
			register_user()
		elif choice == "2":
			login_user()
		elif choice == "3":
			print("Sampai jumpa")
			break
		else:
			print("Pilihan tidak dikenali")


if __name__ == "__main__":
	main()

