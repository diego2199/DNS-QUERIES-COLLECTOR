#librerias
import requests
import re
from collections import Counter
from datetime import datetime
#constantes
LUMU_CLIENT_KEY = "d39a0f19-7278-4a64-a255-b7646d1ace80"
COLLECTOR_ID = "5ab55d08-ae72-4017-a41c-d9d735360288"
API_URL = f"https://api.lumu.io/collectors/{COLLECTOR_ID}/dns/queries?key={LUMU_CLIENT_KEY}"
#funciones
def parse_log(file_path): #funcion para organizar la informacion
    client_ips = []
    hosts = []
    timestamps = []
    with open(file_path, 'r') as file:
        for line in file:
            #print("linea del archivo:",repr(line),"\n") #para saber como recopilaba la informacion.
            # Usar regex para extraer IP del cliente, el host consultado y el timestamp
            timestamp_match = re.search(r'(\d{1,2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2}:\d{2}\.\d{3})', line) 
            ip_match = re.search(r'client .* (\d+\.\d+\.\d+\.\d+)', line)
            host_match = re.search(r'query: (\S+)', line)
            if timestamp_match and ip_match and host_match:
                # Convertir la fecha y hora al formato ISO 8601
                timestamp_iso = convert_to_iso(timestamp_match.group(1))
                timestamps.append(timestamp_iso)
                client_ips.append(ip_match.group(1))
                hosts.append(host_match.group(1))
            else:
                print("No se encontró una coincidencia en la línea:", line)
    return timestamps, client_ips, hosts

def convert_to_iso(timestamp_str): #funcion para convertir la fecha al formato necesario
    # Parsear la fecha usando el formato específico
    dt = datetime.strptime(timestamp_str, '%d-%b-%Y %H:%M:%S.%f')
    # Convertir a ISO 8601
    return dt.isoformat() + "Z"

def send_data_in_chunks(data): #funcion envio de datos 
    for i in range(0, len(data), 500):
        chunk = data[i:i+500]
        response = requests.post(API_URL, json=chunk)
        if response.status_code != 200:
            print("Error sending data:", response.status_code, response.text)

def generate_statistics(client_ips, hosts): #funcion para generar las estadisticas requeridas
    total_records = len(client_ips)
   
    # Contar y ordenar IPs y Hosts
    ip_count = Counter(client_ips).most_common()
    host_count = Counter(hosts).most_common()

    print(f"Total records {total_records}")
    print("\nClient IPs Rank")
    print("--------------- --- -----")
    for ip, count in ip_count:
        percentage = (count / total_records) * 100
        print(f"{ip: <15} {count: <5} {percentage:.2f}%")

    print("\nHost Rank")
    print("------------------------------------------------------------ --- -----")
    for host, count in host_count:
        percentage = (count / total_records) * 100
        print(f"{host: <60} {count: <5} {percentage:.2f}%")

def main(file_path): #funcion principal del programa
    timestamps, client_ips, hosts = parse_log(file_path)
    data = [{
        "client_ip": ip,
        "host": host,
        "timestamp": timestamp  # Usar el timestamp extraído del log
    } for timestamp, ip, host in zip(timestamps, client_ips, hosts)]
    send_data_in_chunks(data)
    generate_statistics(client_ips, hosts)

if __name__ == "__main__": #condicional para asegurar que lleguen los datos correspondientes
    import sys
    if len(sys.argv) < 2:
        print("Usage: py script.py queries")
    else:
        main(sys.argv[1])