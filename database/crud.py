# crud.py
from database.models import User

def get_or_create_user(user_id: int, username: str = None):
    user = User.find(user_id)
    if not user:
        user = User(user_id=user_id, username=username)
        user.save()
    return user

def update_user_stream(user_id: int, stream: str):
    user = User.find(user_id)
    if user:
        user.stream = stream
        user.save()
        return True
    return False

def approve_premium(user_id: int):
    user = User.find(user_id)
    if user:
        user.is_premium = True
        user.payment_pending = False
        user.save()
        return True
    return False