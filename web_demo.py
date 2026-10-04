"""Local seminar UI; Python standard library only."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, shutil, subprocess, sys, tempfile, webbrowser
ROOT=Path(__file__).resolve().parent
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/': self.send_error(404); return
        data=(ROOT/'index.html').read_bytes()
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.end_headers(); self.wfile.write(data)
    def do_POST(self):
        if self.path != '/run': self.send_error(404); return
        try:
            data=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
            patch=data['patch']; expanded=data.get('expanded',False)
            if patch not in ['baseline','regression','partial','fixed']: raise ValueError('Invalid patch')
            events=[]
            with tempfile.TemporaryDirectory(prefix='seminar_visual_') as tmp:
                work=Path(tmp); shutil.copy(ROOT/'calculator.py',work/'calculator.py'); shutil.copytree(ROOT/'tests',work/'tests',ignore=shutil.ignore_patterns('__pycache__'))
                events.append(dict(title='1. Chuẩn bị repository',status='PASS',detail='Đã sao chép code và tests vào thư mục tạm.'))
                diff='Không áp dụng patch — chạy code ban đầu.'
                if patch!='baseline':
                    diff=(ROOT/'patches'/f'{patch}.diff').read_text()
                    for flags in (['--check'],[]):
                        r=subprocess.run(['git','apply',*flags,str(ROOT/'patches'/f'{patch}.diff')],cwd=work,capture_output=True,text=True,timeout=15)
                        if r.returncode: raise RuntimeError(r.stderr)
                events.append(dict(title='2. Áp dụng patch',status='PASS',detail=diff))
                groups=[('FAIL_TO_PASS','tests.test_issue'),('PASS_TO_PASS','tests.test_regression')]
                if expanded: groups.append(('TEST BỔ SUNG','tests.test_extra'))
                for label,module in groups:
                    r=subprocess.run([sys.executable,'-m','unittest','-v',module],cwd=work,capture_output=True,text=True,timeout=15)
                    events.append(dict(title=label,status='PASS' if r.returncode==0 else 'FAIL',detail=r.stdout+r.stderr))
                response=dict(events=events,code=(work/'calculator.py').read_text(),resolved=all(e['status']=='PASS' for e in events),patch=patch)
        except Exception as e: response=dict(error=str(e))
        payload=json.dumps(response,ensure_ascii=False).encode()
        self.send_response(200); self.send_header('Content-Type','application/json; charset=utf-8'); self.end_headers(); self.wfile.write(payload)
if __name__=='__main__':
    port=int(sys.argv[1]) if len(sys.argv)>1 else 8765
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    print(f'Mở http://127.0.0.1:{port} | Ctrl+C để dừng',flush=True)
    webbrowser.open(f'http://127.0.0.1:{port}')
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
