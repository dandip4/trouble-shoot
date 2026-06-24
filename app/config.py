import os

basedir = os.path.abspath(os.path.dirname(__file__))
# Instance folder untuk menyimpan database dan file lokal lainnya
instance_path = os.path.join(basedir, '..', 'instance')
os.makedirs(instance_path, exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key-placeholder")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(instance_path, 'troubleshoot.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", os.path.join(basedir, "..", "uploads"))
