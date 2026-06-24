from app import create_app
from app.models import User, Troubleshoot

app = create_app()
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    print('Admin user:')
    print(f'  Username: {admin.username}')
    print(f'  Role: {admin.role}')
    print(f'  Role value: {admin.role.value}')
    print(f'  Is admin role: {admin.role.value == "admin"}')
    
    # Check troubleshoot
    troubles = Troubleshoot.query.all()
    print(f'\nTotal troubleshoot records: {len(troubles)}')
    
    if troubles:
        for t in troubles[:3]:
            print(f'  - {t.no_spk}: {t.nama_pelanggan}')
    else:
        print('  (No records)')
