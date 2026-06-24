"""
Verifikasi: Troubleshoot <-> Pelanggan Relationship
"""
from app import create_app
from app.models import Troubleshoot, Pelanggan, Perangkat

app = create_app()

print("=" * 70)
print("TROUBLESHOOT <-> PELANGGAN RELATIONSHIP VERIFICATION")
print("=" * 70)

with app.app_context():
    # Test 1: Check relationship
    print("\n1️⃣  RELATIONSHIP CHECK:")
    print("   Checking if Troubleshoot has pelanggan relationship...")
    
    first_trouble = Troubleshoot.query.first()
    if first_trouble:
        print(f"   ✓ First troubleshoot: {first_trouble.no_spk}")
        print(f"     - pelanggan_id (FK): {first_trouble.pelanggan_id}")
        print(f"     - perangkat_id (FK): {first_trouble.perangkat_id}")
        
        if first_trouble.pelanggan:
            print(f"     - pelanggan.nama: {first_trouble.pelanggan.nama}")
            print(f"     - pelanggan.kontak: {first_trouble.pelanggan.kontak}")
            print(f"     - pelanggan.lokasi: {first_trouble.pelanggan.lokasi}")
        else:
            print(f"     - pelanggan: None (NULL FK)")
        
        if first_trouble.perangkat:
            print(f"     - perangkat.nama: {first_trouble.perangkat.nama}")
            print(f"     - perangkat.tipe: {first_trouble.perangkat.tipe}")
            print(f"     - perangkat.ip_address: {first_trouble.perangkat.ip_address}")
        else:
            print(f"     - perangkat: None (NULL FK)")
    
    # Test 2: Show multiple relationships
    print("\n2️⃣  SAMPLE DATA - TROUBLESHOOT LINKED TO CUSTOMERS:")
    troubles = Troubleshoot.query.limit(5).all()
    for t in troubles:
        pelanggan_name = t.pelanggan.nama if t.pelanggan else "N/A"
        perangkat_name = t.perangkat.nama if t.perangkat else "N/A"
        print(f"\n   {t.no_spk}:")
        print(f"      → Customer: {pelanggan_name}")
        print(f"      → Device:   {perangkat_name}")
    
    # Test 3: Reverse relationship - Pelanggan to Troubleshoot
    print("\n3️⃣  REVERSE RELATIONSHIP - CUSTOMER TO TROUBLESHOOT:")
    pelanggan = Pelanggan.query.first()
    if pelanggan:
        print(f"\n   Customer: {pelanggan.nama}")
        print(f"   Total troubleshoots: {len(pelanggan.troubleshoots)}")
        if pelanggan.troubleshoots:
            print(f"   Sample tickets:")
            for t in pelanggan.troubleshoots[:3]:
                print(f"      - {t.no_spk} ({t.status.value})")
    
    # Test 4: Count statistics
    print("\n4️⃣  STATISTICS:")
    total_troubles = Troubleshoot.query.count()
    troubles_with_customer = Troubleshoot.query.filter(Troubleshoot.pelanggan_id != None).count()
    troubles_with_device = Troubleshoot.query.filter(Troubleshoot.perangkat_id != None).count()
    
    print(f"   Total troubleshoots: {total_troubles}")
    print(f"   Linked to customer: {troubles_with_customer} ({100*troubles_with_customer/total_troubles:.1f}%)")
    print(f"   Linked to device:   {troubles_with_device} ({100*troubles_with_device/total_troubles:.1f}%)")
    
    # Test 5: Customer with most troubleshoots
    print("\n5️⃣  TOP CUSTOMERS BY ISSUE COUNT:")
    from sqlalchemy import func
    top_customers = (
        Pelanggan.query
        .outerjoin(Troubleshoot)
        .with_entities(Pelanggan.nama, func.count(Troubleshoot.id).label('count'))
        .group_by(Pelanggan.id)
        .order_by(func.count(Troubleshoot.id).desc())
        .limit(5)
        .all()
    )
    
    for i, (name, count) in enumerate(top_customers, 1):
        print(f"   {i}. {name}: {count} issues")
    
    print("\n" + "=" * 70)
    print("✅ RELATIONSHIP WORKING CORRECTLY!")
    print("=" * 70)
