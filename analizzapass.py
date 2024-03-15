#PROGRAMMA IN PYTHON CHE ANALIZZA LA PASSWORD INSERITA E NE VERIFICA LA SICUREZZA



class AnalizzatorePassword:
    def __init__(self, password):
        self.password = password

    def _controlla_lunghezza(self):
        return len(self.password) >= 8

    def _controlla_maiuscole(self):
        return any(char.isupper() for char in self.password)

    def _controlla_minuscole(self):
        return any(char.islower() for char in self.password)

    def _controlla_numeri(self):
        return any(char.isdigit() for char in self.password)

    def _controlla_simboli(self):
        simboli = "!@#$%^&*()"
        return any(char in simboli for char in self.password)

    def forza_password(self):
        punti = 0
        controlli = [
            self._controlla_lunghezza,
            self._controlla_maiuscole,
            self._controlla_minuscole,
            self._controlla_numeri,
            self._controlla_simboli,
        ]
        for controllo in controlli:
            if controllo():
                punti += 1

        forza = "Debole"
        if punti >= 3:
            forza = "Media"
        if punti >= 4:
            forza = "Forte"
        if punti >= 5:
            forza = "Robusta"

        return f"La tua password ha una forza {forza}."

# Esempio di utilizzo
password_utente = input("Inserisci la tua password: ")
analizzatore = AnalizzatorePassword(password_utente)
risultato = analizzatore.forza_password()
print(risultato)
