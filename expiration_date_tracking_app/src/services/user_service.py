from entities.merchant import Merchant

from repositories.user_repository import (
    user_repository as default_user_repository
)

class UserService:
  def __init__(self, user_repository = default_user_repository):
    self._user_repository = user_repository

  def register_merchant(self, username, password):
    if not username or not password:
      raise ValueError("Username or password missing")
    
    #username is at least 5 charaters long
    if len(username) < 5:
      raise ValueError("Username must be at least 5 characters long")

    #username is unique
    if self._user_repository.find_by_username(username):
      raise ValueError("Username already exists")

    #password is at least 8 characters long
    if len(password) < 8:
      raise ValueError("Password must be at least 8 characters long")
    
    merchant = Merchant(username, password)
    self._user_repository.create(merchant)
    
user_service = UserService()