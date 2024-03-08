import requests
import time
import pprint
import argparse
import multiprocessing
import mimetypes
from aiutanti.TeleTesto import manda_mesaggio 
from aiutanti.TeleVedi import processa_messaggio  

def formatta_dizionario(titolo, dizionario):
    """Formatta un dizionario per una visualizzazione leggibile.

    Args:
        titolo (str): Il titolo da visualizzare sopra il dizionario.
        dizionario (dict): Il dizionario da formattare.

    Returns:
        str: Una stringa di testo ben formattata.
    """
    risultato = f"{titolo}:\n"
    for chiave, valore in dizionario.items():
        if isinstance(valore, dict):  
            risultato += '\n'.join(f"- {k}: {v}" for k, v in valore.items())
        else:
            risultato += f"- {chiave}: {valore}\n"
    return risultato + "\n"

def elimina_messaggi(bot_token, chat_id, message_id):
    """Tenta di eliminare messaggi su Telegram.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        chat_id (int): ID  della chat dove eliminare il messaggio.
        message_id (int): ID  del messaggio da eliminare.
    """
    try:
        response = deleteMessage(bot_token, chat_id, message_id)  # Assumiamo che questa funzione esista
        if response.get("ok") == True:
            print(f"Messaggio {message_id} eliminato")
            message_id -= 1  
        elif response.get("ok") == False and response.get("description") == "Bad Request: message can't be deleted for everyone":
            print(f"Il messaggio {message_id} è troppo vecchio. Puoi eliminare solo messaggi inviati nelle ultime 24 ore.")
        elif response.get("ok") == False:
            print(f"Messaggio {message_id} non trovato.")
    except Exception as e:
        print(f"Errore: {message_id}")

def deleteMessage(bot_token, chat_id, message_id):
    """Funzione fittizia per eliminare un messaggio (da implementare).

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        chat_id (int): ID  della chat dove eliminare il messaggio.
        message_id (int): ID  del messaggio da eliminare.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
    data = {"chat_id": chat_id, "message_id": message_id}
    response = requests.post(url, data=data)
    return response.json()

def send_file_to_telegram_channel(bot_token, chat_id, file_path):
    """Invia un file a un canale Telegram.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        chat_id (int): ID  della chat del canale Telegram.
        file_path (str): Percorso assoluto del file da inviare.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    try:
        mime_type = mimetypes.guess_type(file_path)[0]
        file_type = 'document'  # Predefinito su "documento"

        if mime_type:
            if 'audio' in mime_type:
                file_type = 'audio'
            elif 'video' in mime_type:
                file_type = 'video'
            elif 'image' in mime_type:
                file_type = 'photo'

        file_type_methods = {
            'document': 'sendDocument',
            'photo': 'sendPhoto',
            'audio': 'sendAudio',
            'video': 'sendVideo',
            'animation': 'sendAnimation',
            'voice': 'sendVoice',
            'video_note': 'sendVideoNote'
        }

        url = f"https://api.telegram.org/bot{bot_token}/{file_type_methods[file_type]}"
        with open(file_path, 'rb') as file:
            files = {'file': file}
            message = input("Inserisci il messaggio da inviare con il file (premi invio per saltare): ")
            data = {'chat_id': chat_id, 'caption': message}
            response = requests.post(url, files=files, data=data)
            return response.json()
    except Exception as e:
        print(f"Errore durante l'invio del file: {e}")

def get_my_commands(chat_id, bot_token):
    """Recupera i comandi del bot per la chat specificata.

    Args:
        chat_id (int): ID  della chat.
        bot_token (str): Token autorizzativo del bot Telegram.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getMyCommands"
    data = {"chat_id": chat_id}
    response = requests.get(url, data=data)
    return response.json()

def get_updates(bot_token, offset=None, timeout=30):
    """Recupera gli aggiornamenti dal server Telegram.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        offset (int, optional): ID  dell'ultimo aggiornamento ricevuto (per la scansione successiva).
        timeout (int, optional): Timeout in secondi per la ricezione di nuovi aggiornamenti.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates?timeout={timeout}"
    if offset:
        url += f"&offset={offset}"
    response = requests.get(url)
    return response.json()

def get_bot_info(bot_token):
    """Recupera informazioni sul bot.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url)
    return response.json()

def get_My_Default_AdministratorRights(bot_token, chat_id):
    """Recupera i diritti di amministratore predefiniti del bot per la chat.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        chat_id (int): ID  della chat.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getMyDefaultAdministratorRights"
    data = {"chat_id": chat_id}
    response = requests.get(url, data=data)
    return response.json()
def get_chat_info(bot_token, chat_id):
    """Recupera informazioni sulla chat.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        chat_id (int): ID  della chat.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getChat"
    data = {"chat_id": chat_id}
    response = requests.post(url, data=data)
    return response.json()

def get_chat_administrators(bot_token, chat_id):
    """Recupera l'elenco degli amministratori della chat.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        chat_id (int): ID  della chat.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getChatAdministrators"
    data = {"chat_id": chat_id}
    response = requests.post(url, data=data)
    return response.json()

def get_chat_member_count(bot_token, chat_id):
    """Recupera il numero di membri della chat.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        chat_id (int): ID  della chat.

    Returns:
        dict: Dizionario con la risposta del server Telegram.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getChatMembersCount"
    data = {"chat_id": chat_id}
    response = requests.post(url, data=data)
    return response.json()

def get_latest_messageid(bot_token, chat_id):
    """Recupera l'ID  dell'ultimo messaggio inviato nella chat.

    Args:
        bot_token (str): Token autorizzativo del bot Telegram.
        chat_id (int): ID  della chat.

    Returns:
        int: ID  dell'ultimo messaggio, oppure None in caso di errore.
    """
    response = send_telegram_message(bot_token, chat_id, ".")
    if response.get("ok") == True:
        message_id = response.get('result').get('message_id')
        deleteMessage(bot_token, chat_id, message_id)
        return message_id
    else:
        print("Errore: Impossibile recuperare l'ID  dell'ultimo messaggio:",
            response.get("description"))
        return None

def main(bot_token, chat_id):
    """Funzione principale dello script. Permette la gestione del bot Telegram."""

    # Recupera informazioni 
    can_read = get_bot_info(bot_token).get('result', {}).get('can_read_all_group_messages', False)

    print(formatta_dizionario("Informazioni sul bot", get_bot_info(bot_token)))
    print(formatta_dizionario("Informazioni sulla chat", get_chat_info(bot_token, chat_id)))
    # ... altre chiamate per visualizzare admins, diritti, etc.

    while True:
        print("\nOpzioni:")
        print("1. Monitora nuovi messaggi da un altro bot")
        print("2. Invia un messaggio al canale Telegram dannoso")
        # ... Altre opzioni ...
        print("8. ESCI")

        scelta = input("\nInserisci la tua scelta: ")

        #  Gestire la scelta dell'utente (if / elif)
        # ...

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script per Bot Telegram")
    parser.add_argument("-t", "--bot_token", help="Token del Bot Telegram")
    parser.add_argument("-c", "--chat_id", help="ID Chat Telegram", type=int)
    args = parser.parse_args()

    main(args.bot_token, args.chat_id)
def controlla_file_per_token_e_chat_id(percorso_file, bot_token, chat_id):
    """Controlla se un file contiene una specifica coppia token/ID chat.

    Args:
        percorso_file (str): Percorso del file da controllare.
        bot_token (str): Token del bot Telegram.
        chat_id (int): ID  chat Telegram.

    Returns:
        bool: True se la coppia token/ID chat è presente nel file, False altrimenti.
    """
    with open(percorso_file, 'r') as file:
        for riga in file:
            if riga.strip() == f"{bot_token}:{chat_id}":
                return True
    return False

def aggiungi_token_e_chat_id_al_file(percorso_file, bot_token, chat_id):
    """Aggiunge una coppia token/ID chat a un file.

    Args:
        percorso_file (str): Percorso del file dove aggiungere la coppia.
        bot_token (str): Token del bot Telegram.
        chat_id (int): ID  chat Telegram.
    """
    with open(percorso_file, 'a') as file:
        file.write(f"{bot_token}:{chat_id}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script per Bot Telegram")
    parser.add_argument("-t", "--bot_token", help="Token del Bot Telegram")
    parser.add_argument("-c", "--chat_id", help="ID Chat Telegram", type=int)
    args = parser.parse_args()

    percorso_file = ".bot-history"  # Sostituire con il percorso del file corretto

    if controlla_file_per_token_e_chat_id(percorso_file, args.bot_token, args.chat_id):
        print("Token del bot e ID chat già presenti nel file.")
        risposta = input("Vuoi continuare comunque? (s/n): ")
        if risposta.lower() != "s":
            exit()
    else:
        aggiungi_token_e_chat_id_al_file(percorso_file, args.bot_token, args.chat_id)

    main(args.bot_token, args.chat_id)

