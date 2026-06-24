from app import create_app
from app.models import User, Troubleshoot
from app.models.troubleshoot import KategoriClusterEnum, JenisTroubleEnum, PerangkatEnum

app = create_app()

with app.app_context():
    # Get admin user
    admin = User.query.filter_by(username='admin').first()
    print(f"Admin user: {admin.username}, role: {admin.role.value}")
    
    # Simulate dashboard query exactly as in dashboard.py
    if admin.role.value == "teknisi":
        query = Troubleshoot.query.filter_by(assigned_to=admin.id)
    else:
        query = Troubleshoot.query
    
    total_data = query.count()
    print(f"\n Query result:")
    print(f"  Total: {total_data}")
    
    # Now test the filters used in dashboard
    per_kategori = {
        "Ringan": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Ringan).count(),
        "Sedang": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sedang).count(),
        "Berat": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Berat).count(),
    }
    
    print(f"  Kategori: {per_kategori}")
    
    # Test Jenis Trouble
    per_jenis = {
        "Human": query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum.Human).count(),
        "Configuration Issue": query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum.Configuration_Issue).count(),
    }
    print(f"  Jenis Trouble: {per_jenis}")
    
    # Test Perangkat
    per_perangkat = {
        "PC": query.filter(Troubleshoot.perangkat == PerangkatEnum.PC).count(),
        "Laptop": query.filter(Troubleshoot.perangkat == PerangkatEnum.Laptop).count(),
    }
    print(f"  Perangkat: {per_perangkat}")
    
    # Direct query to see if records exist
    print(f"\nDirect query to verify data exists:")
    all_troubles = Troubleshoot.query.all()
    print(f"  All troubleshoot records: {len(all_troubles)}")
    if all_troubles:
        print(f"  First record: {all_troubles[0].no_spk} - {all_troubles[0].nama_pelanggan}")
