import bcrypt
import secrets
import string

def hash_password(password: str) -> str:
    """对密码进行哈希加密"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def is_password_strong(password: str) -> bool:
    """检查密码强度"""
    if len(password) < 6:
        return False
    return True

def generate_default_password(length: int = 8) -> str:
    """生成默认密码"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def hash_default_password() -> tuple[str, str]:
    """生成并哈希默认密码"""
    default_password = generate_default_password()
    hashed_password = hash_password(default_password)
    return default_password, hashed_password
