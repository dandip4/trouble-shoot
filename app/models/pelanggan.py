from . import db


class Pelanggan(db.Model):
    __tablename__ = "pelanggan"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False, unique=True)
    kontak = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    lokasi = db.Column(db.String(255), nullable=False)
    departemen = db.Column(db.String(100), nullable=True)
    alamat = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    # Relationships
    perangkats = db.relationship("Perangkat", backref="pelanggan", lazy="dynamic", cascade="all, delete-orphan")
    troubleshoots = db.relationship("Troubleshoot", backref="pelanggan_ref", lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pelanggan {self.nama}>"
