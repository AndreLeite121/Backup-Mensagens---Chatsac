import requests
import json
import os
import time
import re
from requests.exceptions import ConnectionError, Timeout

API_TOKEN = 'Token Aqui'  # Substitua pelo seu token de API
BASE_URL = 'https://#########/chats/'

HEADERS = {
    'access-token': API_TOKEN,
    'Content-Type': 'application/json'
}

def sanitize_filename(name):
    """
    Remove caracteres inválidos para nomes de arquivos.
    """
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def gerar_html(nome_cliente, mensagens):
    """
    Gera um HTML simples para exibir as mensagens de um chat.
    """
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Conversas - {nome_cliente}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        h2 {{
            text-align: center;
        }}
        .message {{
            max-width: 60%;
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
            position: relative;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .sent {{
            background-color: #d1f5d3;
            margin-left: auto;
            text-align: right;
        }}
        .received {{
            background-color: #ffffff;
            margin-right: auto;
            text-align: left;
        }}
        .sender {{
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
        }}
        .timestamp {{
            display: block;
            font-size: 0.8em;
            color: #888;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <h2>Conversa com {nome_cliente}</h2>
"""
    for msg in mensagens:
        css_class = "sent" if msg["direcao"] == "enviada" else "received"
        html += f"""
    <div class="message {css_class}">
        <span class="sender">{msg['remetente']}</span>
        <p>{msg['texto']}</p>
        <span class="timestamp">{msg['data']}</span>
    </div>
"""
    html += """
</body>
</html>"""
    return html

def get_chat_data_with_retry(url, headers, retries=3):
    """
    Tenta buscar os dados do chat com algumas tentativas em caso de erro de conexão.
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ HTTP {response.status_code} ao buscar {url}")
                return None
        except (ConnectionError, Timeout) as e:
            print(f"⚠️ Tentativa {attempt + 1} falhou ({type(e).__name__}): {e}")
            time.sleep(1 + attempt * 2)
    print(f"❌ Falha definitiva ao buscar {url} após {retries} tentativas.")
    return None

def extrair_mensagens():
    """
    Extrai as mensagens de cada chat, salva em JSON e HTML por cliente.
    """
    with open('contacts_curchatid_Etna2076.json', 'r', encoding='utf-8') as f:
        contatos = json.load(f)

    os.makedirs("Mensagens", exist_ok=True)

    for contato in contatos:
        chat_id = contato.get("curChatId")
        if not chat_id:
            continue

        url = f"{BASE_URL}{chat_id}"
        chat_data = get_chat_data_with_retry(url, HEADERS)
        if not chat_data:
            print(f"❌ Chat {chat_id} não pôde ser carregado.")
            continue

        contact_info = chat_data.get("contact", {})
        nome_cliente = contact_info.get("name", "SemNome")
        numero_cliente = contact_info.get("number", "")

        mensagens_brutas = chat_data.get("messages", [])
        mensagens_formatadas = []

        for msg in mensagens_brutas:
            if msg.get("isDeleted") or not msg.get("text"):
                continue

            direcao = "enviada" if msg.get("isSentByMe") else "recebida"
            if direcao == "enviada":
                user_info = msg.get("user")
                remetente = user_info.get("name") if user_info and user_info.get("name") else "Operador"
            else:
                remetente = contact_info.get("name", "Cliente")

            mensagens_formatadas.append({
                "data": msg.get("dhMessage"),
                "direcao": direcao,
                "remetente": remetente,
                "texto": msg.get("text")
            })

        cliente_dir = os.path.join("Mensagens", sanitize_filename(nome_cliente))
        os.makedirs(cliente_dir, exist_ok=True)

        # Salva as mensagens em JSON
        with open(os.path.join(cliente_dir, "mensagens.json"), 'w', encoding='utf-8') as f:
            json.dump({
                "chatId": chat_id,
                "contact": {
                    "name": nome_cliente,
                    "number": numero_cliente
                },
                "mensagens": mensagens_formatadas
            }, f, indent=4, ensure_ascii=False)

        # Salva as mensagens em HTML
        with open(os.path.join(cliente_dir, "mensagens.html"), 'w', encoding='utf-8') as f:
            f.write(gerar_html(nome_cliente, mensagens_formatadas))

        print(f"✅ Mensagens salvas para {nome_cliente} ({chat_id})")

        time.sleep(0.3)

    print("\n🏁 Finalizado!")

if __name__ == "__main__":
    extrair_mensagens()