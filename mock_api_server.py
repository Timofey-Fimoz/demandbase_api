
import http.server
import socketserver
import urllib.parse

PORT = 8080

class VulnerableAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/v3/ip.json"):
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            callback = query_components.get("callback", ["_dmd"])[0]
            key = query_components.get("key", [""])[0]

            # This is where the vulnerability lies.
            # The server reflects the raw 'callback' and 'key' parameters in the response.
            # An attacker can inject script content into these parameters.
            
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.end_headers()
            
            response_body = f'/**/{callback}({{"access_type":"simulated","audience":"User","registry_company_name":"Local Mock Server","key":"{key}"}})'
            
            self.wfile.write(response_body.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

with socketserver.TCPServer(("", PORT), VulnerableAPIHandler) as httpd:
    print(f"Mock API server listening on port {PORT}")
    print(f"To start, run: python3 /home/qenmity/xss_demonstration/mock_api_server.py")
    print("To test the vulnerable client, open a browser to http://localhost:8080/vulnerable_client/index.html after starting a simple web server in that directory.")
    httpd.serve_forever()
