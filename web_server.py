#!/usr/bin/env python3
"""
Simple HTTP server to serve the chatbot web interface
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def start_web_server(port=3000):
    """Start the web server."""
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🌐 Web server starting on http://localhost:{port}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print(f"🤖 Chatbot interface: http://localhost:{port}/chatbot_web.html")
            print("=" * 60)
            print("📋 Instructions:")
            print("1. Make sure your FastAPI server is running on http://localhost:8000")
            print("2. Open http://localhost:3000/chatbot_web.html in your browser")
            print("3. Start chatting with your PRMSU chatbot!")
            print("=" * 60)
            print("Press Ctrl+C to stop the server")
            print()
            
            # Auto-open browser after a short delay
            def open_browser():
                time.sleep(2)
                webbrowser.open(f'http://localhost:{port}/chatbot_web.html')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Web server stopped!")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Trying port {port + 1}...")
            start_web_server(port + 1)
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    print("🚀 Starting PRMSU Chatbot Web Interface...")
    start_web_server()
