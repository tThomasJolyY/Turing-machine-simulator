from recup_mt import create_dic

class Machine:
    def __init__(self,fichier) -> None:
        self.dic_etatstrans = create_dic(fichier)
        self.nb_rubans = self.calc_nb_rubans()
        self.etats_rubans = []
        self.etat_courant = "I"
        self.position = []
        self.nb_pas = 0
        self.rubans = []

    def reset(self,mot):
        self.etat_courant = "I"
        self.etats_rubans = []
        self.position = []
        self.nb_pas = 0
        self.rubans = []
        self.entrée(mot)        

    def calc_nb_rubans(self):
        for elt in self.dic_etatstrans.items():
            for car in range(len(elt[0])):
                if elt[0][car] == ",":
                    nb_rubans = len(elt[0]) - (car + 1)
        return nb_rubans

    def get_etat_courant(self):
        return self.etat_courant

    def get_etat_ruban(self):
        return self.etats_rubans

    def position_lecture(self):
        return self.position

    def get_transitions(self):
        pass

    def get_dic(self):
        return self.dic_etatstrans

    def entrée(self,mot):
        self.rubans.append(list(mot))
        if self.nb_rubans > 1:
            self.rubans.append(["_" for _ in range(self.nb_rubans-1)])
            self.etats_rubans= ["_" for _ in range(self.nb_rubans)]
            self.etats_rubans[0] = self.rubans[0][0]
        else:
            self.etats_rubans.append(self.rubans[0][0])
        self.position = [0 for _ in range(self.nb_rubans)]

    def __str__(self):
        l = "".join(str([self.rubans,self.etats_rubans,self.position,self.etat_courant,self.nb_pas]))
        return str(l)

    def pas(self):
        if self.rubans == []:
            print("Veuillez spécifier une entrée")
        for elt in self.dic_etatstrans.items():
            etat = elt[0]
            transi = elt[1]
            etat_courant_comp = "".join([etat[:car] for car in range(len(etat)) if etat[car] == ","])
            if etat_courant_comp == self.etat_courant:
                etats_comp = "".join([etat[car+1:] for car in range(len(etat)) if etat[car] == ","])
                if "".join(self.etats_rubans) == etats_comp:
                    self.etat_courant = transi[0]
                    for ruban_i in range(self.nb_rubans):
                        self.rubans[ruban_i][self.position[ruban_i]] = transi[1][ruban_i] 
                    for transition in range(self.nb_rubans): 
                        if transi[2][transition] == ">":
                            self.position[transition] += 1
                            if len(self.rubans[transition]) <= self.position[transition]:
                                self.rubans[transition].append("_")
                        if transi[2][transition] == "<": 
                            self.position[transition] -= 1
                            if self.position[transition] < 0:
                                old_rub = [elt for elt in self.rubans[transition]]
                                self.rubans[transition].append("_")
                                self.rubans[transition][0] = "_"
                                for elt in range(0,len(old_rub)):
                                    self.rubans[transition][elt+1] = old_rub[elt]
                                self.position[transition]= 0
                    for etat_rub in range(self.nb_rubans):
                        self.etats_rubans[etat_rub] = self.rubans[etat_rub][self.position[etat_rub]]
                    self.nb_pas += 1
                #print(mt_test)
                    return True
        return False
        
    def lancer_machine(self):
        while self.etat_courant != "F":
            res = self.pas()
            if not res:
                print("Le mot que vous avez entré n'est pas reconnu par la machine de turing")
                return False
        print("Voici l'état de la machine dans son état finale")
        print(self)
        return True

mt_test = Machine("mt.txt")
mt_test.entrée("100")
mt_test.lancer_machine()
mt_test.reset("001")
mt_test.pas()
print(mt_test)
