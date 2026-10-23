import json
import threading
import urllib.error
import urllib.request

import pytest

from app.assistant import Assistant
from app.server import serve


@pytest.fixture
def assistant():
    return Assistant()


@pytest.fixture
def live_server():
    a = Assistant()
    srv = serve(a, port=0)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    yield base, a
    srv.shutdown()


def http(method, url, payload=None, raw=None):
    data = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())
