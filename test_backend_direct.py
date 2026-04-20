import json
import urllib.request

body = json.dumps({
    'code': 'x = 1',
    'language': 'securelang'
}).encode('utf-8')

req = urllib.request.Request(
    'http://127.0.0.1:5000/api/analyze',
    data=body,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print('STATUS:', r.status)
        response = r.read().decode()
        print('RESPONSE:', response[:500])
except urllib.error.HTTPError as e:
    print('HTTP ERROR STATUS:', e.code)
    print('ERROR RESPONSE:', e.read().decode())
except Exception as e:
    print('EXCEPTION:', e)