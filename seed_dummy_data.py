"""
Script untuk seed database dengan data dummy yang banyak untuk testing
"""
import os
import sys
from datetime import datetime, timedelta
from random import choice, randint, sample

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, Pelanggan, Perangkat, Troubleshoot, User
from app.models.troubleshoot import (
    JenisTroubleEnum, 
    PerangkatEnum, 
    KategoriClusterEnum,
    ServiceEnum,
    StatusTroubleEnum
)

app = create_app()

# Data dummy untuk pelanggan
PELANGGAN_DATA = [
    {"nama": "PT Maju Jaya", "kontak": "081234567890", "email": "info@majujaya.com", "lokasi": "Jakarta Selatan", "departemen": "IT Department", "alamat": "Jl. Sudirman No. 123, Jakarta Selatan"},
    {"nama": "PT Sejahtera Mitra", "kontak": "082345678901", "email": "contact@sejahtera.com", "lokasi": "Jakarta Pusat", "departemen": "Operations", "alamat": "Jl. Thamrin No. 45, Jakarta Pusat"},
    {"nama": "CV Teknologi Cemerlang", "kontak": "083456789012", "email": "support@tekcem.co.id", "lokasi": "Bandung", "departemen": "Support", "alamat": "Jl. Asia Afrika No. 10, Bandung"},
    {"nama": "PT Global Solusi", "kontak": "084567890123", "email": "admin@globalsol.com", "lokasi": "Surabaya", "departemen": "IT", "alamat": "Jl. Pemuda No. 88, Surabaya"},
    {"nama": "Koperasi Bersama Maju", "kontak": "085678901234", "email": "info@kbm.or.id", "lokasi": "Medan", "departemen": "IT Support", "alamat": "Jl. Diponegoro No. 55, Medan"},
    {"nama": "PT Inovasi Digital", "kontak": "086789012345", "email": "hello@inovdigit.id", "lokasi": "Yogyakarta", "departemen": "Technology", "alamat": "Jl. Malioboro No. 99, Yogyakarta"},
    {"nama": "PT Sukses Bersama", "kontak": "087890123456", "email": "sales@sukberama.com", "lokasi": "Semarang", "departemen": "Admin IT", "alamat": "Jl. Pemuda No. 22, Semarang"},
    {"nama": "CV Cipta Nusantara", "kontak": "088901234567", "email": "info@ciptanusa.net", "lokasi": "Jakarta Timur", "departemen": "IT Division", "alamat": "Jl. Jendral Sudirman No. 111, Jakarta Timur"},
]

# Data dummy untuk perangkat
PERANGKAT_TIPE = ["PC", "Laptop", "Printer", "Server", "Firewall", "Switch", "Router", "Access Point"]

# Jenis trouble dan service
JENIS_TROUBLE = [
    JenisTroubleEnum.Human,
    JenisTroubleEnum.Configuration_Issue,
    JenisTroubleEnum.Hardware_Failure,
    JenisTroubleEnum.Software_Issue,
    JenisTroubleEnum.Network_Issue,
]

PERANGKAT_ENUM = [
    PerangkatEnum.PC,
    PerangkatEnum.Laptop,
    PerangkatEnum.Printer,
    PerangkatEnum.Server,
    PerangkatEnum.Firewall,
    PerangkatEnum.Switch,
    PerangkatEnum.Router,
    PerangkatEnum.Accesspoint,
]

SERVICE_ENUM = [ServiceEnum.UP, ServiceEnum.DOWN]

KATEGORI_ENUM = [
    KategoriClusterEnum.Ringan,
    KategoriClusterEnum.Sedang,
    KategoriClusterEnum.Berat,
]

STATUS_ENUM = [
    StatusTroubleEnum.Pending,
    StatusTroubleEnum.InProgress,
    StatusTroubleEnum.Completed,
]

# Deskripsi trouble yang realistis
TROUBLE_DESCRIPTIONS = [
    "Koneksi jaringan terputus-putus, tidak stabil",
    "Print server tidak merespons, printer offline",
    "Database server down, aplikasi tidak bisa akses data",
    "Hardware error pada disk, ada bad sector",
    "Konfigurasi routing salah, paket tidak sampai",
    "Memory leak di aplikasi, system jadi lambat",
    "Firewall blocking legitimate traffic",
    "WiFi signal lemah di area tertentu",
    "Malware detected pada workstation",
    "VPN connection drop setiap jam",
    "Printer out of toner",
    "Switch port tidak bekerja",
    "Password policy enforcement error",
    "Backup job failed",
    "Certificate expired",
    "DNS resolution slow",
    "Load balancer not distributing traffic evenly",
    "Monitor pixel mati",
    "Keyboard tidak responsif",
    "Email server quota penuh",
]

# Action yang diambil
ACTIONS = [
    "Restart service dan monitoring ulang",
    "Update driver terbaru dan test",
    "Reconfigure networking settings",
    "Hardware replacement dilakukan",
    "Malware scan dan cleanup",
    "Backup restore dari checkpoint terakhir",
    "Certificate renewal dan deployment",
    "Cache cleared dan optimization",
    "Reinstall OS dengan fresh setup",
    "Bandwidth upgrade dan QoS config",
]

def seed_database():
    """Seed database dengan data dummy"""
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Clear existing data
        print("🗑️  Clearing existing data...")
        Troubleshoot.query.delete()
        Perangkat.query.delete()
        Pelanggan.query.delete()
        db.session.commit()
        
        # Get users
        admin = User.query.filter_by(username="admin").first()
        teknisi = User.query.filter_by(username="teknisi1").first()
        manajer = User.query.filter_by(username="manajer1").first()
        
        if not admin:
            print("❌ Admin user not found!")
            return
        
        print("📋 Adding customers (Pelanggan)...")
        pelanggan_list = []
        for data in PELANGGAN_DATA:
            existing = Pelanggan.query.filter_by(nama=data["nama"]).first()
            if not existing:
                pelanggan = Pelanggan(
                    nama=data["nama"],
                    kontak=data["kontak"],
                    email=data["email"],
                    lokasi=data["lokasi"],
                    departemen=data["departemen"],
                    alamat=data["alamat"],
                )
                db.session.add(pelanggan)
                pelanggan_list.append(pelanggan)
                print(f"  ✓ Added: {data['nama']}")
            else:
                pelanggan_list.append(existing)
                print(f"  → Already exists: {data['nama']}")
        
        db.session.commit()
        print(f"✅ Total customers: {len(pelanggan_list)}\n")
        
        print("🖥️  Adding devices (Perangkat)...")
        perangkat_list = []
        for pelanggan in pelanggan_list:
            # Setiap customer dapat 3-6 perangkat
            num_devices = randint(3, 6)
            for i in range(num_devices):
                tipe = choice(PERANGKAT_TIPE)
                nama = f"{tipe} {pelanggan.nama} #{i+1}"
                
                # Generate IP address
                ip_parts = [str(randint(10, 192)), str(randint(1, 254)), str(randint(1, 254)), str(randint(1, 254))]
                ip = ".".join(ip_parts)
                
                # Generate MAC address
                mac_parts = [f"{randint(0, 255):02x}" for _ in range(6)]
                mac = ":".join(mac_parts)
                
                perangkat = Perangkat(
                    nama=nama,
                    tipe=tipe,
                    ip_address=ip,
                    mac_address=mac,
                    location_code=f"LOC-{pelanggan.id}-{i+1:02d}",
                    serial_number=f"SN-{pelanggan.id}{i+1:03d}{randint(1000, 9999)}",
                    status="Aktif",
                    pelanggan_id=pelanggan.id,
                )
                db.session.add(perangkat)
                perangkat_list.append(perangkat)
                print(f"  ✓ {nama} ({ip})")
        
        db.session.commit()
        print(f"✅ Total devices: {len(perangkat_list)}\n")
        
        print("🔧 Adding troubleshoot records...")
        count = 0
        
        # Create troubleshoot data spanning last 3 months
        base_date = datetime.now()
        for days_ago in range(90, 0, -1):
            num_tickets_today = randint(0, 3)  # 0-3 tickets per day
            
            for _ in range(num_tickets_today):
                created_date = base_date - timedelta(days=days_ago, hours=randint(0, 23), minutes=randint(0, 59))
                
                # Random perangkat
                perangkat = choice(perangkat_list)
                pelanggan = perangkat.pelanggan
                
                # Generate ticket
                no_spk = f"SPK-{created_date.strftime('%Y%m%d')}-{randint(1000, 9999)}"
                
                # Check if SPK already exists
                if Troubleshoot.query.filter_by(no_spk=no_spk).first():
                    continue
                
                trouble = Troubleshoot(
                    no_spk=no_spk,
                    nama_pelanggan=pelanggan.nama,
                    informasi_trouble=choice(TROUBLE_DESCRIPTIONS),
                    jenis_trouble=choice(JENIS_TROUBLE),
                    perangkat=choice(PERANGKAT_ENUM),
                    service=choice(SERVICE_ENUM),
                    tanggal_komplain=created_date,  # DateTime, not date
                    selesai_pengerjaan=(created_date + timedelta(days=randint(1, 5))) if randint(0, 1) else None,
                    durasi_pengerjaan=randint(1, 7),
                    keterangan_action=choice(ACTIONS),
                    kategori_cluster=choice(KATEGORI_ENUM),
                    status=choice(STATUS_ENUM),
                    assigned_to=teknisi.id if randint(0, 1) else None,  # Random assign ke teknisi
                    created_by=admin.id,  # Created by admin
                    pelanggan_id=pelanggan.id,
                    perangkat_id=perangkat.id,
                    created_at=created_date,
                    updated_at=created_date,
                )
                db.session.add(trouble)
                count += 1
                
                if count % 10 == 0:
                    print(f"  ✓ Added {count} troubleshoot records...")
        
        db.session.commit()
        print(f"✅ Total troubleshoot records: {count}\n")
        
        # Print summary
        total_pelanggan = Pelanggan.query.count()
        total_perangkat = Perangkat.query.count()
        total_troubleshoot = Troubleshoot.query.count()
        assigned_count = Troubleshoot.query.filter(Troubleshoot.assigned_to != None).count()
        
        print("=" * 60)
        print("📊 DATABASE SUMMARY")
        print("=" * 60)
        print(f"Total Customers (Pelanggan):    {total_pelanggan}")
        print(f"Total Devices (Perangkat):      {total_perangkat}")
        print(f"Total Troubleshoot Records:     {total_troubleshoot}")
        print(f"Assigned to Technician:         {assigned_count}")
        print(f"Pending Assignment:             {total_troubleshoot - assigned_count}")
        print("=" * 60)
        print("\n✨ Database seeding completed successfully!\n")
        
        print("🔐 Test Accounts:")
        print("  Admin:     admin / admin123")
        print("  Teknisi:   teknisi1 / teknisi123")
        print("  Manager:   manajer1 / manajer123")
        print("\n🌐 Access: http://127.0.0.1:5000\n")

if __name__ == "__main__":
    seed_database()
