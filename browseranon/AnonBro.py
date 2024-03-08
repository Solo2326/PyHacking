import socket
import socks
import requests
from bs4 import BeautifulSoup

def connectTOR():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket

def analyze_form(form):
    form_data = {'name': form.name, 'controls': []}
    for control in form.controls:
        control_dict = {
            'name': control.name or "",
            'type': control.type or "",
            'value': control.value or ""
        }
        form_data['controls'].append(control_dict)
    return form_data

if __name__ == "__main__":
    connectTOR()
    response = requests.get("http://www.google.com")
    response.raise_for_status()  # Raise error if there's a problem

    soup = BeautifulSoup(response.content, 'html.parser')
    forms = soup.find_all('form')

    for form in forms:
        form_data = analyze_form(form)
        print("[*] Form:", form_data['name'])
        for control in form_data['controls']:
            print(f"   [*] Control Name: {control['name']}")
            print(f"   [*] Control Type: {control['type']}")
            print(f"   [*] Control Value: {control['value']}")

