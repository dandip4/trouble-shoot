from app import create_app
from app.models import Troubleshoot
from app.models.troubleshoot import KategoriClusterEnum, JenisTroubleEnum, PerangkatEnum

app = create_app()

with app.app_context():
    # Test basic query
    all_troubles = Troubleshoot.query.all()
    print(f"Total records: {len(all_troubles)}")
    
    if all_troubles:
        t = all_troubles[0]
        print(f"\nFirst record:")
        print(f"  no_spk: {t.no_spk}")
        print(f"  kategori_cluster: {t.kategori_cluster} (type: {type(t.kategori_cluster)})")
        print(f"  jenis_trouble: {t.jenis_trouble} (type: {type(t.jenis_trouble)})")
        print(f"  perangkat: {t.perangkat} (type: {type(t.perangkat)})")
        print(f"  created_at: {t.created_at}")
        
        # Test enum filtering
        print(f"\nEnum comparison tests:")
        print(f"  KategoriClusterEnum.Ringan = {KategoriClusterEnum.Ringan}")
        print(f"  t.kategori_cluster == KategoriClusterEnum.Ringan: {t.kategori_cluster == KategoriClusterEnum.Ringan}")
        
        # Test direct filters
        print(f"\nDirect filter tests:")
        ringan_count = Troubleshoot.query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Ringan).count()
        print(f"  Ringan count: {ringan_count}")
        
        sedang_count = Troubleshoot.query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sedang).count()
        print(f"  Sedang count: {sedang_count}")
        
        berat_count = Troubleshoot.query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Berat).count()
        print(f"  Berat count: {berat_count}")
        
        total_by_kategori = ringan_count + sedang_count + berat_count
        print(f"  Total by kategori: {total_by_kategori}")
