"""
Script untuk menambah data dummy MELALUI APLIKASI (form submission)
Bukan langsung insert ke database
"""
from app import create_app
from app.models import db, Pelanggan, Perangkat, Troubleshoot
from datetime import datetime, timedelta
from random import randint, choice
import re

app = create_app()

print("=" * 70)
print("DATA DUMMY - INSERT MELALUI APLIKASI")
print("=" * 70)

with app.test_client() as client:
    print("\n1️⃣  LOGIN")
    resp = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    print(f"   Status: {resp.status_code}")
    
    # Clear existing data
    print("\n2️⃣  CLEARING EXISTING DATA")
    with app.app_context():
        Troubleshoot.query.delete()
        Perangkat.query.delete()
        Pelanggan.query.delete()
        db.session.commit()
        print("   ✓ Cleared")
    
    # Add Pelanggan via form
    print("\n3️⃣  ADDING PELANGGAN (8) VIA FORM")
    pelanggan_data = [
        {"nama": "PT Maju Jaya", "kontak": "081234567890", "email": "maju@jaya.com", "lokasi": "Jakarta Selatan", "departemen": "IT", "alamat": "Jl Sudirman 123"},
        {"nama": "PT Sejahtera Mitra", "kontak": "082345678901", "email": "sejahtera@mitra.com", "lokasi": "Jakarta Pusat", "departemen": "Ops", "alamat": "Jl Thamrin 45"},
        {"nama": "CV Teknologi Cemerlang", "kontak": "083456789012", "email": "tek@cemerlang.id", "lokasi": "Bandung", "departemen": "Support", "alamat": "Jl Asia Afrika 10"},
        {"nama": "PT Global Solusi", "kontak": "084567890123", "email": "global@solusi.com", "lokasi": "Surabaya", "departemen": "IT", "alamat": "Jl Pemuda 88"},
        {"nama": "Koperasi Bersama Maju", "kontak": "085678901234", "email": "kbm@or.id", "lokasi": "Medan", "departemen": "IT Support", "alamat": "Jl Diponegoro 55"},
        {"nama": "PT Inovasi Digital", "kontak": "086789012345", "email": "inovasi@digital.id", "lokasi": "Yogyakarta", "departemen": "Tech", "alamat": "Jl Malioboro 99"},
        {"nama": "PT Sukses Bersama", "kontak": "087890123456", "email": "sukses@bersama.com", "lokasi": "Semarang", "departemen": "Admin IT", "alamat": "Jl Pemuda 22"},
        {"nama": "CV Cipta Nusantara", "kontak": "088901234567", "email": "cipta@nusa.net", "lokasi": "Jakarta Timur", "departemen": "IT Div", "alamat": "Jl Sudirman 111"},
    ]
    
    pelanggan_ids = {}
    for data in pelanggan_data:
        resp = client.post('/pelanggan/tambah', data=data, follow_redirects=True)
        if resp.status_code == 200:
            # Check if success message in response
            if 'berhasil' in resp.data.decode().lower():
                print(f"   ✓ {data['nama']}")
                # Get the ID from database
                with app.app_context():
                    p = Pelanggan.query.filter_by(nama=data['nama']).first()
                    if p:
                        pelanggan_ids[data['nama']] = p.id
            else:
                print(f"   ! {data['nama']} (check response)")
    
    print(f"\n   Total added: {len(pelanggan_ids)}")
    
    # Add Perangkat via form
    print("\n4️⃣  ADDING PERANGKAT (20) VIA FORM")
    device_types = ["PC", "Laptop", "Printer", "Server", "Firewall", "Switch", "Router", "Access Point"]
    device_count = 0
    
    with app.app_context():
        for pelanggan_name in list(pelanggan_data[:3]):  # First 3 customers get devices
            pelanggan_id = Pelanggan.query.filter_by(nama=pelanggan_name['nama']).first().id
            
            for i in range(randint(3, 4)):
                tipe = choice(device_types)
                ip = f"192.168.{randint(1,254)}.{randint(1,254)}"
                mac = ":".join([f"{randint(0,255):02x}" for _ in range(6)])
                
                device_data = {
                    'nama': f"{tipe} {pelanggan_name['nama']} #{i+1}",
                    'tipe': tipe,
                    'ip_address': ip,
                    'mac_address': mac,
                    'location_code': f"LOC-{pelanggan_id}-{i+1:02d}",
                    'serial_number': f"SN-{pelanggan_id}{i+1:03d}{randint(1000, 9999)}",
                    'status': 'Aktif',
                    'pelanggan_id': pelanggan_id,
                    'keterangan': f"Device di lokasi {pelanggan_name['lokasi']}"
                }
                
                resp = client.post('/pelanggan/perangkat/tambah', data=device_data, follow_redirects=True)
                if resp.status_code == 200 and 'berhasil' in resp.data.decode().lower():
                    print(f"   ✓ {device_data['nama']}")
                    device_count += 1
    
    print(f"\n   Total added: {device_count}")
    
    # Add Troubleshoot via form
    print("\n5️⃣  ADDING TROUBLESHOOT (30) VIA FORM")
    
    trouble_descriptions = [
        "Koneksi jaringan terputus-putus",
        "Printer offline tidak bisa print",
        "Database server crash",
        "Hardware error disk rusak",
        "Konfigurasi routing salah",
        "Memory leak aplikasi",
        "Firewall blocking traffic",
        "WiFi signal lemah",
        "Malware terdeteksi",
        "Email server down"
    ]
    
    trouble_count = 0
    with app.app_context():
        for i in range(30):
            # Random customer and device
            pelanggan = Pelanggan.query.order_by(db.func.random()).first()
            perangkat = Perangkat.query.order_by(db.func.random()).first()
            
            if not pelanggan or not perangkat:
                continue
            
            tanggal = (datetime.now() - timedelta(days=randint(1, 60))).strftime("%Y-%m-%d")
            
            trouble_data = {
                'no_spk': f"SPK-{datetime.now().strftime('%Y%m%d')}-{randint(1000, 9999)}",
                'pelanggan_id': pelanggan.id,
                'perangkat_id': perangkat.id,
                'informasi_trouble': choice(trouble_descriptions),
                'jenis_trouble': choice(['Human', 'Configuration Issue', 'Hardware Failure', 'Software Issue', 'Network Issue']),
                'perangkat_tipe': perangkat.tipe if perangkat.tipe in ['PC', 'Laptop', 'Printer', 'Server', 'Firewall', 'Switch', 'Router', 'Accesspoint'] else 'PC',
                'service': choice(['UP', 'DOWN']),
                'tanggal_komplain': tanggal,
                'selesai_pengerjaan': (datetime.now() - timedelta(days=randint(0, 5))).strftime("%Y-%m-%d"),
                'durasi_pengerjaan': randint(1, 7),
                'keterangan_action': 'Sudah diperbaiki'
            }
            
            resp = client.post('/troubleshoot/tambah', data=trouble_data, follow_redirects=True)
            if resp.status_code == 200 and 'berhasil' in resp.data.decode().lower():
                trouble_count += 1
                if trouble_count % 5 == 0:
                    print(f"   ✓ Added {trouble_count} troubleshoot records")
    
    print(f"\n   Total added: {trouble_count}")
    
    # Verify data
    print("\n" + "=" * 70)
    print("6️⃣  VERIFICATION - DATA DI DATABASE")
    print("=" * 70)
    
    with app.app_context():
        pelanggan_count = Pelanggan.query.count()
        perangkat_count = Perangkat.query.count()
        troubleshoot_count = Troubleshoot.query.count()
        
        print(f"\n✅ Pelanggan:    {pelanggan_count} records")
        print(f"✅ Perangkat:    {perangkat_count} records")
        print(f"✅ Troubleshoot: {troubleshoot_count} records")
        
        # Show sample
        if troubleshoot_count > 0:
            print(f"\nSample troubleshoot records:")
            for t in Troubleshoot.query.limit(3).all():
                print(f"  - {t.no_spk}: {t.nama_pelanggan} ({t.perangkat.nama if t.perangkat else 'N/A'})")

print("\n" + "=" * 70)
print("✅ SELESAI - DATA BERHASIL DIMASUKKAN MELALUI APLIKASI")
print("=" * 70)
print("\nSekarang buka browser dan login untuk lihat datanya!")
print("http://127.0.0.1:5000")
