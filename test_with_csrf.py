import urllib.request
import http.cookiejar
from urllib.parse import urlencode, parse_qs
import re

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# Step 1: Get login page and extract CSRF token
print('Step 1: Get login page...')
resp = opener.open('http://127.0.0.1:5000/auth/login')
html = resp.read().decode('utf-8')

# Extract CSRF token
csrf_match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', html)
if csrf_match:
    csrf_token = csrf_match.group(1)
    print(f'✓ CSRF token found: {csrf_token[:20]}...')
else:
    print('✗ CSRF token not found')
    csrf_token = None

# Step 2: Login with CSRF token
print('\nStep 2: Login with CSRF token...')
login_data = {
    'username': 'admin',
    'password': 'admin123',
}
if csrf_token:
    login_data['csrf_token'] = csrf_token

login_encoded = urlencode(login_data).encode('utf-8')
resp = opener.open('http://127.0.0.1:5000/auth/login', login_encoded)
print(f'✓ Login response: {resp.status}')

# Step 3: Access troubleshoot list
print('\nStep 3: Access troubleshoot list...')
resp = opener.open('http://127.0.0.1:5000/troubleshoot/')
html = resp.read().decode('utf-8')

print(f'✓ Troubleshoot page: {resp.status}')
print(f'✓ Page length: {len(html)} chars')

# Check for data
spk_count = html.count('<td>SPK-')
print(f'✓ SPK records found: {spk_count}')

if spk_count > 0:
    print('\n✅ SUCCESS - Data is displaying in the application!')
    # Show first SPK
    match = re.search(r'<td>(SPK-\d+-\d+)</td>', html)
    if match:
        print(f'✓ First ticket: {match.group(1)}')
else:
    print('\n❌ No SPK data found')
    print('Checking for "Tidak ada data":')
    print(f'  Found: {"Tidak ada data" in html}')
