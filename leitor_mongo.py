from pymongo import MongoClient
from urllib.parse import quote_plus
import pprint  # Biblioteca para imprimir JSON "bonito" (Pretty Print)

# --- CONFIGURAÇÕES ---
IP_DO_SERVIDOR = "168.138.159.118"
PORTA = 27017

# Credenciais
USUARIO_RAW = "root"
SENHA_RAW = "@Senai2026"  # <--- COLOCAR SENHA CORRETA

# Tratamento da senha
USUARIO = quote_plus(USUARIO_RAW)
SENHA = quote_plus(SENHA_RAW)
URI = f"mongodb://{USUARIO}:{SENHA}@{IP_DO_SERVIDOR}:{PORTA}/?authSource=admin"

try:
    print("🔌 Conectando para ler dados...")
    client = MongoClient(URI, serverSelectionTimeoutMS=5000)
    
    # Seleciona o Banco e a Coleção (Tabela)
    db = client["iot_db"]
    colecao = db["sensor_direto"] 

    # --- 1. CONTAGEM TOTAL ---
    total = colecao.count_documents({})
    print(f"\n📊 TOTAL DE REGISTROS NO BANCO: {total}")
    print("-" * 50)

    # --- 2. LER OS ÚLTIMOS 5 REGISTROS ---
    print("🕒 ÚLTIMAS 5 LEITURAS (Mais novas primeiro):")
    
    # .find() = busca tudo
    # .sort("_id", -1) = ordena decrescente (do mais novo pro mais velho)
    # .limit(5) = pega só 5
    cursor = colecao.find().sort("_id", -1).limit(5)

    for documento in cursor:
        # pprint deixa o JSON legível com indentação
        pprint.pprint(documento)
        print("-" * 20)

    # --- 3. EXEMPLO DE FILTRO (QUERY) ---
    sensor_alvo = "cozinha"
    print(f"\n🔎 BUSCANDO APENAS SENSOR: '{sensor_alvo}' (Último registro)")
    
    filtro = {"sensor": sensor_alvo}
    dado_especifico = colecao.find_one(filtro, sort=[("_id", -1)])
    
    if dado_especifico:
        pprint.pprint(dado_especifico)
    else:
        print("Nenhum dado encontrado para esse sensor.")

except Exception as e:
    print(f"❌ Erro ao ler: {e}")