import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "message": "🚀 T-SQL Desafios API está funcionando!",
            "endpoints": {
                "cron_job": "/api/cron-desafio",
                "test": "/api/test"
            },
            "cron_schedule": "Todos os dias às 8h (0 8 * * *)",
            "status": "active"
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))
