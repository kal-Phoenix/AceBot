# models.py
from pymongo import MongoClient
from config import Config
from datetime import datetime

class User:
    collection = MongoClient(Config.MONGO_URI)[Config.DB_NAME]["users"]

    def __init__(self, user_id, username=None, full_name=None, stream=None, is_premium=False,
                 payment_pending=False, payment_proof=None, referral_balance=0.0,
                 referral_count=0, referred_by=None, referral_credited=False,
                 blocked=False, withdrawal_request_pending=False, pending_action=None,
                 pending_admin_approval=False, created_at=None, last_active=None):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.stream = stream
        self.is_premium = is_premium
        self.payment_pending = payment_pending
        self.payment_proof = payment_proof
        self.referral_balance = referral_balance
        self.referral_count = referral_count
        self.referred_by = referred_by
        self.referral_credited = referral_credited
        self.blocked = blocked
        self.withdrawal_request_pending = withdrawal_request_pending
        self.pending_action = pending_action
        self.pending_admin_approval = pending_admin_approval
        self.created_at = created_at or datetime.utcnow()
        self.last_active = last_active or datetime.utcnow()

    def save(self):
        """Saves or updates the user in the database."""
        self.collection.update_one(
            {"user_id": self.user_id},
            {
                "$set": {
                    "username": self.username,
                    "full_name": self.full_name,
                    "stream": self.stream,
                    "is_premium": self.is_premium,
                    "payment_pending": self.payment_pending,
                    "payment_proof": self.payment_proof,
                    "referral_balance": self.referral_balance,
                    "referral_count": self.referral_count,
                    "referred_by": self.referred_by,
                    "referral_credited": self.referral_credited,
                    "blocked": self.blocked,
                    "withdrawal_request_pending": self.withdrawal_request_pending,
                    "pending_action": self.pending_action,
                    "pending_admin_approval": self.pending_admin_approval,
                    "created_at": self.created_at,
                    "last_active": self.last_active
                }
            },
            upsert=True
        )

    def delete(self):
        """Deletes the user from the database."""
        self.collection.delete_one({"user_id": self.user_id})

    @classmethod
    def find(cls, user_id):
        """Finds a user by user_id."""
        data = cls.collection.find_one({"user_id": user_id})
        if not data:
            return None
        return cls(
            user_id=data["user_id"],
            username=data.get("username"),
            full_name=data.get("full_name"),
            stream=data.get("stream"),
            is_premium=data.get("is_premium", False),
            payment_pending=data.get("payment_pending", False),
            payment_proof=data.get("payment_proof"),
            referral_balance=data.get("referral_balance", 0.0),
            referral_count=data.get("referral_count", 0),
            referred_by=data.get("referred_by"),
            referral_credited=data.get("referral_credited", False),
            blocked=data.get("blocked", False),
            withdrawal_request_pending=data.get("withdrawal_request_pending", False),
            pending_action=data.get("pending_action"),
            pending_admin_approval=data.get("pending_admin_approval", False),
            created_at=data.get("created_at", datetime.utcnow()),
            last_active=data.get("last_active", datetime.utcnow())
        )

    @classmethod
    def all(cls):
        """Returns all users in the database."""
        users = cls.collection.find()
        return [
            cls(
                user_id=user["user_id"],
                username=user.get("username"),
                full_name=user.get("full_name"),
                stream=user.get("stream"),
                is_premium=user.get("is_premium", False),
                payment_pending=user.get("payment_pending", False),
                payment_proof=user.get("payment_proof"),
                referral_balance=user.get("referral_balance", 0.0),
                referral_count=user.get("referral_count", 0),
                referred_by=user.get("referred_by"),
                referral_credited=user.get("referral_credited", False),
                blocked=user.get("blocked", False),
                withdrawal_request_pending=user.get("withdrawal_request_pending", False),
                pending_action=user.get("pending_action"),
                pending_admin_approval=user.get("pending_admin_approval", False),
                created_at=user.get("created_at", datetime.utcnow()),
                last_active=user.get("last_active", datetime.utcnow())
            )
            for user in users
        ]

    @classmethod
    def delete_all(cls):
        """Deletes all users from the database and returns the number of deleted users."""
        result = cls.collection.delete_many({})
        return result.deleted_count