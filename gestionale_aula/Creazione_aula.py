class Professore:
    
    def __init__(self, nome: str, cognome: str, materie = None, classi = None):
        self.__nome = nome
        self.__cognome = cognome
        self.__materie = materie if materie is not None else []
        self.__classi = classi if classi is not None else []
        
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nuovo_nome):
        self.__nome = nuovo_nome
    
    @property
    def cognome(self):
        return self.__cognome
    
    @cognome.setter
    def cognome(self, nuovo_cognome):
        self.__cognome = nuovo_cognome
    
    @property
    def materie(self):
        return self.__materie
    
    def get_materia(self, materia):
        if materia.lower() in self.__materie:
            return materia
        else:
            return None
    
    def aggiungi_materia(self, materia):
        if materia.lower() not in self.__materie:
            self.__materie.append(materia.lower())
    
    def rimuovi_materia(self, materia):
        if materia.lower() in self.__materie:
            self.__materie.remove(materia.lower())
    
    @property
    def classi(self):
        return self.__classi
    
    def aggiungi_classe(self, classe):
        if classe.lower() not in self.__classi:
            self.__classi.append(classe.lower())
    
    def rimuovi_classe(self, classe):
        if classe.lower() in self.__classi:
            self.__classi.remove(classe.lower())  

    def __str__(self):
        return f"Prof. {self.nome} {self.cognome} - Materie: {self.materie} - Classi: {self.classi}"
        
    def __repr__(self):
        return f"Professore(nome = {self.nome}, cognome = {self.cognome}, materie = {self.materie}, classi = {self.classi})"
    


def crea_aula(n_studenti, materia, professore):

    nome = input("Inserisci il nome della classe (Es. 4A) : ")
    with open(f"12_Giovedi_30_04/input_output/Aula_{nome}_{professore.cognome}.txt", "w") as file:
        file.write(f"Classe: {nome}\nMateria: {materia}\n\nStudenti:\n")
        for i in range(n_studenti):
            studente = input("Inserisci nome e cognome dello studente da aggiungere all'aula (Es: Mario Rossi) :").strip().title()
            file.write(studente + "\n")
        
    print(f"File 'Aula_{nome}_{professore.cognome}.txt' creato con successo!")
    return nome
    

def aggiungi_studente(classe, professore):
    nome = input("Aggiungi studente alla classe: ").strip().title()
    with open(f"12_Giovedi_30_04/input_output/Aula_{classe}_{professore.cognome}.txt", "a") as file:
        file.write(nome + "\n")
    print(f"Studente {nome} aggiunto alla classe {classe} con successo!")
    
    

def main():
    
    on = True

    while on: 
        nome = input("Inserisci il nome del professore: ").title()
        cognome = input("Inserisci il cognome del professore: ").title()
        #materie = input("Inserisci le materie insegnate dal professore (separate da virgola): ").strip().lower().split(",")
        #classi = input("Inserisci le classi in cui insegna il professore (separate da virgola): ").strip().lower().split(",")
        prof = Professore(nome, cognome)
        print(f"Benvenuto Prof. {prof.nome} {prof.cognome}")
        
        while True:
            print("\nOpzioni:")
            print("1. Aggiungi materia")
            print("2. Rimuovi materia")
            print("3. Aggiungi classe")
            print("4. Rimuovi classe")
            print("5. Aggiungi studente a classe")
            print("*. Esci")
            
            scelta = input("Scegli un'opzione: ").strip()
            
            match scelta:
                case "1":
                    print(prof.materie)
                    nuova_materia = input("Inserisci la nuova materia da aggiungere: ").lower()
                    prof.aggiungi_materia(nuova_materia)
                    print(f"Materia '{nuova_materia}' aggiunta con successo!")
                    print(f"Il prof {prof.cognome} insegna le seguenti materie : {prof.materie}")
                case "2":
                    print(prof.materie)
                    materia = input("digita la nuova materia da rimuovere: ").lower()
                    prof.rimuovi_materia(materia)
                    print(f"Materia '{materia}' rimossa con successo!")
                    print(f"Il prof {prof.cognome} insegna le seguenti materie : {prof.materie}")    
                case "3":
                    print(f"Le classi del {prof.cognome} sono {prof.classi}")
                    print(f"Le Materie che insegna il {prof.cognome} sono {prof.materie}")
                    materia = input("Per quale materia vuoi creare una classe? ").lower()
                    n_studenti = int(input("Quanti studenti ci sono nella classe? "))
                    if materia in prof.materie:
                        classe = crea_aula(n_studenti, materia, prof)
                    prof.aggiungi_classe(classe)
                case "4":
                    print(prof.classi)
                    classe_da_rimuovere = input("Inserisci la classe da rimuovere: ").strip().lower()
                    prof.rimuovi_classe(classe_da_rimuovere)
                    print(f"Classe '{classe_da_rimuovere}' rimossa con successo!")
                    print(f"Il prof {prof.cognome} insegna le seguenti materie : {prof.materie}")
                case "5":
                    print(prof.classi)
                    classe = input("In quale classe vuoi aggiungere uno studente? ")
                    aggiungi_studente(classe, prof)
                case "*":
                    print("Uscita dal gestionale. Arrivederci!")
                    break
        on = False
        
        
if __name__ == "__main__":
    main()