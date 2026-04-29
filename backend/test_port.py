import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind(('0.0.0.0', 6767))
    print('Port 6767 is available!')
    s.close()
except Exception as e:
    print(f'Port error: {e}')