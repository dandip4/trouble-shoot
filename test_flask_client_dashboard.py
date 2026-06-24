from app import create_app

app = create_app()

with app.test_client() as client:
    # Login as admin
    resp = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    
    print(f"Login response: {resp.status_code}")
    
    # Go to dashboard
    resp = client.get('/dashboard')
    html = resp.data.decode()
    
    # Extract Total Data Troubleshoot value
    import re
    match = re.search(r'Total Data Troubleshoot</[^>]*>.*?<[^>]*>(\d+)</[^>]*>', html, re.DOTALL)
    if match:
        total = match.group(1)
        print(f"Total Data Troubleshoot: {total}")
    else:
        # Try alternative pattern
        if '<td>0</td>' in html:
            print("Found 0 in table")
        if 'Total' in html:
            print("Found 'Total' in page")
            # Show context
            idx = html.find('Total Data Troubleshoot')
            if idx != -1:
                print(f"Context: ...{html[idx:idx+200]}...")
