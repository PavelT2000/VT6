from config import USERS_FILE


def verify(username: str, password: str) -> bool:
    if not USERS_FILE.exists():
        return False
    for line in USERS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        login, pwd = line.split(":", 1)
        if login == username and pwd == password:
            return True
    return False
