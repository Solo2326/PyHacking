import requests
import argparse
import pprint
import time

def send_telegram_message(bot_token, chat_id, message):
  url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
  data = {"chat_id": chat_id, "text": message}
  response = requests.post(url, data=data)
  if response.json().get("ok") == True:
    print(f"Messaggio inviato con successo! -> ID messaggio: {response.json().get('result').get('message_id')}")
  return response.json()

def main(bot_token, chat_id, message, spam):
  if spam:
    while True:
      response = send_telegram_message(bot_token, chat_id, message)
      print("Messaggio inviato. Risposta:")
      pprint.pprint(response)
      time.sleep(0.04)
  else:
    response = send_telegram_message(bot_token, chat_id, message)
    print("Messaggio inviato. Risposta:")
    pprint.pprint(response)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Invia un messaggio a una chat Telegram")
  parser.add_argument("-t", "--bot_token", help="Token del Bot Telegram")
  parser.add_argument("-c", "--chat_id", help="ID della chat Telegram")
  parser.add_argument("-m", "--message", help="Messaggio da inviare")
  parser.add_argument("--spam", help="Attiva l'invio in loop", action="store_true")

  args = parser.parse_args()

  main(args.bot_token, args.chat_id, args.message, args.spam)
