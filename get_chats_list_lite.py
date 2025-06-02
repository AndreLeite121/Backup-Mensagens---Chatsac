import requests
import json
import time

API_TOKEN = 'seu_token_aqui'  # Substitua pelo seu token de acesso
URL = 'https://#########/chats/list-lite'

headers = {
    'access-token': API_TOKEN,
    'Content-Type': 'application/json'
}

def get_all_chats():
    """
    Busca todas as conversas (chats) da API, paginando os resultados,
    e salva o resultado em um arquivo JSON local.
    """
    all_chats = []
    page = 0
    while True:
        payload = {
            "page": page,
            "status": 2,       # Status do chat (ex: 2 = finalizado)
            "typeChat": 2      # Tipo do chat (ex: 2 = WhatsApp)
        }

        response = requests.post(URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            chats = data.get("chats", [])
            if not chats:
                break  # Fim da paginação
            all_chats.extend(chats)
            print(f"✅ Página {page} processada com {len(chats)} chats.")
            page += 1
            time.sleep(0.5)  # Pequeno delay entre requisições para evitar sobrecarga
        else:
            print(f"❌ Erro na página {page}: {response.status_code} - {response.text}")
            break

    # Salva todos os chats em um arquivo JSON
    with open('chats_list.json', 'w', encoding='utf-8') as f:
        json.dump(all_chats, f, indent=4, ensure_ascii=False)

    print(f"\n📦 Total de {len(all_chats)} chats salvos em chats_list.json")

if __name__ == "__main__":
    get_all_chats()