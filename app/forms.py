from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, TextAreaField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email


class TroubleshootForm(FlaskForm):
    no_spk = StringField("No SPK", validators=[DataRequired(), Length(max=80)])
    nama_pelanggan = StringField("Nama Pelanggan", validators=[DataRequired(), Length(max=150)])
    informasi_trouble = TextAreaField("Informasi Trouble", validators=[DataRequired()])
    jenis_trouble = SelectField("Jenis Trouble", validators=[DataRequired()], choices=[
        ("Human", "Human"),
        ("Configuration Issue", "Configuration Issue"),
        ("Hardware Failure", "Hardware Failure"),
        ("Software Issue", "Software Issue"),
        ("Network Issue", "Network Issue"),
    ])
    perangkat = SelectField("Perangkat", validators=[DataRequired()], choices=[
        ("PC", "PC"),
        ("Laptop", "Laptop"),
        ("Printer", "Printer"),
        ("Server", "Server"),
        ("Firewall", "Firewall"),
        ("Switch", "Switch"),
        ("Router", "Router"),
        ("Accesspoint", "Accesspoint"),
    ])
    service = SelectField("Service", validators=[DataRequired()], choices=[
        ("UP", "UP"),
        ("DOWN", "DOWN"),
    ])
    tanggal_komplain = DateField("Tanggal Komplain", validators=[DataRequired()], format="%Y-%m-%d")
    selesai_pengerjaan = DateField("Selesai Pengerjaan", validators=[Optional()], format="%Y-%m-%d")
    durasi_pengerjaan = IntegerField("Durasi Pengerjaan (hari)", validators=[Optional()])
    keterangan_action = TextAreaField("Keterangan Action", validators=[Optional()])
    submit = SubmitField("Simpan")


class UploadForm(FlaskForm):
    file = FileField("Pilih file Excel", validators=[
        DataRequired(),
        FileAllowed(["xlsx"], "Hanya file .xlsx yang diperbolehkan."),
    ])
    submit = SubmitField("Upload")


class AssignTroubleForm(FlaskForm):
    assigned_to = SelectField("Assign ke Teknisi", validators=[DataRequired()], coerce=int)
    submit = SubmitField("Assign")


class UpdateStatusForm(FlaskForm):
    status = SelectField("Status", validators=[DataRequired()], choices=[
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ])
    submit = SubmitField("Update Status")


class PelangganForm(FlaskForm):
    nama = StringField("Nama Pelanggan", validators=[DataRequired(), Length(max=150)])
    kontak = StringField("No Kontak", validators=[DataRequired(), Length(max=20)])
    email = StringField("Email", validators=[Optional(), Email()])
    lokasi = StringField("Lokasi", validators=[DataRequired(), Length(max=255)])
    departemen = StringField("Departemen", validators=[Optional(), Length(max=100)])
    alamat = TextAreaField("Alamat", validators=[Optional()])
    submit = SubmitField("Simpan")


class PerangkatForm(FlaskForm):
    nama = StringField("Nama Perangkat", validators=[DataRequired(), Length(max=150)])
    ip_address = StringField("IP Address", validators=[Optional(), Length(max=50)])
    mac_address = StringField("MAC Address", validators=[Optional(), Length(max=50)])
    location_code = StringField("Location Code", validators=[Optional(), Length(max=50)])
    tipe = StringField("Tipe Perangkat", validators=[DataRequired(), Length(max=100)])
    serial_number = StringField("Serial Number", validators=[Optional(), Length(max=100)])
    status = SelectField("Status", validators=[DataRequired()], choices=[
        ("Aktif", "Aktif"),
        ("Nonaktif", "Nonaktif"),
        ("Service", "Service"),
    ])
    keterangan = TextAreaField("Keterangan", validators=[Optional()])
    pelanggan_id = SelectField("Pelanggan", validators=[DataRequired()], coerce=int)
    submit = SubmitField("Simpan")
