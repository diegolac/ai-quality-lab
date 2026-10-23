"""Servidor HTTP minimo (apenas biblioteca padrao) que expoe o assistente para testes de API e de UI."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .assistant import Assistant

PAGE = """<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Assistente Financeiro</title>
<body><h1>Assistente Financeiro</h1>
<label>Tenant <select id="tenant"><option>acme</option><option>globex</option></select></label>
<input id="q" placeholder="Pergunte algo"><button id="send">Enviar</button>
<p id="answer" role="status"></p>
<script>
document.getElementById('send').onclick = async () => {
  const r = await fetch('/api/ask', {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({tenant: document.getElementById('tenant').value,
                          question: document.getElementById('q').value})});
  const j = await r.json();
  document.getElementById('answer').textContent = j.answer;
};
</script></body></html>"""


def make_handler(assistant):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype="application/json"):
            data = body if isinstance(body, bytes) else body.encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/":
                return self._send(200, PAGE, "text/html; charset=utf-8")
            if self.path == "/health":
                return self._send(200, json.dumps({"status": "ok"}))
            self._send(404, json.dumps({"error": "not found"}))

        def do_POST(self):
            try:
                n = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(n) or b"{}")
            except ValueError:
                return self._send(400, json.dumps({"error": "json invalido"}))
            if self.path == "/api/ask":
                if not body.get("tenant") or not body.get("question"):
                    return self._send(422, json.dumps({"error": "tenant e question sao obrigatorios"}))
                res = assistant.ask(body["tenant"], body["question"], body.get("role", "employee"))
                return self._send(503 if res.get("degraded") else 200, json.dumps(res))
            self._send(404, json.dumps({"error": "not found"}))
    return H


def serve(assistant=None, port=0):
    srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(assistant or Assistant()))
    return srv


if __name__ == "__main__":
    s = serve(port=8000)
    print("http://127.0.0.1:8000")
    s.serve_forever()
