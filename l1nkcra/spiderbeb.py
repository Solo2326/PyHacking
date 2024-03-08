import argparse
from bs4 import BeautifulSoup
import MySQLdb

class WebSpider():
    def __init__(self, url, profondita, database_config, proxies=None):
     # Controllo argomenti
     if not url:
        raise ValueError("Errore: URL non specificato.")
    if not isinstance(profondita, int) or profondita <= 0:
        raise ValueError("Errore: Profondità non valida.")
    if not database_config:
        raise ValueError("Errore: Configurazione del database non specificata.")

    # Impostazioni di base
    self.url = url
    self.profondita = profondita
    self.totaleProfondita = 0
    self.linksVisitati = set()
    self.proxies = proxies

    # Connessione al database
    self.db = MySQLdb.connect(**database_config)
    self.cursorDB = self.db.cursor()

    # Inizializzazione variabili
    self.idWebSiteRoot = None

    def crawl(self):
    
        print("[*] Inizio crawling del sito web...")

    # Recupera e analizza il sito web principale
    response = requests.get(self.url)
    rootSite = BeautifulSoup(response.text, 'html.parser')

    # Memorizza informazioni sul sito web principale
    self.idWebSiteRoot = self.storeWebSiteRoot(self.url, contents)
    self.storeWebSiteForms(self.url)
    self.storeWebSiteLinks(rootSite.find_all("a"))

    # Scansione ricorsiva dei link
    try:
        for link in rootSite.find_all("a"):
            self.handleLink(link)
    finally:
        self.db.close()
        self.cursorDB.close()




    def handleLink(self, link):
    

        self.totaleProfondita += 1
    if self.totaleProfondita > self.profondita:
        self.totaleProfondita -= 1
        return

    if 'href' in link.attrs and 'http' in link['href']:
        try:
            href = link["href"]
            if href in self.linksVisitati:
                return

            self.linksVisitati.add(href) 

            print(f"[*] Crawling: {href}")
            response = requests.get(href, proxies=self.proxies)

            if response.status_code == 200:
                linkSite = BeautifulSoup(response.text, 'html.parser') 
                self.storeWebSiteForms(href)
                self.storeWebSiteLinks(linkSite.find_all("a")) 

                if self.totaleProfondita <= self.profondita:
                    for sublink in linkSite.find_all("a"):
                        self.handleLink(sublink)

        except Exception as e:  # Gestione degli errori
            print(f"[-] Errore nel recupero del link: {href}")
            print(f"[-] Errore: {str(e)}")

    self.totaleProfondita -= 1

    def storeWebSiteRoot(self, url, contents):
        # ... codice di memorizzazione dati sito web ...

    def storeWebSiteForms(self, url):
        # ... codice di memorizzazione dati form ...

    def storeWebSiteLinks(self, links):
        # ... codice di memorizzazione dati link ...

# Analisi argomenti
parser = argparse.ArgumentParser()
# ...

# Esecuzione Web Spider
spider = WebSpider(args.url, args.profondita, args.config, args.proxy)
spider.crawl()
