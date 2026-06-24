from . import db


class Perangkat(db.Model):
    __tablename__ = "perangkat"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=False)
    ip_address = db.Column(db.String(50), nullable=True)
    mac_address = db.Column(db.String(50), nullable=True)
    location_code = db.Column(db.String(50), nullable=True)
    tipe = db.Column(db.String(100), nullable=False)  # PC, Laptop, Printer, Server, etc
    serial_number = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Aktif")  # Aktif, Nonaktif, Service
    keterangan = db.Column(db.Text, nullable=True)
    pelanggan_id = db.Column(db.Integer, db.ForeignKey("pelanggan.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    # Relationships
    troubleshoots = db.relationship("Troubleshoot", backref="perangkat_ref", lazy="dynamic")

    def __repr__(self):
        return f"<Perangkat {self.nama}>"
