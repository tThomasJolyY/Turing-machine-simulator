from recup_mt import create_dic

class Machine:
    def __init__(self,fichier) -> None:
        self.input = None
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

    def get_nb_rub(self):
        return self.nb_rubans

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

    def get_position_lecture(self):
        return self.position

    def get_rubans(self):
        return self.rubans

    def set_rubans(self,nv_rub):
        self.rubans = nv_rub
    
    def set_position_lecture(self,nv_pos):
        self.position = nv_pos
        self.etats_rubans= [self.rubans[i][self.position[i]] for i in range(self.nb_rubans)]

    def get_dic(self):
        return self.dic_etatstrans

    def entrée(self,mot):
        self.input = mot
        self.rubans.append(list(mot))
        if self.nb_rubans > 1:
            for _ in range(self.nb_rubans-1):
                self.rubans.append(["_"])
            self.etats_rubans= [self.rubans[i][0] for i in range(self.nb_rubans)]
        else:
            self.etats_rubans.append(self.rubans[0][0])
        self.position = [0 for _ in range(self.nb_rubans)]
   
    def pas(self):
        if self.rubans == []:
            print("Veuillez spécifier une entrée")
        if self.etat_courant == "M'":
            for elt in self.dic_etatstrans.items():
                transi = elt[1]
                if transi[0] == "M'":
                    self.etat_courant = transi[1]
                    return True
        for elt in self.dic_etatstrans.items():
            etat = elt[0]
            transi = elt[1]
            etat_courant_comp = "".join([etat[:car] for car in range(len(etat)) if etat[car] == ","])
            if etat_courant_comp == self.etat_courant:
                etats_comp = "".join([etat[car+1:] for car in range(len(etat)) if etat[car] == ","])
                if "".join(self.etats_rubans) == etats_comp and transi[0] != "M'":
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
                    return True
                elif "".join(self.etats_rubans) == etats_comp:
                    self.etat_courant = transi[0]
                    return True
        return False
        
    def lancer_machine(self):
        if self.input == None:
            print("t'as pas précisé d'entrée sale fou")
            return False
        print("Les caractères coloriés correspondent a la position du curseur sur chacun des rubans")
        while self.etat_courant != "F":
            self.afficher()
            res = self.pas()
            if not res:
                print("Le mot que vous avez entré n'est pas reconnu par la machine de turing")
                return False
        print("Voici l'état de la machine dans son état finale")
        self.afficher()

    def afficher(self):
        print("Etat actuelle:",self.etat_courant)
        for ruban in range(self.nb_rubans):
            if self.position[ruban] == 0:
                print("Ruban {} : \033[91m {} \033[0m{}".format(ruban+1,self.rubans[ruban][self.position[ruban]]," ".join(self.rubans[ruban][self.position[ruban]+1:])))
            elif self.position[ruban] == len(self.rubans[ruban]) - 1:
                print("Ruban {} : {} \033[91m{} \033[0m".format(ruban+1," ".join(self.rubans[ruban][:self.position[ruban]]),self.rubans[ruban][self.position[ruban]]))
            else:
                print("Ruban {} : {} \033[91m{}\033[0m {}".format(ruban+1," ".join(self.rubans[ruban][:self.position[ruban]]),self.rubans[ruban][self.position[ruban]]," ".join(self.rubans[ruban][self.position[ruban]+1:])))

    def __str__(self):
        l = "".join(str([self.rubans,self.etats_rubans,self.position,self.etat_courant,self.nb_pas]))
        return l

def create_m3(m1,m2):
    dic1 = m1.get_dic()
    dic2 = m2.get_dic()
    dic3 = {}
    etat_r = []
    i = 0
    for trans in dic1.items():
        if "M'" not in trans[1]:
            dic3[trans[0]] = trans[1]
        else:
            etat_r.append(trans[1][1])
            sep = trans[0].split(",")
            nom_apellei = "".join(["m",str(i),"I"])
            dic3[trans[0]] = [nom_apellei,[sep[1][i] for i in range(len(sep[1]))],["-" for _ in range(m1.get_nb_rub())]]
            i += 1
    for appels in range(i):
        for trans in dic2.items():
            if "F" not in trans[1]:
                #print(trans)
                nv_trans = trans[1][0]
                nom_trans = "".join(["m",str(appels)])
                nv_trans = "".join([nom_trans,nv_trans])
                #print(nv_trans)
                dic3["".join([nom_trans,trans[0]])] = [nv_trans,trans[1][1],trans[1][2]]
                #print("".join([nom_trans,trans[0]]),dic3["".join([nom_trans,trans[0]])])
            else:
                #print(trans,appels)
                nv_trans1 = trans[1][0]
                nv_trans1 = etat_r[appels]
                nom_trans = "".join(["m",str(appels)])
                #print(trans[1])
                dic3["".join([nom_trans,trans[0]])] = [nv_trans1,trans[1][1],trans[1][2]]
    return write_m3(dic3)

def write_m3(dic):
    fichier = open("m3.txt","w")
    for trans in dic.items():
        ligne1 = []
        ligne2 = []
        char = 0
        while trans[0][char] != ",":
            ligne1.append(trans[0][char])
            char += 1
        char += 1
        while char < len(trans[0]):
            ligne1.append(",")
            ligne1.append(trans[0][char])
            char += 1
        ligne2.append(trans[1][0])
        #print(trans)
        ligne2.append(",".join(trans[1][1]))
        ligne2.append(",".join(trans[1][2]))
        fichier.write("".join(ligne1))
        fichier.write("\n")
        fichier.write(",".join(ligne2))
        fichier.write("\n\n")
    fichier.close()
    return Machine("m3.txt")

add = Machine("addition.txt")
mult = Machine("multiplication.txt")
mult_eg = create_m3(mult,add)
mult_eg.entrée("100*0101")
mult_eg.lancer_machine()