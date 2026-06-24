import urllib.request
import http.cookiejar
from urllib.parse import urlencode

# Create cookie jar for session
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Get login page
try:
    opener.open('http://127.0.0.1:5000/auth/login')
    print('✓ Login page accessed')
except Exception as e:
    print(f'Error accessing login page: {e}')
    exit(1)

# Login
try:
    login_data = urlencode({'username': 'admin', 'password': 'admin123'}).encode('utf-8')
    opener.open('http://127.0.0.1:5000/auth/login', login_data)
    print('✓ Login POST sent')
except Exception as e:
    print(f'Error during login: {e}')

# Access troubleshoot
try:
    resp = opener.open('http://127.0.0.1:5000/troubleshoot/')
    html = resp.read().decode('utf-8')
    print(f'✓ Troubleshoot page status: 200')
    print(f'✓ Page content length: {len(html)} chars')
    
    has_spk = 'SPK-' in html
    spk_count = html.count('SPK-')
    
    print(f'✓ SPK records found: {has_spk}')
    print(f'✓ Number of SPK references: {spk_count}')
    
    if has_spk:
        print('\n✅ SUCCESS - Data is displaying!')
        # Show first SPK found
        start = html.find('SPK-')
        if start != -1:
            end = html.find('<', start)
            first_spk = html[start:end]
            print(f'✓ First ticket: {first_spk}')
    else:
        print('\n❌ No SPK data found')
        
except Exception as e:
    print(f'Error accessing troubleshoot: {e}')
