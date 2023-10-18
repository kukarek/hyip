from aiogram.types import Message
from misc.config import ADMINS

def isAdmin(user_id: int) -> bool:

    return True if user_id in ADMINS else False