from abc import ABC, abstractmethod
import datetime

anno = datetime.date.today().year
#print(anno)  # Output: 2026 (o l'anno attuale)

class Elettrodomestico(ABC):
    
    # costruttore con attributi privati
    def __init__(self, marca: str, modello:str, anno_acquisto:int, guasto:str):
        self.__marca = marca
        self.__modello = modello
        self.__anno_acquisto = anno_acquisto
        self.__guasto = guasto
    
    # metodo concreto per ritorna descrizione
    def descrizione(self):
        return (
        f" | Classe: {type(self)}"
        f" | Marca: {self.get_marca()}" +
        f" | Modello:{self.get_modello()}" +
        f" | Anno d'acquisto: {self.get_anno_acquisto()}" +
        f" | Guasto: {self.get_guasto()}"
        )

    def stima_costo_base(self):
        return 50
            
    # metodi getter
    def get_marca(self):
        return self.__marca
    
    def get_modello(self):
        return self.__modello
    
    def get_anno_acquisto(self):
        return self.__anno_acquisto
    
    def get_guasto(self):
        return self.__guasto
    
    # metodi setter
    def set_marca(self, nuova_marca):
        self.__marca = nuova_marca
    
    def set_modello(self, nuovo_modello):
        self.__modello = nuovo_modello
    
    def set_anno_acquisto(self, nuovo_anno_acquisto):
        anno = datetime.date.today().year
        # Check per verificare che l'anno di acquisto non sia nel futuro
        if nuovo_anno_acquisto >= anno:
            self.__anno_acquisto = nuovo_anno_acquisto
        else:
            raise ValueError("L'anno di acquisto non può essere nel futuro")
            
    def set_guasto(self, nuovo_guasto):
        self.__guasto = nuovo_guasto
        
        
class Forno(Elettrodomestico):
    
    def __init__(self, marca: str, modello:str, anno_acquisto:int, guasto:str, tipo_alimentazione: str, ha_ventilato:bool):
        super().__init__(marca, modello, anno_acquisto, guasto)
        self.tipo_alimentazione = tipo_alimentazione
        self.ha_ventilato = ha_ventilato
        
    def stima_costo_base(self):
        if self.tipo_alimentazione == 'elettrico':
            if self.ha_ventilato:
                return super().stima_costo_base() + 25
            else:
                return super().stima_costo_base() + 15
        else:
            if self.ha_ventilato:
                return super().stima_costo_base() + 20
            else:
                return super().stima_costo_base() + 10
            
    def descrizione(self):
        return (
            super().descrizione() +
            f" | Tipo alimentazione: {self.tipo_alimentazione}"
            f" | Ventilato: {self.ha_ventilato}"
        )
                
    
f1 = Forno("samsung", "ab1", "2024", "resistenza", "elettrico", True)

print(f1.descrizione())



f2 = Forno("turi", "cd2", "2021", "resistenza", "elettrico", False)

f3 = Forno("cico", "ef3", "2025", "resistenza", "gas", True)

f4 = Forno("canon", "ab1", "2027", "sportello", "gas", False)



class Frigorifero(Elettrodomestico):
    
    def __init__(self, marca: str, modello:str, anno_acquisto:int, guasto:str, litri:int, ha_freezer:bool):
        super().__init__(marca, modello, anno_acquisto, guasto)
        self.litri = litri
        self.ha_freezer = ha_freezer

    def stima_costo_base(self):
        costo_base = super().stima_costo_base()

        if self.litri > 50:
            return costo_base + 30 + (30 if self.ha_freezer else 0)
        elif self.litri > 25:
            return costo_base + 10 + (30 if self.ha_freezer else 0)
        else:
            return costo_base + (30 if self.ha_freezer else 0)
    
    def descrizione(self):
        return (
            super().descrizione() +
            f" | Capacità: {self.litri} l"
            f" | Freezer: {'V' if self.ha_freezer else 'X'}"
        )

class Lavatrice(Elettrodomestico): 
    
    soglia_capacita_alta = 8
    
    def __init__(self, marca: str, modello: str, anno_acquisto: int, guasto: str,
                 capacita_kg: int, giri_centrifuga: int):
        
        super().__init__(marca, modello, anno_acquisto, guasto)
        
        # attributi pubblici, niente __ davanti
        self.capacita_kg = capacita_kg
        self.giri_centrifuga = giri_centrifuga

    def stima_costo_base(self):
        costo = super().stima_costo_base()
        if self.capacita_kg > self.soglia_capacita_alta:  # self.capacita_kg, non self.__capacita_kg
            costo += 20.0
        return costo

    def descrizione(self):
        return (
            super().descrizione() +
            f" | Capacità: {self.capacita_kg} kg"           # stesso
            f" | Centrifuga: {self.giri_centrifuga} giri/min"  # stesso
        )
    
    

class TicketRiparazione:
    
    ID_TICKET = 0
    
    def __init__(self, elettrodomestico: Elettrodomestico, stato = None, note = None):
        TicketRiparazione.ID_TICKET +=1
        self.__id_ticket = TicketRiparazione.ID_TICKET
        self.__elettrodomestico = elettrodomestico
        self.__stato = stato if stato is not None  else "aperto"
        self.__note = note if note is not None else []
        
    def calcola_preventivo(self, extra1 = None, extra2 = None):
        if extra1 == "commissioni" and extra2 == "iva":
            costo = self.get_elettrodomestico().stima_costo_base() + 10
            print("Commissioni di €10 applicate + iva al 22%")
            return costo * 1.22
        elif extra1 == "commissioni": 
            costo = self.get_elettrodomestico().stima_costo_base() + 10
            print("Commissioni di €10 applicate")
            return costo
        else:
            print("Nessun extra addebbitato")
            return self.get_elettrodomestico().stima_costo_base()
        
        
    # Metodi getter
    
    def get_id(self):
        return self.__id_ticket
    
    def get_elettrodomestico(self):
        return self.__elettrodomestico
    
    def get_stato(self):
        return self.__stato
    
    def get_note(self):
        return self.__note
    
    # Metodi setter
    def set_stato(self, nuovo_stato):
        self.__stato = nuovo_stato
        
    def aggiungi_note(self, nuove_note : str):
        self.__note = self.__note.append(nuove_note)
    
    
class Officina:
    
    def __init__(self, nome, tickets = None):
        self.nome = nome
        self.tickets = tickets if tickets is not None else []
        
    def aggiungi_ticket(self):
        elettrodomestico = input("Per quale elettrodomestico vuoi aprire un ticket?\n 1 : Frigorifero\n 2 : Lavatrice\n 3 : Forno \n * per uscire | ")
        match elettrodomestico:
            case "1":
                marca = input("Marca: ")
                modello = input("Modello: ")
                anno_acquisto = int(input("Anno di acquisto: "))
                guasto = input("Guasto: ")
                litri = int(input("Litri: "))
                ha_freezer = input("Ha freezer? (V per sì, X per no): ").upper() == "V"
                elettrodomestico = Frigorifero(marca, modello, anno_acquisto, guasto, litri, ha_freezer)
                ticket = TicketRiparazione(elettrodomestico)
                return ticket
            case "2":
                marca = input("Marca: ")
                modello = input("Modello: ")
                anno_acquisto = int(input("Anno di acquisto: "))
                guasto = input("Guasto: ")
                capacita_kg = int(input("Capacità (kg): "))
                giri_centrifuga = int(input("Giri di centrifuga: "))
                elettrodomestico = Lavatrice(marca, modello, anno_acquisto, guasto, capacita_kg, giri_centrifuga)
                ticket = TicketRiparazione(elettrodomestico)
                return ticket
            case "3":
                marca = input("Marca: ")
                modello = input("Modello: ")
                anno_acquisto = int(input("Anno di acquisto: "))
                guasto = input("Guasto: ")
                tipo_alimentazione = input("Tipo di alimentazione (elettrico/gas): ")
                ha_ventilato = input("True se il forno è ventilato, False altrimenti: ").title()
                elettrodomestico = Forno(marca, modello, anno_acquisto, guasto, tipo_alimentazione, ha_ventilato)
                ticket = TicketRiparazione(elettrodomestico)
                return ticket
            case "*":
                print("Uscita dal programma.")
                return
            case _:
                print("Scelta non valida, riprova.")
                
            
        self.tickets.append(ticket)   
    
    def chiudi_ticket(self, id_ticket):
        for ticket in self.tickets:
            if ticket.get_id() == id_ticket:
                ticket.set_stato("chiuso")
                break
    
    def stampa_ticket_aperti(self):
        for t in self.tickets:
            if t.get_stato() == "aperto":
                print(f" | ID: {t.get_id()} | Tipo elettrodomestico: {t.get_elettrodomestico().__class__.__name__} | Stato: {t.get_stato()}")
                return True
    
    def totale_preventivi(self):
        tot = 0
        for t in self.tickets:
            tot += t.calcola_preventivo()
        print(f"Il totale dei preventivi è di {tot}")
        return tot
    
    
    def statistiche_per_tipo(self):
        n_lavatrici = 0
        n_frigoriferi = 0
        n_forni = 0
        
        for t in self.tickets:
            if t.isinstance(t.get_elettrodomestico(), Lavatrice):
                n_lavatrici += 1
            elif t.isinstance(t.get_elettrodomestico(), Frigorifero):
                n_frigoriferi += 1
            elif t.isinstance(t.get_elettrodomestico(), Forno):
                n_forni += 1
                
        print(f"Numero di lavatrici in riparazione: {n_lavatrici}")
        print(f"Numero di frigoriferi in lavorazione: {n_frigoriferi}")
        print(f"Numero di forni in lavorazione: {n_forni}")
        



o = Officina("Masamune") 

aperta = True 

while aperta:
    azione = input("Cosa vuoi fare? 1 : Aggiungi ticket | 2 : Chiudi ticket | 3 : Stampa ticket aperti | 4 : Totale preventivi | 5 : Statistiche per tipo | * per uscire: ")
    match azione:
        case "1":
            ticket = o.aggiungi_ticket()
            if ticket is not None:
                o.tickets.append(ticket)
        case "2":
            id_ticket = int(input("ID del ticket da chiudere: "))
            o.chiudi_ticket(id_ticket)
        case "3":
            o.stampa_ticket_aperti()
        case "4":
            o.totale_preventivi()
        case "5":
            o.statistiche_per_tipo()
        case "*":
            print("Uscita dal programma.")
            aperta = False
        case _:
            print("Scelta non valida, riprova.")
    