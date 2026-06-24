from app import create_app
from app.models import Troubleshoot
from flask_login import current_user

app = create_app()
with app.app_context():
    # Simulate route behavior
    query = Troubleshoot.query
    print(f'Raw query count: {query.count()}')
    
    # Paginate as route does
    pagination = query.order_by(Troubleshoot.created_at.desc()).paginate(page=1, per_page=15)
    
    print(f'\nPagination object:')
    print(f'  - items count: {len(pagination.items)}')
    print(f'  - total: {pagination.total}')
    print(f'  - pages: {pagination.pages}')
    print(f'  - has_next: {pagination.has_next}')
    
    # Show first item if exists
    if pagination.items:
        t = pagination.items[0]
        print(f'\nFirst item:')
        print(f'  - no_spk: {t.no_spk}')
        print(f'  - nama_pelanggan: {t.nama_pelanggan}')
