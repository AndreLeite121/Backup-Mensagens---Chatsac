# Backup Chat Extractor

Scripts para extração de conversas.

## Scripts

- **get_chats_list_lite.py**  
  Busca todos os chats finalizados do WhatsApp e salva em `chats_list.json`.

- **extract_curchatid_from_contacts.py**  
  Lê a lista de chats e busca o `curChatId` de cada contato, salvando em `contacts_curchatid.json`.

- **extrair_mensagens_por_chat.py**  
  Extrai as mensagens de cada chat, salvando em arquivos JSON e HTML organizados por cliente na pasta `Mensagens`.

## Como usar

1. **Obtenha a lista de chats:**
   ```
   python get_chats_list_lite.py
   ```
   Isso gera o arquivo `chats_list.json`.

2. **Extraia os curChatIds dos contatos:**
   ```
   python extract_curchatid_from_contacts.py
   ```
   Isso gera o arquivo `contacts_curchatid.json`.

3. **Extraia as mensagens de cada chat:**
   ```
   python extrair_mensagens_por_chat.py
   ```
   Isso gera uma pasta `Mensagens` com os arquivos de cada cliente.

## Requisitos

- Python 3.x
- requests

Instale as dependências com:
```
pip install requests
```

---
