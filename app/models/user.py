import enum
import bcrypt

from sqlalchemy import Integer, String, Column, Enum, Text

from app.db.base_class import Base


class RoleEnum(enum.Enum):
    SIMPLE = "simple"
    ADVANCED = "advanced"
    ADMIN = "admin"


class User(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(256), index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password_hash = Column(Text, nullable=False)
    
    @property
    def password(self):
        raise AttributeError("User.password is write-only")
    
    @staticmethod
    def generate_hash_password(password: str, rounds: int = 12):
        password = password.encode()
        salt = bcrypt.gensalt(rounds)
        return bcrypt.hashpw(password, salt)
    
    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = self.generate_hash_password(password)
    
    def verify_password(self, password: str):
        pwhash = self.generate_hash_password(password)
        return pwhash == self.password_hash
