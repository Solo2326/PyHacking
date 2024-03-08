import pyrogram
import json
from dotenv import load_dotenv
import os
import random

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


def get_file_info(data):
 media_type = ""
 random_numbers = [random.randint(1, 100) for _ in range(6)]
 if data.media is not None:
   try:
     for key in ['document', 'photo', 'video', 'location', 'voice', 'audio']:
       if key in str(data):
         media_type = key
         break
     if media_type == "document":
       return (data.document.file_id, data.document.file_name)
     elif media_type == "photo":
       return (data.photo.file_id, f"{random_numbers}.png")
     elif media_type == "video":
       return (data.video.file_id, data.video.file_name)
     elif media_type == "location":
       return (data.location.file_id, data.location.file_name)
     elif media_type == "voice":
       return (data.voice.file_id, data.voice.file_name)
     elif media_type == "audio":
       return (data.audio.file_id, data.audio.file_name)
     else:
       return None
   except Exception as e:
     print(f"Error: {e}")
     return None


def parse_and_print_message(message):
 print("=" * 20 + "\n")
 message_dict = message.__dict__
 for key, value in message_dict.items():
   if value not in [None, False]:
     print(f"{key}: {value}")
 print("\n")
 print("=" * 20 + "\n")


def processa_messaggio(bot_token, chat_id, num_messages, message_id):
 app = pyrogram.Client(bot_token, api_id, api_hash)

 async def main(num_messages, message_id):
   try:
     # Calcola il contatore per ottenere il numero corretto di messaggi. 
     # Lo facciamo per iterare sui messaggi in ordine inverso dall'ultimo messaggio.
     counter = message_id - num_messages
     while message_id >= counter:
       message_id -= 1
       async with app:
         messages = await app.get_messages(chat_id, message_id)
         if messages.date is None:
           # Mostra il message_id non trovato ogni 10 messaggi
           if message_id % 10 == 0:
             print(f"[-] Message_id {message_id} non trovato")
           counter -= 1
           pass
         else:
           parse_and_print_message(messages)
           if messages.media is not None:
             file_id, file_name = get_file_info(messages)
             if messages.from_user is not None:
               file_name = f"downloads/{messages.from_user.username}/{message_id}_{file_name}"
             else:
               file_name = f"downloads/{chat_id}/{message_id}_{file_name}"
             # Download del file
             # Segui la progressione durante il download
             async def progress(current, total):
               if total != 0:
                 print(f"{current * 100 / total:.1f}%")
               else:
                 print(f"[*] Download di {file_name.split('/')[-1]} completato!")

             await app.download_media(
                 file_id,
                 file_name=file_name,
                 progress=progress,
             )
           # Salva su file
           if messages.from_user is not None:
             with open(f'{messages.from_user.username}_bot.txt', 'a') as file:
               file.write(f"Message ID: {messages.id}\n")
               file.write(
                   f"From User ID: {messages.from_user.id} - Username: {messages.from_user.username}\n"
               )
               file.write(f"Date: {messages.date}\n")
               file.write(f"Text: {messages.text}\n")
               file.write(f"Reply_markup: {messages.reply_markup}\n\n")
             # Salva l'intero messaggio su file
             with open(f'{messages.from_user.username}_bot.json', 'a') as file:
               file.write(str(messages))
           else:
             with open(f'{chat_id}_bot.txt', 'a') as file:
               file.write(f"Message ID: {messages.id}\n")
               file.write(f"Date: {messages.date}\n")
               file.write(f"Text: {messages.text}\n")
               file.write(f"Reply_markup: {messages.reply_markup}\n\n")
             # Salva l'intero messaggio su file
             with open(f'{chat_id}_bot.json', 'a') as file:
               file.write(str(messages))
   except AttributeError as e:
     print(f"Error: {e}")
     pass
   except Exception as e:
     print(f"Error: {e}")
     pass

 try:
   app.run(main(num_messages, message_id))
 except KeyboardInterrupt:
   print("\nStopping...")
   app.disconnect()
   pass