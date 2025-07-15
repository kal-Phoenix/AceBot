# database/models.py
from datetime import datetime
from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]

class User:
    collection = db["users"]

    def __init__(self, user_id: int, username: str = None, stream: str = None,
                 is_premium: bool = False, payment_pending: bool = False,
                 payment_proof: str = None, created_at: datetime = None,
                 last_active: datetime = None, pending_action: str = None,
                 pending_admin_approval: bool = False,
                 full_name: str = None,
                 # NEW FIELDS FOR REFERRAL SYSTEM
                 referral_balance: float = 0.0,
                 referral_count: int = 0,
                 referred_by: int = None,
                 referral_credited: bool = False,
                 _id=None, **kwargs):
        self.user_id = user_id
        self.username = username
        self.stream = stream
        self.is_premium = is_premium
        self.payment_pending = payment_pending
        self.payment_proof = payment_proof
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.last_active = last_active if last_active is not None else datetime.utcnow()
        self.pending_action = pending_action
        self.pending_admin_approval = pending_admin_approval
        self.full_name = full_name
        # Initialize new fields
        self.referral_balance = referral_balance
        self.referral_count = referral_count
        self.referred_by = referred_by
        self.referral_credited = referral_credited
        self._id = _id

    def save(self):
        data = self.__dict__.copy()
        data.pop('_id', None)
        self.collection.update_one(
            {"user_id": self.user_id},
            {"$set": data},
            upsert=True
        )

    @classmethod
    def find(cls, user_id: int):
        data = cls.collection.find_one({"user_id": user_id})
        if data:
            return cls(
                user_id=data['user_id'],
                username=data.get('username'),
                stream=data.get('stream'),
                _id=data.get('_id'),
                is_premium=data.get('is_premium', False),
                payment_pending=data.get('payment_pending', False),
                payment_proof=data.get('payment_proof'),
                created_at=data.get('created_at', datetime.utcnow()),
                last_active=data.get('last_active', datetime.utcnow()),
                pending_action=data.get('pending_action'),
                pending_admin_approval=data.get('pending_admin_approval', False),
                full_name=data.get('full_name'),
                # Get new fields
                referral_balance=data.get('referral_balance', 0.0),
                referral_count=data.get('referral_count', 0),
                referred_by=data.get('referred_by'),
                referral_credited=data.get('referral_credited', False)
            )
        return None