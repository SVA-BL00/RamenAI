from pymongo import MongoClient


class Conversation:
    def __init__(self, user_id, role, content, timestamp):
        self.user_id = user_id
        self.role = role
        self.content = content
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "userId": self.user_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }
