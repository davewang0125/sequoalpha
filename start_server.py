#!/usr/bin/env python3
import http.server
import socketserver
import os

# Change to the current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create server
PORT = 5000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    print(f"Current directory: {os.getcwd()}")
    print("Press Ctrl+C to stop the server")
    httpd.serve_forever()
