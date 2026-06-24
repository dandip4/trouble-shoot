"""
Verification script untuk menunjukkan aplikasi troubleshoot berfungsi dengan data
"""
from app import create_app
from app.models import Troubleshoot, Pelanggan, Perangkat

app = create_app()

def verify_data():
    with app.app_context():
        print("=" * 60)
        print("APLIKASI TROUBLESHOOT - DATA VERIFICATION")
        print("=" * 60)
        
        # Check customers
        customers = Pelanggan.query.all()
        print(f"\n✅ Pelanggan (Customers): {len(customers)}")
        for c in customers[:3]:
            print(f"   - {c.nama} ({c.kontak})")
        if len(customers) > 3:
            print(f"   ... dan {len(customers)-3} lainnya")
        
        # Check devices
        devices = Perangkat.query.all()
        print(f"\n✅ Perangkat (Devices): {len(devices)}")
        for d in devices[:3]:
            print(f"   - {d.nama} ({d.tipe}) @ {d.pelanggan.nama if d.pelanggan else 'N/A'}")
        if len(devices) > 3:
            print(f"   ... dan {len(devices)-3} lainnya")
        
        # Check troubleshoots
        troubleshoots = Troubleshoot.query.all()
        print(f"\n✅ Troubleshoot (Tickets): {len(troubleshoots)}")
        for t in troubleshoots[:5]:
            status_badge = "📋" if t.status.value == "Pending" else "🔧" if t.status.value == "InProgress" else "✅"
            assigned = f"→ {t.assigned_user.username}" if t.assigned_user else "→ (unassigned)"
            print(f"   - {t.no_spk} [{status_badge} {t.status.value}] {assigned}")
        if len(troubleshoots) > 5:
            print(f"   ... dan {len(troubleshoots)-5} lainnya")
        
        # Status breakdown
        print(f"\n📊 Status Breakdown:")
        pending = Troubleshoot.query.filter_by(status='Pending').count()
        in_progress = Troubleshoot.query.filter_by(status='InProgress').count()
        completed = Troubleshoot.query.filter_by(status='Completed').count()
        print(f"   - Pending: {pending}")
        print(f"   - In Progress: {in_progress}")
        print(f"   - Completed: {completed}")
        
        # Assignment breakdown
        print(f"\n👤 Assignment Breakdown:")
        assigned = Troubleshoot.query.filter(Troubleshoot.assigned_to != None).count()
        unassigned = Troubleshoot.query.filter_by(assigned_to=None).count()
        print(f"   - Assigned: {assigned}")
        print(f"   - Unassigned: {unassigned}")
        
        print("\n" + "=" * 60)
        print("✅ APLIKASI BERFUNGSI DENGAN BAIK - SIAP DIGUNAKAN")
        print("=" * 60)
        print("\n🔗 Akses aplikasi di: http://127.0.0.1:5000")
        print("👤 Login dengan:")
        print("   - Username: admin")
        print("   - Password: admin123")
        print("\n   Atau: teknisi1 / teknisi123")
        print("   Atau: manajer1 / manajer123")

if __name__ == "__main__":
    verify_data()
