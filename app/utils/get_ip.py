import socket
import urllib.request

def get_public_ip():
    try:
        external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        return external_ip
    except:
        return None

def get_local_ip():
    try:
        # Intento 1: conectar a un destino conocido (no envía datos)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        try:
            # Intento 2: usa el nombre del host
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return ip
        except:
            # Si todo falla, usa localhost
            return "127.0.0.1"
        
        
