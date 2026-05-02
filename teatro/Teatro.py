class Posto:
    
    def __init__(self, numero: int, fila: str, occupato= False):
        self._numero = numero
        self._fila = fila
        self._occupato = occupato
        
    def prenota(self):
        # Controllo: il posto è già occupato?
        if self._occupato:
            # Se sì, informo l'utente che non può prenotarlo
            print(f"Il posto {self._numero} {self._fila} è già occupato")
            # Ritorno False per indicare che la prenotazione NON è andata a buon fine
            return False
        # Se il posto era libero, lo segno come occupato
        else:
            self._occupato = True
            print(f"Posto {self._numero} {self._fila} prenotato")
            # Ritorno True per indicare che la prenotazione è riuscita
            return True
    
    def libera(self):
        if not self._occupato:
            # Se è già libero, non posso "liberarlo" di nuovo
            print(f"Il posto {self._numero} {self._fila} è gia libero")
            # Ritorno False per indicare che l'operazione NON è andata a buon fine
            return False
        
        else: # Se il posto era occupato, lo rendo libero
            self._occupato = False
            print(f"Posto {self._numero} {self._fila} liberato")
            # Ritorno True per indicare che l'operazione è riuscita
            return True
        
    # metodi getter per numero, fila e occupato
    def get_numero(self):
        return self._numero
    
    def get_fila(self):
        return self._fila
    
    def get_occupato(self):
        return self._occupato
    
    # metodi setter per numero, fila
    def set_numero(self, nuovo_numero):
        self._numero = nuovo_numero
    
    def set_fila(self, nuova_fila):
        self._fila = nuova_fila
        

class PostoVIP(Posto):
    
    def __init__(self, numero, fila, occupato = False, servizi_extra = None):
        super().__init__(numero, fila, occupato)
        self.servizi_extra = servizi_extra if servizi_extra is not None else []
        
    def aggiungi_servizi_extra(self):
        # fa agginugere all'utente tutti i servizi extra che vuole acquistare
        prenotazione_servizi = True
        while prenotazione_servizi:
            servizi = input("Quali servizi extra vuoi prenotare? 1 per Accesso al lounge | 2 per Servizio in posto | * per smemmete di selezionare servizi aggiuntivi: ")
            match servizi:
                case "1":
                    self.servizi_extra.append("accesso al lounge")
                case "2":
                    self.servizi_extra.append("servizio in posto")
                case "*":
                    prenotazione_servizi = False
                case _:
                    print("Scelta non valida, riprova.")
        
    def prenota(self):
        prenotazione = super().prenota() # ritorna True se la prenotazione è riuscita, False altrimenti
        # fa agginugere all'utente tutti i servizi extra che vuole acquistare
        if prenotazione: # se prenotazione è riuscita, posso aggiungere i servizi extra
            self.aggiungi_servizi_extra()
            return True
        else: # se prenotazione è fallita, non posso aggiungere i servizi extra
            print("Prenotazione del posto VIP fallita, non è possibile selezionare servizi extra.")
            return False

    def get_servizi_extra(self):
        return self.servizi_extra
    
    def set_servizi_extra(self,):
        self.servizi_extra = []
        self.aggiungi_servizi_extra()
        
    
class PostoStandard(Posto):
    
    def __init__(self, numero, fila, costo, occupato = False):
        super().__init__(numero, fila, occupato)
        self.costo = costo
    
    # override del metodo prenota per aggiungere un print che indica il costo del Posto Standard    
    def prenota(self):
        if super().prenota(): # se la prenotazione è riuscita, stampo il costo del posto
            print(f"Il posto selezionato ha un costo di €{self.costo}")
            return True
        else: 
            print("Prenotazione del posto Standard fallita.")
            return False
    
    # metodi getter e setter per costo
    def get_costo(self):
        return self.costo
    
    def set_costo(self, nuovo_costo):
        self.costo = nuovo_costo
        
class Teatro:
    
    def __init__(self, posti):
        self._posti = posti
        
    def aggiungi_posto(self, posto: Posto):
        # aggiunge un'istanza di classe Posto alla lista _posti
        self._posti.append(posto)
    
    def trova_posto(self, numero, fila):
        # ritorna l'istanza di classe Posto se trovato, None altrimenti
        for posto in self._posti:
            if posto.get_numero() == numero and posto.get_fila() == fila:
                return posto
        return None
    
    def prenota_posto(self, numero, fila):
        
        # trovo il posto corrispondente a numero e fila
        posto_trovato = self.trova_posto(numero, fila)
        
        # se esiste, lo prenoto, altrimenti informo l'utente che il posto non esiste
        if posto_trovato is not None:
            return posto_trovato.prenota()
        else:
            print(f"Il posto {numero} {fila} non esiste.")
            return False
    
    def libera_posto(self, numero, fila):
        
        # trovo il posto corrispondente a numero e fila
        posto_trovato = self.trova_posto(numero, fila)
        
        # se esiste, lo libero, altrimenti informo l'utente che il posto non esiste
        if posto_trovato is not None:
            # libera() integra il check per verificare se il posto è già libero o meno
            return posto_trovato.libera() # libera() integra il check per verificare se il posto è già libero o meno
        else:
            print(f"Il posto {numero} {fila} non esiste.")
            return False
           
    def stampa_posti_occupati(self):
        # Stampa tutti i posti occupati, indicando numero, fila e se è un posto VIP o Standard
        for posto in self._posti:
            if posto.get_occupato():
                print(posto.__class__.__name__, posto.get_numero(), posto.get_fila())
                


t = Teatro([])

while True:
    accesso = input("Vuoi accedere al teatro? SI | NO ")

    if accesso.upper() == "SI":
        while True:
            scelta = input(
                "1 Prenota | 2 Libera | 3 Visualizza | 4 Esci: "
            )
            match scelta:
                case "1":

                    tipo = input("1 Standard | 2 VIP: ")
                    n = int(input("Numero: "))
                    f = input("Fila: ")
                    posto = t.trova_posto(n, f)
                    if posto is not None:
                        print("Il posto esiste già.")
                        posto.prenota()
                        continue
                    if tipo == "1":
                        c = float(input("Costo: "))
                        nuovo = PostoStandard(n, f, c)
                    elif tipo == "2":
                        nuovo = PostoVIP(n, f)
                    else:
                        print("Scelta non valida")
                        continue
                    t.aggiungi_posto(nuovo)
                    nuovo.prenota()

                case "2":
                    n = int(input("Numero: "))
                    f = input("Fila: ")
                    t.libera_posto(n, f)
                    
                case "3":
                    t.stampa_posti_occupati()

                case "4":
                    break
                case _:
                    print("Scelta non valida")

    elif accesso.upper() == "NO":
        print("Arrivederci!")
        break

    else:
        print("Scelta non valida")