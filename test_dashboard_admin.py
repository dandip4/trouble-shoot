from app import create_app
from app.models import User, Troubleshoot
from flask_login import current_user
from app.models.troubleshoot import KategoriClusterEnum

app = create_app()

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    print(f"Admin user:")
    print(f"  username: {admin.username}")
    print(f"  role: {admin.role}")
    print(f"  role.value: {admin.role.value}")
    
    # Simulate dashboard query for admin
    if admin.role.value == "teknisi":
        query = Troubleshoot.query.filter_by(assigned_to=admin.id)
        print(f"  -> Using technician filter")
    else:
        query = Troubleshoot.query
        print(f"  -> Using admin filter (all data)")
    
    total = query.count()
    ringan = query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Ringan).count()
    sedang = query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sedang).count()
    berat = query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Berat).count()
    
    print(f"\nDashboard metrics:")
    print(f"  Total: {total}")
    print(f"  Ringan: {ringan}")
    print(f"  Sedang: {sedang}")
    print(f"  Berat: {berat}")
