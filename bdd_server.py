from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

# Define the string to match
DESIRED_STRING = "openAI"

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters from the URL
        query_components = parse_qs(urlparse(self.path).query)
        
        # Check if the "query" parameter exists and matches the desired string
        if 'query' in query_components and query_components['query'][0] == DESIRED_STRING:
            # Get the client's IP address
            client_ip = self.client_address[0]
            
            # Prepare the response as JSON
            response = {
                "client_ip": client_ip
            }
            
            # Send a 200 OK response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Write the JSON response
            self.wfile.write(json.dumps(response).encode())
        else:
            # If the query doesn't match, return a 400 Bad Request
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Write an error message in JSON
            response = {
                "error": "Invalid query string"
            }
            self.wfile.write(json.dumps(response).encode())

# Define the server address and port
server_address = ('', 8080)  # Listen on all interfaces, port 8080

# Create the HTTP server
httpd = HTTPServer(server_address, MyHTTPRequestHandler)

# Start the server
print("Server started on port 8080...")
httpd.serve_forever()
