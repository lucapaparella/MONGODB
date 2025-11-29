from pymongo import MongoClient
from urllib.parse import quote_plus
import time
import random
import datetime

# --- CONFIGURAÇÕES DO BANCO ---
IP_DO_SERVIDOR = "168.138.159.118" # Ex: 168.138...
PORTA = 27017

# Suas credenciais do Mongo
USUARIO_RAW = "root"
SENHA_RAW = "@Senai2026"

# Tratamento da senha (para evitar erro com caracteres especiais)
USUARIO = quote_plus(USUARIO_RAW)
SENHA = quote_plus(SENHA_RAW)

# String de conexão direta
URI = f"mongodb://{USUARIO}:{SENHA}@{IP_DO_SERVIDOR}:{PORTA}/?authSource=admin"

# --- CONFIGURAÇÃO DA SIMULAÇÃO ---
LOCAIS = ["sala_estar", "cozinha", "garagem"]

try:
    print(f"🔌 Conectando ao MongoDB em {IP_DO_SERVIDOR}...")
    client = MongoClient(URI, serverSelectionTimeoutMS=5000)
    
    # Teste rápido de conexão
    client.server_info()
    print("✅ Conexão estabelecida com sucesso!")

    # Seleciona Banco e Coleção
    db = client["iot_db"]
    colecao = db["sensor_direto"] # Nome da tabela nova

    print("🚀 Iniciando envio direto de dados (Loop)...")
    
    while True:
        # 1. Gera dados
        local = random.choice(LOCAIS)
        temp = round(random.uniform(18.0, 32.0), 1)
        hum = random.randint(30, 90)
        
        # 2. Cria o documento (JSON)
        pacote_dados = {
            "sensor": local,
            "temperatura": temp,
            "umidade": hum,
            "metodo": "conexao_direta", # Marcamos que veio sem MQTT
            "data_hora": datetime.datetime.now()
        }

        # 3. Grava direto no banco
        resultado = colecao.insert_one(pacote_dados)
        
        print(f"[GRAVADO] ID: {resultado.inserted_id} | {local}: {temp}°C")

        # Espera 3 segundos
        time.sleep(3)

except KeyboardInterrupt:
    print("\n🛑 Parando script...")
except Exception as e:
    print(f"\n❌ ERRO CRÍTICO: {e}")
    print("DICA: Verifique se a porta 27017 está liberada no Firewall da Oracle/AWS.")