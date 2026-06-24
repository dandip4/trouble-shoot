"""
Script untuk import data dari CSV ke database
"""
import os
import sys
import csv
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, Pelanggan, Perangkat, Troubleshoot, User
from app.models.troubleshoot import (
    JenisTroubleEnum,
    PerangkatEnum,
    ServiceEnum,
    StatusTroubleEnum
)

app = create_app()

def parse_duration(durasi_str):
    """Convert 'X Hari' to number of days"""
    if not durasi_str or durasi_str == '':
        return 0
    try:
        return int(durasi_str.split()[0])
    except:
        return 0

def get_or_create_pelanggan(nama_pelanggan):
    """Get or create pelanggan"""
    pelanggan = Pelanggan.query.filter_by(nama=nama_pelanggan).first()
    if not pelanggan:
        pelanggan = Pelanggan(
            nama=nama_pelanggan,
            kontak="",
            email="",
            lokasi="Tidak ditentukan",
            departemen="General",
            alamat=""
        )
        db.session.add(pelanggan)
        db.session.flush()
    return pelanggan

def get_or_create_perangkat(nama_pelanggan, perangkat_type, service_status):
    """Get or create perangkat for pelanggan"""
    pelanggan = get_or_create_pelanggan(nama_pelanggan)
    
    # Find existing perangkat with same type
    existing = Perangkat.query.filter_by(
        pelanggan_id=pelanggan.id,
        tipe=perangkat_type
    ).first()
    
    if existing:
        return existing
    
    # Create new perangkat
    perangkat = Perangkat(
        nama=f"{perangkat_type} {pelanggan.nama}",
        ip_address="",
        mac_address="",
        location_code="",
        tipe=perangkat_type,
        serial_number="",
        status="Aktif",
        keterangan="",
        pelanggan_id=pelanggan.id
    )
    db.session.add(perangkat)
    db.session.flush()
    return perangkat

def import_csv(csv_file):
    """Import troubleshoot data from CSV"""
    
    print("=" * 70)
    print("IMPORT DATA DARI CSV")
    print("=" * 70)
    
    if not os.path.exists(csv_file):
        print(f"❌ File tidak ditemukan: {csv_file}")
        return
    
    # Get admin user for created_by
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        print("❌ Admin user tidak ditemukan!")
        return
    
    # Clear existing data
    print("\n🗑️  CLEARING EXISTING DATA...")
    with app.app_context():
        Troubleshoot.query.delete()
        Perangkat.query.delete()
        Pelanggan.query.delete()
        db.session.commit()
        print("   ✓ Cleared")
    
    # Read CSV
    print("\n📖 MEMBACA FILE CSV...")
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print(f"   ✓ Total baris: {len(rows)}")
    except Exception as e:
        print(f"❌ Error membaca CSV: {e}")
        return
    
    # Map Jenis Trouble
    jenis_trouble_map = {
        "Human": JenisTroubleEnum.Human,
        "Human Error": JenisTroubleEnum.Human,
        "Configuration Issue": JenisTroubleEnum.Configuration_Issue,
        "Config Issue": JenisTroubleEnum.Configuration_Issue,
        "Hardware Failure": JenisTroubleEnum.Hardware_Failure,
        "Software Issue": JenisTroubleEnum.Software_Issue,
        "Network Issue": JenisTroubleEnum.Network_Issue,
    }
    
    # Map Perangkat
    perangkat_map = {
        "PC": PerangkatEnum.PC,
        "Laptop": PerangkatEnum.Laptop,
        "Printer": PerangkatEnum.Printer,
        "Server": PerangkatEnum.Server,
        "Firewall": PerangkatEnum.Firewall,
        "Switch": PerangkatEnum.Switch,
        "Router": PerangkatEnum.Router,
        "Accesspoint": PerangkatEnum.Accesspoint,
    }
    
    # Map Service
    service_map = {
        "UP": ServiceEnum.UP,
        "DOWN": ServiceEnum.DOWN,
    }
    
    # Import records
    print("\n🔧 IMPORTING TROUBLESHOOT RECORDS...")
    success_count = 0
    error_count = 0
    
    for idx, row in enumerate(rows, 1):
        try:
            # Get or create pelanggan
            pelanggan = get_or_create_pelanggan(row['Nama_Pelanggan'])
            
            # Get or create perangkat
            perangkat = get_or_create_perangkat(
                row['Nama_Pelanggan'],
                row['Perangkat'],
                row['Service']
            )
            
            # Parse dates
            tanggal_komplain = datetime.strptime(row['Tanggal_Compliment_Pelanggan'], '%Y-%m-%d %H:%M:%S')
            selesai_pengerjaan = datetime.strptime(row['Selesai_Pengerjaan'], '%Y-%m-%d %H:%M:%S') if row['Selesai_Pengerjaan'] else None
            
            # Parse duration
            durasi = parse_duration(row['Durasi_Pengerjaan'])
            
            # Create troubleshoot
            jenis_trouble = jenis_trouble_map.get(row['Jenis_Trouble'], JenisTroubleEnum.Software_Issue)
            perangkat_type = perangkat_map.get(row['Perangkat'], PerangkatEnum.PC)
            service = service_map.get(row['Service'], ServiceEnum.UP)
            
            troubleshoot = Troubleshoot(
                no_spk=row['No_SPK'],
                nama_pelanggan=row['Nama_Pelanggan'],
                informasi_trouble=row['Informasi_Trouble'],
                jenis_trouble=jenis_trouble,
                perangkat=perangkat_type,
                service=service,
                tanggal_komplain=tanggal_komplain,
                selesai_pengerjaan=selesai_pengerjaan,
                durasi_pengerjaan=durasi,
                keterangan_action=row['Keterangan_Action'],
                pelanggan_id=pelanggan.id,
                perangkat_id=perangkat.id,
                created_by=admin.id,
                status=StatusTroubleEnum.Completed if selesai_pengerjaan else StatusTroubleEnum.Pending
            )
            
            db.session.add(troubleshoot)
            success_count += 1
            
            if success_count % 10 == 0:
                print(f"  ✓ Added {success_count} records...")
            
        except Exception as e:
            error_count += 1
            print(f"  ⚠️  Row {idx} error: {e}")
    
    # Commit all changes
    try:
        db.session.commit()
        print(f"\n✅ Import selesai!")
        print(f"   ✓ Success: {success_count}")
        print(f"   ✗ Error: {error_count}")
        
        # Show summary
        with app.app_context():
            pelanggan_count = Pelanggan.query.count()
            perangkat_count = Perangkat.query.count()
            troubleshoot_count = Troubleshoot.query.count()
            
            print(f"\n📊 DATABASE SUMMARY:")
            print(f"   - Total Pelanggan: {pelanggan_count}")
            print(f"   - Total Perangkat: {perangkat_count}")
            print(f"   - Total Troubleshoot: {troubleshoot_count}")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error saat commit: {e}")

if __name__ == "__main__":
    csv_file = "data_troubleshoot_dummy.csv"
    
    with app.app_context():
        import_csv(csv_file)
