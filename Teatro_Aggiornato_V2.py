class Posto:
    def __init__(self, numero, fila, occupato=False):
        self._numero = numero
        self._fila = fila.upper()
        self._occupato = occupato

    @property
    def numero(self):
        return self._numero

    @property
    def fila(self):
        return self._fila

    @property
    def occupato(self):
        return self._occupato

    def prenota(self):
        if self._occupato:
            print(f"Il posto {self._fila}{self._numero} è già occupato.")
            return False
        self._occupato = True
        print(f"Posto {self._fila}{self._numero} prenotato con successo.")
        return True

    def libera(self):
        if not self._occupato:
            print(f"Il posto {self._fila}{self._numero} è già libero.")
            return False
        self._occupato = False
        print(f"Posto {self._fila}{self._numero} liberato.")
        return True

class PostoVIP(Posto):
    def __init__(self, numero, fila, occupato=False):
        super().__init__(numero, fila, occupato)
        self.servizi_extra = []

    def aggiungi_servizi(self, lista_servizi):
        if lista_servizi:
            self.servizi_extra.extend(lista_servizi)
            print(f"Servizi aggiunti al posto {self.fila}{self.numero}: {', '.join(lista_servizi)}")

class PostoStandard(Posto):
    def __init__(self, numero, fila, costo, occupato=False):
        super().__init__(numero, fila, occupato)
        self.costo = costo

    def prenota(self):
        if super().prenota():
            print(f"Tariffa applicata: €{self.costo}")
            return True
        return False

class Teatro:
    def __init__(self, righe_file, posti_per_fila):
        self._posti = []
        self._genera_teatro(righe_file, posti_per_fila)

    def _genera_teatro(self, righe_file, posti_per_fila):
        # Definiamo le file A e B come VIP
        file_vip = ['A', 'B']
        for fila in righe_file:
            for numero in range(1, posti_per_fila + 1):
                if fila.upper() in file_vip:
                    nuovo_posto = PostoVIP(numero, fila)
                else:
                    # Costo standard fissato a 15.0 euro
                    nuovo_posto = PostoStandard(numero, fila, 15.0)
                self._posti.append(nuovo_posto)

    def trova_posto(self, numero, fila):
        fila = fila.upper()
        for posto in self._posti:
            if posto.numero == numero and posto.fila == fila:
                return posto
        return None

    def prenota_posto(self, numero, fila, tipo_richiesto):
        posto = self.trova_posto(numero, fila)
        
        if posto is None:
            print(f"Errore: Il posto {fila}{numero} non esiste.")
            return False

        # Verifica coerenza tra tipo scelto e tipo del posto
        is_vip_posto = isinstance(posto, PostoVIP)
        
        if tipo_richiesto == "2" and not is_vip_posto:
            print("Errore: Hai selezionato un biglietto VIP per un posto Standard.")
            return False
        if tipo_richiesto == "1" and is_vip_posto:
            print("Errore: Hai selezionato un biglietto Standard per un posto VIP.")
            return False

        if posto.prenota():
            # Se è VIP, chiediamo i servizi extra qui (logica di interfaccia)
            if isinstance(posto, PostoVIP):
                servizi_input = input("Inserisci servizi extra separati da virgola (o premi invio): ")
                servizi = [s.strip() for s in servizi_input.split(",") if s.strip()]
                posto.aggiungi_servizi(servizi)
            return True
        return False

    def libera_posto(self, numero, fila):
        posto = self.trova_posto(numero, fila)
        if posto:
            return posto.libera()
        print("Posto non trovato.")
        return False

    def stampa_posti_occupati(self):
        print("\n--- ELENCO POSTI OCCUPATI ---")
        occupati = [p for p in self._posti if p.occupato]
        if not occupati:
            print("Nessun posto occupato.")
        for p in occupati:
            tipo = "VIP" if isinstance(p, PostoVIP) else "Standard"
            print(f"[{tipo}] Fila: {p.fila}, Numero: {p.numero}")

def main():
    # Inizializzazione: file A-L, 20 posti per fila
    elenco_file = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'L']
    teatro = Teatro(elenco_file, 20)

    while True:
        accesso = input("\nVuoi accedere al sistema teatro? (SI/NO): ").upper()
        if accesso != "SI":
            print("Chiusura programma...")
            break
        
        while True:
            print("\n--- MENU ---")
            print("1. Prenota Posto")
            print("2. Libera Posto")
            print("3. Visualizza Posti Occupati")
            print("4. Torna al menu principale")
            scelta = input("Scegli un'opzione: ")

            if scelta == "1":
                print("Nota: File A-B sono VIP, C-L sono Standard.")
                tipo = input("Tipo biglietto (1 Standard | 2 VIP): ")
                f = input("Fila (lettera): ")
                try:
                    n_input = input("Numero posto: ")
                    n = int(n_input)
                    teatro.prenota_posto(n, f, tipo)
                except ValueError:
                    print("Errore: Inserisci un numero valido.")

            elif scelta == "2":
                f = input("Fila: ")
                try:
                    n_input = input("Numero: ")
                    n = int(n_input)
                    teatro.libera_posto(n, f)
                except ValueError:
                    print("Errore: Inserisci un numero valido.")

            elif scelta == "3":
                teatro.stampa_posti_occupati()

            elif scelta == "4":
                break
            else:
                print("Opzione non valida.")

if __name__ == "__main__":
    main()
