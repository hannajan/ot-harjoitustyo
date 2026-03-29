import bcrypt
import uuid
from .user_role import UserRole

class User:
  def __init__(self, username, role, password=None, user_id=None, password_hash=None):
    self.user_id = user_id or str(uuid.uuid4())
    self.username = username

    if password_hash:
      self.password_hash = password_hash  # ✔ DB:stä loginissa
    elif password:
      self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Rekisteröinti
    else:
      raise ValueError("Password or password_hash must be provided")

    if role == UserRole.EMPLOYEE or role == UserRole.MERCHANT:
      self.role = role
    else:
      raise ValueError("Invalid role")
    
  def check_password(self, password):
    return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

