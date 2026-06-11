from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import shutil
import os

class DiskSpaceHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/disk':
            try:
                # Query disk usage for the /downloads mount
                total, used, free = shutil.disk_usage("/downloads")
                data = {
                    "total": total,
                    "used": used,
                    "free": free
                }
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/delete-files':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                req_data = json.loads(post_data.decode('utf-8'))
                file_paths = req_data.get("files", [])
                
                deleted_paths = []
                errors = []
                
                for path in file_paths:
                    if not path:
                        continue
                        
                    # Security checks: ensure path starts with /downloads
                    # Normalizing path
                    normalized = os.path.abspath(path)
                    downloads_dir = os.path.abspath("/downloads")
                    
                    if not normalized.startswith(downloads_dir):
                        errors.append(f"Forbidden path: {path}")
                        continue
                        
                    if os.path.exists(path):
                        try:
                            if os.path.isdir(path):
                                shutil.rmtree(path)
                                deleted_paths.append(path)
                            else:
                                os.remove(path)
                                deleted_paths.append(path)
                                
                                # Clean up parent directory if empty (and not /downloads itself)
                                parent = os.path.dirname(path)
                                if parent != downloads_dir and parent.startswith(downloads_dir + "/") and os.path.exists(parent) and not os.listdir(parent):
                                    shutil.rmtree(parent)
                                    deleted_paths.append(parent)
                        except Exception as file_err:
                            errors.append(f"Error deleting {path}: {str(file_err)}")
                            
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({
                    "deleted": deleted_paths,
                    "errors": errors
                }).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8080):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, DiskSpaceHandler)
    print(f"Starting disk space API on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
