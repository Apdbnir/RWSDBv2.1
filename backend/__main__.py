"""
RWSDBv2.1 - Railway Station Database System v2.1
HTTP Server Entry Point
"""
from server import run_server, load_config
import sys

def start_application():
    """Start the RWSDBv2.1 HTTP server"""
    print("Starting RWSDBv2.1 HTTP Server...")

    # Get port from config
    cfg = load_config()
    port = cfg.get('port', 8080)

    run_server(port)

if __name__ == "__main__":
    start_application()