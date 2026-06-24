from app import create_app
from app.models import User
from flask_login import LoginManager
from werkzeug.security import check_password_hash

app = create_app()

# Test direct login
with app.test_client() as client:
    # Step 1: Get login page
    resp = client.get('/auth/login')
    print(f'Step 1 - Get login page: {resp.status_code}')
    
    # Step 2: Post login
    resp = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    print(f'Step 2 - Login POST: {resp.status_code}')
    print(f'  Redirected to: {resp.request.path}')
    
    # Step 3: Check dashboard
    resp = client.get('/dashboard')
    print(f'Step 3 - Dashboard: {resp.status_code}')
    print(f'  Contains "Total Data": {"Total Data" in resp.data.decode()}')
    
    # Step 4: Check troubleshoot list
    resp = client.get('/troubleshoot/')
    html = resp.data.decode()
    print(f'Step 4 - Troubleshoot list: {resp.status_code}')
    print(f'  Page length: {len(html)}')
    print(f'  Contains "SPK-": {"SPK-" in html}')
    print(f'  Contains "Tidak ada data": {"Tidak ada data" in html}')
    
    # Check tbody
    if '<tbody>' in html:
        tbody_start = html.find('<tbody>')
        tbody_end = html.find('</tbody>') + 8
        tbody = html[tbody_start:tbody_end]
        rows = tbody.count('<tr>')
        print(f'  Table rows: {rows}')
        if rows > 1:
            # Show first row
            first_row = tbody[tbody.find('<tr'):tbody.find('</tr>')+5]
            print(f'  First row preview: {first_row[:100]}')
