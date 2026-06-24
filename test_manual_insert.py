"""
Test: Insert data manual, then check dashboard
"""
from datetime import datetime
from app import create_app
from app.models import db, Troubleshoot, Pelanggan, Perangkat, User
from app.models.troubleshoot import (
    JenisTroubleEnum, PerangkatEnum, ServiceEnum,
    KategoriClusterEnum, StatusTroubleEnum
)

app = create_app()

with app.app_context():
    print("=" * 60)
    print("TEST: MANUAL DATA INSERTION")
    print("=" * 60)
    
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    print(f"\n✓ Admin user: {admin.username}")
    
    # Get or create a customer
    pelanggan = Pelanggan.query.first()
    if not pelanggan:
        print("\n! No customers found, creating one...")
        pelanggan = Pelanggan(
            nama="PT Test Manual",
            kontak="081111111111",
            email="test@test.com",
            lokasi="Jakarta",
            alamat="Jl Test",
            departemen="IT"
        )
        db.session.add(pelanggan)
        db.session.commit()
        print(f"  ✓ Created customer: {pelanggan.nama}")
    else:
        print(f"✓ Using existing customer: {pelanggan.nama}")
    
    # Get or create a device
    perangkat = Perangkat.query.first()
    if not perangkat:
        print("\n! No devices found, creating one...")
        perangkat = Perangkat(
            nama="PC Test",
            tipe="PC",
            ip_address="192.168.1.1",
            mac_address="00:11:22:33:44:55",
            status="Aktif",
            pelanggan_id=pelanggan.id
        )
        db.session.add(perangkat)
        db.session.commit()
        print(f"  ✓ Created device: {perangkat.nama}")
    else:
        print(f"✓ Using existing device: {perangkat.nama}")
    
    # Insert TEST data
    print("\n📝 Inserting TEST troubleshoot records...")
    test_records = [
        {
            "no_spk": f"SPK-TEST-00001",
            "nama_pelanggan": pelanggan.nama,
            "informasi_trouble": "Test issue 1",
            "jenis_trouble": JenisTroubleEnum.Human,
            "perangkat": PerangkatEnum.PC,
            "service": ServiceEnum.DOWN,
            "kategori_cluster": KategoriClusterEnum.Ringan,
            "status": StatusTroubleEnum.Pending,
        },
        {
            "no_spk": f"SPK-TEST-00002",
            "nama_pelanggan": pelanggan.nama,
            "informasi_trouble": "Test issue 2",
            "jenis_trouble": JenisTroubleEnum.Hardware_Failure,
            "perangkat": PerangkatEnum.PC,
            "service": ServiceEnum.DOWN,
            "kategori_cluster": KategoriClusterEnum.Sedang,
            "status": StatusTroubleEnum.InProgress,
        },
        {
            "no_spk": f"SPK-TEST-00003",
            "nama_pelanggan": pelanggan.nama,
            "informasi_trouble": "Test issue 3",
            "jenis_trouble": JenisTroubleEnum.Network_Issue,
            "perangkat": PerangkatEnum.Router,
            "service": ServiceEnum.UP,
            "kategori_cluster": KategoriClusterEnum.Berat,
            "status": StatusTroubleEnum.Completed,
        },
    ]
    
    inserted_count = 0
    for data in test_records:
        # Check if exists
        if Troubleshoot.query.filter_by(no_spk=data["no_spk"]).first():
            print(f"  → Already exists: {data['no_spk']}")
            continue
        
        trouble = Troubleshoot(
            no_spk=data["no_spk"],
            nama_pelanggan=data["nama_pelanggan"],
            informasi_trouble=data["informasi_trouble"],
            jenis_trouble=data["jenis_trouble"],
            perangkat=data["perangkat"],
            service=data["service"],
            tanggal_komplain=datetime.now(),
            durasi_pengerjaan=1,
            keterangan_action="Test action",
            kategori_cluster=data["kategori_cluster"],
            status=data["status"],
            created_by=admin.id,
            pelanggan_id=pelanggan.id,
            perangkat_id=perangkat.id,
        )
        db.session.add(trouble)
        inserted_count += 1
        print(f"  ✓ Inserted: {data['no_spk']}")
    
    db.session.commit()
    print(f"\n✓ Inserted {inserted_count} test records")
    
    # Query immediately to verify
    print("\n" + "=" * 60)
    print("DIRECT QUERY CHECK")
    print("=" * 60)
    
    test_spks = [r["no_spk"] for r in test_records]
    for spk in test_spks:
        found = Troubleshoot.query.filter_by(no_spk=spk).first()
        print(f"  {spk}: {'✓ FOUND' if found else '✗ NOT FOUND'}")
    
    # Total count
    total = Troubleshoot.query.count()
    print(f"\nTotal records in database: {total}")
    
    # Query as admin (like dashboard does)
    print("\n" + "=" * 60)
    print("DASHBOARD QUERY (ADMIN VIEW)")
    print("=" * 60)
    
    admin_query = Troubleshoot.query
    admin_total = admin_query.count()
    print(f"  Admin total: {admin_total}")
    
    # Check if TEST records are in dashboard query
    test_in_dashboard = admin_query.filter(Troubleshoot.no_spk.like("SPK-TEST%")).count()
    print(f"  TEST records in admin query: {test_in_dashboard}")
    
    if test_in_dashboard > 0:
        print("\n  ✅ TEST data IS in dashboard query!")
        test_records_query = admin_query.filter(Troubleshoot.no_spk.like("SPK-TEST%")).all()
        for t in test_records_query:
            print(f"    - {t.no_spk}: kategori={t.kategori_cluster}, status={t.status}")
    else:
        print("\n  ❌ TEST data NOT in dashboard query!")
    
    print("\n" + "=" * 60)
    print(f"Next: Check dashboard rendering via Flask test client")
    print("=" * 60)
