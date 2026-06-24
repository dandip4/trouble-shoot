from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin


class RoleEnum(Enum):
    admin = "admin"
    teknisi = "teknisi"
    manajer = "manajer"


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.teknisi)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} role={self.role.value}>"
