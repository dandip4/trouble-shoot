from enum import Enum
from . import db


class JenisTroubleEnum(Enum):
    Human = "Human"
    Configuration_Issue = "Configuration Issue"
    Hardware_Failure = "Hardware Failure"
    Software_Issue = "Software Issue"
    Network_Issue = "Network Issue"


class PerangkatEnum(Enum):
    PC = "PC"
    Laptop = "Laptop"
    Printer = "Printer"
    Server = "Server"
    Firewall = "Firewall"
    Switch = "Switch"
    Router = "Router"
    Accesspoint = "Accesspoint"


class ServiceEnum(Enum):
    UP = "UP"
    DOWN = "DOWN"


class KategoriClusterEnum(Enum):
    Ringan = "Ringan"
    Sedang = "Sedang"
    Berat = "Berat"


class StatusTroubleEnum(Enum):
    Pending = "Pending"
    InProgress = "In Progress"
    Completed = "Completed"


class Troubleshoot(db.Model):
    __tablename__ = "troubleshoot"

    id = db.Column(db.Integer, primary_key=True)
    no_spk = db.Column(db.String(80), unique=True, nullable=False)
    nama_pelanggan = db.Column(db.String(150), nullable=False)
    informasi_trouble = db.Column(db.Text, nullable=False)
    jenis_trouble = db.Column(db.Enum(JenisTroubleEnum), nullable=False)
    perangkat = db.Column(db.Enum(PerangkatEnum), nullable=False)
    service = db.Column(db.Enum(ServiceEnum), nullable=False)
    tanggal_komplain = db.Column(db.DateTime, nullable=False)
    selesai_pengerjaan = db.Column(db.DateTime, nullable=True)
    durasi_pengerjaan = db.Column(db.Integer, nullable=True)
    keterangan_action = db.Column(db.Text, nullable=True)
    cluster_id = db.Column(db.Integer, nullable=True)
    kategori_cluster = db.Column(db.Enum(KategoriClusterEnum), nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.Enum(StatusTroubleEnum), nullable=False, default=StatusTroubleEnum.Pending)
    pelanggan_id = db.Column(db.Integer, db.ForeignKey("pelanggan.id"), nullable=True)
    perangkat_id = db.Column(db.Integer, db.ForeignKey("perangkat.id"), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    user = db.relationship("User", backref=db.backref("troubleshoots", lazy="dynamic"), lazy="select", foreign_keys=[created_by])
    assigned_user = db.relationship("User", backref=db.backref("assigned_troubleshoots", lazy="dynamic"), lazy="select", foreign_keys=[assigned_to])

    def __repr__(self):
        return f"<Troubleshoot {self.no_spk} {self.nama_pelanggan}>"
