from pymongo import MongoClient
from urllib.parse import quote_plus  # <--- IMPORTANTE: Importar isso
import datetime

# --- CONFIGURAÇÕES ---
IP_DO_SERVIDOR = "168.138.159.118"  # Ex: 168.138...
PORTA = 27017
USUARIO = "root"
SENHA = "@Senai2026"

# --- A CORREÇÃO MÁGICA ---
# Isso converte caracteres especiais em códigos seguros (ex: @ vira %40)
USUARIO = quote_plus(USUARIO)
SENHA = quote_plus(SENHA)

# A string de conexão mágica
# authSource=admin é obrigatório quando se loga como root
uri = f"mongodb://{USUARIO}:{SENHA}@{IP_DO_SERVIDOR}:{PORTA}/?authSource=admin"

try:
    # 1. Conectar ao Banco
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # Verifica se conectou de verdade pedindo info do servidor
    client.server_info() 
    print("✅ Conectado ao MongoDB com sucesso!")

    # 2. Selecionar o Banco de Dados (se não existir, ele cria sozinho)
    db = client["iot_db"]

    # 3. Selecionar a Coleção (equivalente a Tabela)
    colecao = db["temperaturas"]

    # 4. Inserir um dado de teste
    documento = {
        "sensor": "sala_estar",
        "valor": 25.5,
        "unidade": "C",
        "data": datetime.datetime.now()
    }
    
    id_inserido = colecao.insert_one(documento).inserted_id
    print(f"💾 Documento salvo com ID: {id_inserido}")

    # 5. Ler o dado de volta para confirmar
    dado_lido = colecao.find_one({"_id": id_inserido})
    print("🔍 Dado recuperado do banco:", dado_lido)

except Exception as e:
    print(f"❌ Erro ao conectar: {e}")