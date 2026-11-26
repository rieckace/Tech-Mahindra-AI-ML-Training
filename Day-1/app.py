"""Local web interface using the Python standard library only."""
import argparse
import csv
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from dataclasses import asdict
from decision import REQUIREMENTS, Requirement, classify, lifecycle, export_reports, report_rows

ROOT = Path(__file__).resolve().parent

def payload(r):
    return {'requirement': asdict(r), 'decision': asdict(classify(r)), 'lifecycle': lifecycle(r)}

class Handler(BaseHTTPRequestHandler):
    def send(self, body, kind, status=200, filename=None):
        self.send_response(status); self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(body)))
        if filename: self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
        self.end_headers(); self.wfile.write(body)

    def json_response(self, value, status=200):
        self.send(json.dumps(value).encode(), 'application/json; charset=utf-8', status)

    def do_GET(self):
        if self.path == '/':
            self.send((ROOT/'index.html').read_bytes(), 'text/html; charset=utf-8')
        elif self.path == '/api/demo': self.json_response([payload(r) for r in REQUIREMENTS])
        elif self.path in ('/report.csv','/lifecycle.csv'):
            name = 'decision_report.csv' if self.path == '/report.csv' else 'lifecycle_map.csv'
            self.send((ROOT/'reports'/name).read_bytes(), 'text/csv; charset=utf-8', filename=name)
        else: self.json_response({'error':'Not found'}, 404)

    def do_POST(self):
        if self.path != '/api/classify':
            self.json_response({'error':'Not found'}, 404); return
        try:
            size = int(self.headers.get('Content-Length','0'))
            if not 0 < size <= 16384: raise ValueError('Invalid request size.')
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict): raise ValueError('Expected a JSON object.')
            self.json_response(payload(Requirement(**data)))
        except (ValueError, TypeError) as e: self.json_response({'error':str(e)}, 400)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-only', action='store_true')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    rows = export_reports(REQUIREMENTS, ROOT/'reports')
    for row in rows: print(f"{row['decision']:22} | {row['requirement']}")
    print('Reports written to reports/')
    if not args.report_only:
        with ThreadingHTTPServer(('127.0.0.1', args.port), Handler) as server:
            print(f'Open http://127.0.0.1:{args.port} (Ctrl+C to stop)')
            try: server.serve_forever()
            except KeyboardInterrupt: pass

if __name__ == '__main__': main()
