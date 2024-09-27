from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json
from urllib.parse import urlparse, parse_qs

class CommandHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters from the URL
        query_components = parse_qs(urlparse(self.path).query)
        
        # Check if the "command" parameter exists
        if 'command' in query_components:
            # Get the command from the query string
            command = query_components['command'][0]
            
            try:
                # Run the command and capture the output
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                
                # Prepare the response as JSON
                response = {
                    "command": command,
                    "output": output
                }
                
                # Send a 200 OK response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # Write the JSON response
                self.wfile.write(json.dumps(response).encode())
            except subprocess.CalledProcessError as e:
                # Handle the error if the command fails
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # Prepare the error response
                response = {
                    "error": "Command execution failed",
                    "command": command,
                    "output": e.output
                }
                
                # Write the error response
                self.wfile.write(json.dumps(response).encode())
        else:
            # If the "command" parameter is not present, return a 400 Bad Request
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Write an error message in JSON
            response = {
                "error": "Missing 'command' parameter"
            }
            self.wfile.write(json.dumps(response).encode())

# Define the server address and port
server_address = ('', 8080)  # Listen on all interfaces, port 8080

# Create the HTTP server
httpd = HTTPServer(server_address, CommandHTTPRequestHandler)

# Start the server
print("Server started on port 8080...")
httpd.serve_forever()
