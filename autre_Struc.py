# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 16:50:59 2023

@author: Mona CHOUCHANE et Manda RAVELOARISON

"""
import re


class Token:
    def __init__(self, type_, valeur):
        self.type_ = type_
        self.valeur = valeur


class Noeud:
    def __init__(self, type_, valeur=None):
        self.type = type_
        self.valeur = valeur
        self.enfants = []

    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)

    def afficher(self, niveau=0):
        indent = "  " * niveau
        print(f"{indent}{self.type}: {self.valeur}")
        for enfant in self.enfants:
            enfant.afficher(niveau + 1)



listeToken = []

listeTypeToken = {
    "CONSTANTE": r"[0-9]+",
    "IDENTIFIER": r"\b[a-zA-Z][a-zA-Z0-9]*\b",
    "PLUS": r"\+",
    "MULT": r"\*",
    "DIV": r"\/",
    "MOINS": r"\-",
    "PEXCLAMATION": r"\!",
    "PARENTHG": r"\(",
    "PARENTHD": r"\)",
    "POINTVIRGULE": r"\;",
    "ACCOLOUVRANTE": r"\{",
    "ACCOLFERMANTE": r"\}",
}


def check(type_):
    global token
    if token.type_ == type_:
        next()
        return True
    else:
        return False


def accept(type_):
    if not check(type_):
        raise ValueError("Erreur Fatal", type_, token.type_)


def next():
    global positionListeToken
    global token
    global last
    if positionListeToken == 0:
        token = listeToken[positionListeToken]
    elif positionListeToken > 0 and positionListeToken <= len(listeToken) - 1:
        token = listeToken[positionListeToken]
        last = listeToken[positionListeToken - 1]
    positionListeToken = positionListeToken + 1


def analyseLexicale():
    global position
    global codeSource
    with open("code.txt", "r", encoding="utf-8") as fichier:
        codeSource = fichier.read()
        while position <= len(codeSource) - 1:
            try:
                caractereActuel = codeSource[position]
                if caractereActuel == " ":
                    position = position + 1
                    continue
                else:
                    caractere_valide_trouve = False
                    for cle, valeur in listeTypeToken.items():
                        if re.match(valeur, caractereActuel):
                            caractere_valide_trouve = True
                            if cle == "CONSTANTE":
                                constante = str(caractereActuel)
                                while (
                                    position + 1 <= len(codeSource) - 1
                                    and codeSource[position + 1].isnumeric()
                                ):
                                    position = position + 1
                                    constante = constante + str(codeSource[position])
                                token = Token(cle, constante)
                                listeToken.append(token)
                                position = position + 1
                            elif cle == "IDENTIFIER":
                                identifier = caractereActuel
                                while (
                                    position + 1 <= len(codeSource) - 1
                                    and codeSource[position + 1].isalnum()
                                ):
                                    position = position + 1
                                    identifier = identifier + str(codeSource[position])
                                token = Token(cle, identifier)
                                listeToken.append(token)
                                position = position + 1
                            else:
                                token = Token(cle, caractereActuel)
                                listeToken.append(token)
                                position = position + 1
                            break
                    if not caractere_valide_trouve:
                        raise ValueError(
                            "Erreur: caractère inconnu ('" + caractereActuel + "')"
                        )
            except ValueError as e:
                print(e)
                break
        listeToken.append(Token("EOF", "EOF"))


def atome():
    if check("CONSTANTE"):
        return Noeud("CONSTANTE", last.valeur)
    elif check("IDENTIFIER"):
        return Noeud("IDENTIFIER", last.valeur)
    elif check("PARENTHG"): 
        N = expression()
        accept("PARENTHD")
        return N
    else:
        raise SyntaxError(f"Atome inattendu: {last.type_}")


def prefixe():
    if check("MOINS"):
        N = prefixe()
        return Noeud("N_MOINS_UNAIRE", N)
    elif check("PEXCLAMATION"):
        N = prefixe()
        return Noeud("N_NOT", N)
    elif check("PLUS"):
        N = prefixe()
        return N
    else:
        N = atome()
        return N


def expression():
    noeud = prefixe()
    while token.type_ in {"PLUS", "MOINS", "MULT", "DIV"}:
        op = token
        noeud_droit = prefixe()
        noeud_gauche = noeud
        noeud = Noeud("BINAIRE", op.valeur)
        noeud.ajouter_enfant(noeud_gauche)
        noeud.ajouter_enfant(noeud_droit)
    return noeud

def instruction():
    if check("POINTVIRGULE"):
        return Noeud("NOEUD_VIDE", "")
    elif check("ACCOLOUVRANTE"):
        N = Noeud("NOEUD_BLOCK", "")
        while not check("ACCOLFERMANTE"):
            N.ajouter_enfant(instruction())
        return N
    else:
        N = expression()
        accept("POINTVIRGULE")
        return N
    
def analyseSyntaxique():
    return instruction()

def genecode(self):
    if self.type == "CONSTANTE":
        return [f"push {self.valeur}"]
    elif self.type == "MOINS_UNAIRE":
        codeOperation = self.enfants[0].genecode()
        return ["push 0"] + codeOperation 
    elif self.type == "NOT":
        return ["push 0"]
    elif self.type == "IDENTIFIER":
        pass
    elif self.type == "BINAIRE":
        instructions_gauche = self.enfants[0].genecode()
        instructions_droite = self.enfants[1].genecode()
        if self.valeur == "+":
            operation = "ADD"
        elif self.valeur == "-":
            operation = "SUB"
        elif self.valeur == "*":
            operation = "MUL"
        elif self.valeur == "/":
            operation = "DIV"
        return instructions_gauche + instructions_droite + [f"push {operation}"]
    else:
        raise ValueError("Type de nœud inconnu")
    pass
# def analyseSemantique(Noeud):
#    nbVar, nbVal = 0
#    if(Noeud.type == NdDeclare):
#       S = declare(N.valeur);
#        S.position = nbVar
#        nbVar = nbVar + 1
#        S.type = varLocale
#    elif(Noeud.type == NdRef):
#            S = chercher(N.valeur)
#            S.position = nbVal
#            nbVal = nbVal + 1
#            S.type = valLocale
#    else:
#        for E in N.enfants:
#            analyseSemantique(E)
    
codeSource = ""
position = 0
positionListeToken = 0
token = Token("", "")
last = Token("", "")
analyseLexicale()
next()
print("Liste des tokens :")
for x in listeToken:
    print(x.type_ + " " + x.valeur)
print()
print("Arbre de token :")
A = analyseSyntaxique()
A.afficher()
#print("Generation du code :")
#assembleur = racine.genecode()
#for instructions in assembleur:
    #print(instructions)
#analyseSyntaxique()
