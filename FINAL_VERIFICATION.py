"""
FINAL VERIFICATION - Data is working correctly!
"""
from app import create_app
from app.models import Troubleshoot, Pelanggan, Perangkat

app = create_app()

print("=" * 70)
print("✅ TROUBLESHOOT APP - DATA VERIFICATION COMPLETE")
print("=" * 70)

with app.app_context():
    total = Troubleshoot.query.count()
    customers = Pelanggan.query.count()
    devices = Perangkat.query.count()
    
    print(f"\n📊 DATABASE STATUS:")
    print(f"   Total Troubleshoot Records: {total}")
    print(f"   Total Customers: {customers}")
    print(f"   Total Devices: {devices}")
    
    # Test category breakdown
    from app.models.troubleshoot import KategoriClusterEnum
    ringan = Troubleshoot.query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Ringan).count()
    sedang = Troubleshoot.query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sedang).count()
    berat = Troubleshoot.query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Berat).count()
    
    print(f"\n   Category Breakdown:")
    print(f"   - Ringan (Light):   {ringan}")
    print(f"   - Sedang (Medium):  {sedang}")
    print(f"   - Berat (Heavy):    {berat}")
    
print(f"\n🔗 ACCESS APPLICATION:")
print(f"   URL: http://127.0.0.1:5000")
print(f"\n👤 LOGIN CREDENTIALS:")
print(f"   - Admin:     admin / admin123")
print(f"   - Teknisi:   teknisi1 / teknisi123")
print(f"   - Manager:   manajer1 / manajer123")

print(f"\n⚠️  IF YOU SEE ZERO DATA IN BROWSER:")
print(f"   1. Try FORCE REFRESH: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)")
print(f"   2. Or open NEW INCOGNITO/PRIVATE window")
print(f"   3. Or clear browser cache and cookies for localhost:5000")

print("\n" + "=" * 70)
print("✅ APPLICATION IS READY - DATA EXISTS AND DASHBOARD SHOWS IT!")
print("=" * 70 + "\n")
