import json
import urllib.request
import urllib.error

body = json.dumps({
    'code': 'def foo() { x = 1 return x }',
    'language': 'securelang'
}).encode('utf-8')

req = urllib.request.Request(
    'http://127.0.0.1:5000/api/analyze',
    data=body,
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print(r.status)
        print(r.read().decode())
except urllib.error.HTTPError as e:
    print('STATUS', e.code)
    print(e.read().decode())
except Exception as e:
    print('ERR', e)
