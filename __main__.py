"""
RWSDBv2.1 - Railway Station Database System v2.1
HTTP Server Entry Point
"""
from server import run_server
import sys

def start_application():
    """Start the RWSDBv2.1 HTTP server"""
    print("Starting RWSDBv2.1 HTTP Server...")

    # Determine port from command line arguments or use default
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number '{sys.argv[1]}', using default port {port}")

    run_server(port)

if __name__ == "__main__":
    start_application()