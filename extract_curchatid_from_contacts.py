import requests
import json
import time

API_TOKEN = 'Token Aqui'  # Substitua pelo seu token de API
BASE_URL = 'https://#########/contacts/'

headers = {
    'access-token': API_TOKEN,
    'Content-Type': 'application/json'
}

def extract_cur_chat_ids():
    """
    Lê uma lista de chats, busca o curChatId de cada contato na API
    e salva o resultado em um arquivo JSON.
    """
    with open('chats_list_Etna2076.json', 'r', encoding='utf-8') as f:
        chats_data = json.load(f)

    results = []
    seen = set()
    total = 0

    for chat in chats_data:
        contact = chat.get("contact")
        if not contact:
            continue

        contact_id = contact.get("id")
        total += 1
        print(f"📌 Registro {total}: contactId = {contact_id}")

        if not contact_id or contact_id in seen:
            print("⏭️ Ignorado (vazio ou duplicado)")
            continue

        seen.add(contact_id)
        url = f"{BASE_URL}{contact_id}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            results.append({
                "contactId": contact_id,
                "curChatId": data.get("curChatId")
            })
            print(f"✅ contactId {contact_id} processado.")
        else:
            print(f"❌ Erro para contactId {contact_id}: {response.status_code} - {response.text}")

        time.sleep(0.3)

    # Salva os resultados em um arquivo JSON
    with open('contacts_curchatid.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"\n📦 Total de {len(results)} registros salvos em contacts_curchatid.json")

if __name__ == "__main__":
    extract_cur_chat_ids()