from recup_mt import create_dic

class Machine:
    def __init__(self,fichier) -> None:
        self.dic_etatstrans = create_dic(fichier)
        self.nb_rubans = 0
        self.etat_ruban = ""
        self.etat_courant = "I"
        self.position = 0
        self.nb_pas = 0
        self.mot = ""

    def calc_nb_rubans(self):
        #for elt in self.dic_etatstrans.items():
         #   nb_rubans = len(elt[0]) - 1
        pass

    def get_etat_courant(self):
        return self.etat

    def get_etat_ruban(self):
        return self.etat_ruban

    def position_lecture(self):
        return self.position

    def get_transitions(self):
        pass

    def get_dic(self):
        return self.dic_etatstrans

    def entrée(self,mot):
        self.mot = list(mot)
        self.etat_ruban = self.mot[0]

    def __str__(self):
        l = "".join(str([self.mot,self.etat_ruban,self.position,self.etat_courant,self.nb_pas]))
        return str(l)

    def pas(self):
        if self.mot == "":
            print("Veuillez spécifier une entrée")
        for elt in self.dic_etatstrans.items():
            etat = elt[0]
            transi = elt[1]
            if etat[0] == self.etat_courant:
                if self.etat_ruban == etat[1]:
                    self.etat_courant = transi[0]
                    self.mot[self.position] = transi[1][0]
                    if transi[2][0] == ">":
                        self.position += 1
                    if transi[2][0] == "<":
                        self.position -= 1
                    self.etat_ruban = self.mot[self.position]
                    self.nb_pas += 1
            

mt_test = Machine("mt.txt")
mt_test.entrée("000")
mt_test.pas()
print(mt_test)