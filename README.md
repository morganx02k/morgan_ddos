![Morgan DDOS Banner](https://i.postimg.cc/gXHD2NVN/banner.jpg)

# Morgan DDOS Script

Este é um script de ataque de negação de serviço distribuído (DDoS), escrito em Python, que permite realizar diferentes tipos de ataques de inundação (flood) contra servidores. O código utiliza múltiplas threads para enviar pacotes repetidos, com a possibilidade de usar proxies para mascarar a origem do tráfego.

**Importante:** O uso deste script para atacar servidores sem autorização explícita é ilegal e pode resultar em consequências legais graves. Este código é fornecido **somente para fins educacionais** e deve ser utilizado de forma responsável.

## Funcionalidades

O script oferece os seguintes tipos de ataque:

1. **UDP Flood**: Ataque que inunda o servidor com pacotes UDP, muito comum em servidores de jogos.
2. **TCP Flood**: Ataque que utiliza pacotes TCP para sobrecarregar o servidor.
3. **TCP SYN Flood**: Ataque que explora o processo de handshake TCP, consumindo recursos do servidor.
4. **DNS Flood**: Ataque que envia consultas DNS em grande quantidade, impactando servidores DNS.
5. **ICMP Flood (Ping Flood)**: Ataque que envia pacotes ICMP, também conhecidos como "ping", para saturar a rede.

## Proxy

O script oferece a opção de utilizar proxies para ocultar a origem do ataque. Quando um proxy é utilizado, o tráfego de ataque é redirecionado através de um servidor intermediário, de modo que o servidor alvo não consegue identificar de onde o ataque está realmente vindo. Isso pode ser útil em cenários onde você deseja mascarar a identidade do atacante ou evitar a detecção de sua rede de origem.

### Como Funciona o Proxy?

- **Sem Proxy**: O script envia os pacotes diretamente do seu IP para o servidor alvo.
- **Com Proxy**: O tráfego de ataque é redirecionado para o proxy, e o servidor alvo vê o IP do proxy em vez do seu IP real. Isso dificulta a identificação da origem do ataque.

## Instalação

Para rodar o script, siga os passos abaixo:

1. Clone o repositório para o seu computador:
   ```bash
   git clone https://github.com/morganx02k/morgan_ddos.git
   ```

2. Acesse a pasta do projeto:
   ```bash
   cd morgan_ddos
   ```

3. Instale as dependências:
   ```bash
   pip install psutil
   ```

4. Execute o script:
   ```bash
   python3 morgan_ddos.py
   ```

## Como Usar

1. **Digite o IP do alvo**: Você será solicitado a inserir o IP do servidor que deseja atacar.
2. **Escolha o tipo de ataque**: O script oferece cinco tipos de ataque. Você pode escolher qual deseja executar.
3. **Defina o intervalo de pacotes**: Você pode configurar o intervalo entre os pacotes enviados (em segundos).
4. **Número de threads**: O script calcula automaticamente o número ideal de threads com base no número de núcleos de CPU e memória RAM disponível. Você pode alterar o número de threads se desejar.
5. **Proxy (Opcional)**: Se desejar utilizar um proxy, insira o IP e a porta do servidor proxy no formato `IP:PORTA`.

### Exemplo de Execução

```bash
Digite o IP alvo: 192.168.1.1
Deseja usar um proxy? Se sim, insira no formato IP:Porta (ou pressione Enter para não usar): 192.168.0.2:8080
Escolha o tipo de ataque:
1. UDP Flood (Impacta servidores de jogos online como FiveM e outros que usam UDP)
2. TCP Flood (Impacta servidores Minecraft e outros serviços que usam TCP)
3. TCP SYN Flood (Explora o handshake TCP, afetando servidores web e serviços de rede)
4. DNS Flood (Impacta servidores DNS, podendo causar falhas na resolução de nomes)
5. ICMP Flood (Ping Flood - saturação através de pacotes ICMP, afeta a disponibilidade geral)
Digite o número do ataque desejado: 1
Digite o intervalo em segundos entre pacotes (ex: 0.1 para 100ms): 0.1
Digite o número de threads que deseja (ou pressione Enter para usar 1000): 100
```

## Observações Importantes

- **Legalidade**: O uso deste script contra servidores sem a devida permissão é ilegal. Certifique-se de usar este código apenas em ambientes controlados e com permissão explícita dos responsáveis pelos servidores.
- **Requisitos de Sistema**: Este script foi projetado para funcionar em sistemas com Python 3.x. Ele utiliza a biblioteca `psutil` para monitorar o sistema e otimizar o número de threads com base na capacidade do computador.
- **Impacto no Sistema**: O uso de múltiplas threads pode consumir uma grande quantidade de recursos do sistema. Certifique-se de monitorar o desempenho do seu computador enquanto o script estiver em execução.

## Contribuições

Se você deseja contribuir para este projeto, fique à vontade para enviar um pull request. Certifique-se de seguir as diretrizes de contribuições e respeitar as boas práticas de código.

## Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Aviso Legal

Este código é fornecido apenas para fins educacionais. O autor não se responsabiliza por qualquer uso indevido ou ilegal do código.

---

**Aviso:** O uso de DDoS sem autorização é crime em muitos países. O autor não apoia ou incentiva práticas ilegais.


**Just like Dexter Morgan, everyone has hidden secrets and vices that only you can know**
