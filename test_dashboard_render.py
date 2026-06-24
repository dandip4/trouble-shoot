"""
Test: Dashboard rendering via Flask test client
"""
from app import create_app
import re

app = create_app()

with app.test_client() as client:
    print("=" * 60)
    print("TEST: DASHBOARD RENDERING")
    print("=" * 60)
    
    # Login as admin
    print("\n1️⃣  Logging in as admin...")
    resp = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    
    print(f"   Status: {resp.status_code}")
    print(f"   Redirected to: {resp.request.path}")
    
    # Get dashboard
    print("\n2️⃣  Fetching dashboard...")
    resp = client.get('/dashboard')
    html = resp.data.decode()
    
    print(f"   Status: {resp.status_code}")
    print(f"   Page length: {len(html)} chars")
    
    # Look for specific data points
    print("\n3️⃣  Checking dashboard content...")
    
    # Check for total data
    print("\n   Searching for 'Total Data Troubleshoot'...")
    if 'Total Data Troubleshoot' in html:
        print("   ✓ Found heading")
        # Try to extract value
        match = re.search(r'<h1[^>]*>([\d]+)</h1>', html)
        if match:
            value = match.group(1)
            print(f"   Found value: {value}")
        else:
            # Try alternative patterns
            total_match = re.search(r'Total Data Troubleshoot.*?<[^>]*>(\d+)', html, re.DOTALL)
            if total_match:
                print(f"   Found (alt pattern): {total_match.group(1)}")
            else:
                print("   Could not extract number")
                # Show context
                idx = html.find('Total Data Troubleshoot')
                print(f"   Context: ...{html[idx:idx+300]}...")
    else:
        print("   ✗ Heading NOT found")
    
    # Look for test records
    print("\n   Searching for TEST records in page...")
    test_found = html.count('SPK-TEST')
    print(f"   Test records found: {test_found}")
    
    if test_found > 0:
        print("   ✓ TEST data renders in page!")
    
    # Look for any SPK records
    print("\n   Searching for any SPK records...")
    spk_count = html.count('SPK-')
    print(f"   SPK references: {spk_count}")
    
    # Check tables
    print("\n   Checking for tables...")
    if '<table' in html:
        print("   ✓ Table found")
        if '<tbody>' in html:
            tbody_start = html.find('<tbody>')
            tbody_end = html.find('</tbody>')
            tbody_html = html[tbody_start:tbody_end]
            row_count = tbody_html.count('<tr>')
            print(f"   Table rows: {row_count}")
        else:
            print("   ✗ No tbody found")
    else:
        print("   ✗ No table found")
    
    # Check for metrics cards
    print("\n   Checking metric cards...")
    metrics = {
        'Ringan': html.count('Kategori Ringan'),
        'Sedang': html.count('Kategori Sedang'),
        'Berat': html.count('Kategori Berat'),
    }
    for metric, count in metrics.items():
        print(f"   {metric}: {count}")
    
    print("\n" + "=" * 60)
    print("Saving HTML to file for inspection...")
    with open('dashboard_output.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Saved to dashboard_output.html")
