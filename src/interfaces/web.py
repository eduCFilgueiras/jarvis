import asyncio
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Event, Lock, Thread
from urllib.parse import urlparse

from src.core.jarvis import Jarvis


class ControlState:
    def __init__(self) -> None:
        self.status = "idle"
        self.transcript = ""
        self.response = ""
        self.events: list[str] = []
        self.cancel = Event()
        self.lock = Lock()

    def snapshot(self) -> dict[str, object]:
        with self.lock:
            return {
                "status": self.status,
                "transcript": self.transcript,
                "response": self.response,
                "events": list(self.events[-20:]),
            }

    def update(self, status: str, event: str | None = None) -> None:
        with self.lock:
            self.status = status
            if event:
                self.events.append(event)


class ControlServer:
    def __init__(self, jarvis: Jarvis | None = None) -> None:
        self.jarvis = jarvis or Jarvis()
        self.state = ControlState()

    def serve(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        server = ThreadingHTTPServer((host, port), self._handler())
        print(f"Jarvis web: http://{host}:{port}")
        server.serve_forever()

    def _handler(self):
        control = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                path = urlparse(self.path).path
                if path == "/api/status":
                    self._json(control.state.snapshot())
                elif path == "/":
                    self._html()
                else:
                    self.send_error(404)

            def do_POST(self) -> None:
                path = urlparse(self.path).path
                if path == "/api/stop":
                    control.state.cancel.set()
                    control.state.update("stopped", "Execucao cancelada pelo usuario")
                    self._json({"ok": True})
                    return
                if path != "/api/process":
                    self.send_error(404)
                    return
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length) or b"{}")
                message = str(payload.get("message", "")).strip()
                if not message:
                    self._json({"error": "Informe uma mensagem."}, 400)
                    return
                control.state.cancel.clear()
                control.state.transcript = message
                control.state.response = ""
                control.state.update("processing", f"Processando: {message}")
                Thread(target=self._process, args=(message,), daemon=True).start()
                self._json({"ok": True})

            def _process(self, message: str) -> None:
                async def run() -> None:
                    if control.state.cancel.is_set():
                        return
                    response = await control.jarvis.process_message(message)
                    if control.state.cancel.is_set():
                        return
                    control.state.response = response
                    control.state.update("idle", "Resposta concluida")

                try:
                    asyncio.run(run())
                except Exception as error:
                    control.state.update("error", f"Erro: {error}")

            def _json(self, payload: dict[str, object], status: int = 200) -> None:
                body = json.dumps(payload, ensure_ascii=False).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _html(self) -> None:
                body = _PAGE.encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args) -> None:
                return

        return Handler


_PAGE = """<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Jarvis Control</title>
<style>body{font:16px system-ui;margin:0;background:#101418;color:#edf2f7}main{max-width:860px;margin:auto;padding:28px}.panel{border:1px solid #33404d;border-radius:8px;padding:16px;margin:14px 0;background:#171d23}textarea{width:100%;box-sizing:border-box;background:#0d1115;color:white;padding:10px;border:1px solid #465563;border-radius:6px;font:inherit}button{padding:10px 16px;border:0;border-radius:6px;background:#3c8df6;color:white;font:inherit;margin:10px 8px 0 0}.stop{background:#bd3e4d}.value{white-space:pre-wrap;min-height:48px}.events{white-space:pre-wrap;font:13px monospace;color:#aab6c2}.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:650px){.grid{grid-template-columns:1fr}}</style>
<main><h1>Jarvis Control</h1><p>Painel local de observabilidade</p><div class="panel"><b>Status: </b><span id="status">idle</span><br><button id="send-button" type="button">Enviar</button><button id="stop-button" type="button" class="stop">Parar</button><textarea id="message" rows="3" placeholder="Mensagem para o Jarvis"></textarea></div><div class="grid"><div class="panel"><h3>Transcricao</h3><div id="transcript" class="value">-</div></div><div class="panel"><h3>Resposta</h3><div id="response" class="value">-</div></div></div><div class="panel"><h3>Eventos</h3><div id="events" class="events">-</div></div></main>
<script>const $=id=>document.getElementById(id);function showError(error){$('events').textContent='Erro no painel: '+error;}$('send-button')?.addEventListener('click',sendMessage);$('stop-button')?.addEventListener('click',stopRun);async function sendMessage(){const message=$('message').value.trim();if(!message)return;try{await fetch('/api/process',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});$('message').value='';await refresh();}catch(error){showError(error)}}async function stopRun(){try{await fetch('/api/stop',{method:'POST'});await refresh();}catch(error){showError(error)}}async function refresh(){try{const response=await fetch('/api/status',{cache:'no-store'});const state=await response.json();for(const key of ['status','transcript','response','events'])$(key).textContent=key==='events'?state[key].join('\n')||'-':state[key]||'-';}catch(error){showError(error)}}setInterval(refresh,700);refresh()</script>"""
