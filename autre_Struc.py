# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 16:50:59 2023

@author: Mona CHOUCHANE et Manda RAVELOARISON

"""
import re
import sys


class Token:
    def __init__(self, type_, valeur):
        self.type_ = type_
        self.valeur = valeur


class Noeud:
    def __init__(self, type_, valeur=None, symbole=None):
        self.type = type_
        self.valeur = valeur
        self.enfants = []
        self.symbole = symbole

    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)



class Symbole:
    def __init__(self, nom, type=None, position=None, nbVar=0):
        self.nom = nom
        self.type = type
        self.position = position
        self.nbVar = nbVar


listeToken = []

TableSymbole = []

listeTypeToken = {
    "CONSTANTE": r"[0-9]+",
    "IDENTIFIER": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "PLUS": r"\+",
    "MULT": r"\*",
    "DIV": r"\/",
    "MOINS": r"\-",
    "MODULO": r"\%",
    "PIPE": r"\|",
    "ESPERLUETTE": r"\&",
    "PEXCLAMATION": r"\!",
    "INFERIEUR": r"\<",
    "SUPERIEUR": r"\>",
    "PARENTHG": r"\(",
    "PARENTHD": r"\)",
    "POINTVIRGULE": r"\;",
    "VIRGULE": r"\,",
    "ACCOLOUVRANTE": r"\{",
    "ACCOLFERMANTE": r"\}",
    "CROCHETG": r"\[",
    "CROCHETD": r"\]",
    "AFFECTATION": r"\=",
}

operateur = {
    "AFFECTATION": {"Noeud": "N_AFFECTATION", "Priorite": 1, "Aad": 1},
    "OU": {"Noeud": "N_OU", "Priorite": 2, "Aad": 0},
    "ET": {"Noeud": "N_ET", "Priorite": 3, "Aad": 0},
    "EQUIVALENT": {"Noeud": "N_EQUIVALENT", "Priorite": 4, "Aad": 0},
    "DIFFERENT": {"Noeud": "N_DIFFERENT", "Priorite": 4, "Aad": 0},
    "INFERIEUR": {"Noeud": "N_INFERIEUR", "Priorite": 5, "Aad": 0},
    "INFERIEUROUEGALE": {"Noeud": "N_INFERIEUROUEGALE", "Priorite": 5, "Aad": 0},
    "SUPERIEUR": {"Noeud": "N_SUPERIEUR", "Priorite": 5, "Aad": 0},
    "SUPERIEUROUEGALE": {"Noeud": "N_SUPERIEUROUEGALE", "Priorite": 5, "Aad": 0},
    "PLUS": {"Noeud": "N_PLUS", "Priorite": 6, "Aad": 0},
    "MOINS": {"Noeud": "N_MOINS", "Priorite": 6, "Aad": 0},
    "MULT": {"Noeud": "N_MULT", "Priorite": 7, "Aad": 0},
    "DIV": {"Noeud": "N_DIV", "Priorite": 7, "Aad": 0},
    "MODULO": {"Noeud": "N_MODULO", "Priorite": 7, "Aad": 0},
}


def analyseLexicale(fichier):
    global position
    global codeSource
    with open("./" + fichier, "r", encoding="utf-8") as fichier:
        codeSource = fichier.read().replace("\n", "").replace("\t", "")
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
                                while position + 1 <= len(codeSource) - 1 and (
                                    codeSource[position + 1].isalnum()
                                    or codeSource[position + 1] == "_"
                                ):
                                    position = position + 1
                                    identifier = identifier + str(codeSource[position])
                                if identifier == "if":
                                    token = Token("IF", "if")
                                elif identifier == "else":
                                    token = Token("ELSE", "else")
                                elif identifier == "debug":
                                    token = Token("DEBUG", "debug")
                                elif identifier == "return":
                                    token = Token("RETURN", "return")
                                elif identifier == "int":
                                    token = Token("INT", "int")
                                elif identifier == "while":
                                    token = Token("WHILE", "while")
                                elif identifier == "for":
                                    token = Token("FOR", "for")
                                else:
                                    token = Token(cle, identifier)
                                listeToken.append(token)
                                position = position + 1
                            elif cle == "PIPE":
                                if (
                                    position + 1 <= len(codeSource) - 1
                                    and codeSource[position + 1] == "|"
                                ):
                                    token = Token("OU", "||")
                                    position = position + 2
                                else:
                                    raise ValueError("ERREUR FATALE")
                                listeToken.append(token)
                            elif cle == "ESPERLUETTE":
                                if (
                                    position + 1 <= len(codeSource) - 1
                                    and codeSource[position + 1] == "&"
                                ):
                                    token = Token("ET", "&&")
                                    position = position + 2
                                else:
                                    token = Token("ESPERL", "&")
                                    position = position + 1
                                listeToken.append(token)
                            elif cle == "INFERIEUR":
                                if (
                                    position + 1 <= len(codeSource) - 1
                                    and codeSource[position + 1] == "="
                                ):
                                    token = Token("INFERIEUROUEGALE", "<=")
                                    position = position + 2
                                else:
                                    token = Token("INFERIEUR", "<")
                                    position = position + 1
                                listeToken.append(token)
                            elif cle == "SUPERIEUR":
                                if (
                                    position + 1 <= len(codeSource) - 1
                                    and codeSource[position + 1] == "="
                                ):
                                    token = Token("SUPERIEUROUEGALE", ">=")
                                    position = position + 2
                                else:
                                    token = Token("SUPERIEUR", ">")
                                    position = position + 1
                                listeToken.append(token)
                            elif cle == "PEXCLAMATION":
                                if (
                                    position + 1 <= len(codeSource) - 1
                                    and codeSource[position + 1] == "="
                                ):
                                    token = Token("DIFFERENT", "!=")
                                    position = position + 2
                                else:
                                    token = Token("PEXCLAMATION", "!")
                                    position = position + 1
                                listeToken.append(token)
                            elif cle == "AFFECTATION":
                                if (
                                    position + 1 <= len(codeSource) - 1
                                    and codeSource[position + 1] == "="
                                ):
                                    token = Token("EQUIVALENT", "==")
                                    position = position + 2
                                else:
                                    token = Token("AFFECTATION", "=")
                                    position = position + 1
                                listeToken.append(token)
                            else:
                                token = Token(cle, caractereActuel)
                                listeToken.append(token)
                                position = position + 1
                            break
                    if not caractere_valide_trouve:
                        raise ValueError("ERREUR FATALE")
            except ValueError as e:
                print(e)
                break
        listeToken.append(Token("EOF", "EOF"))


def check(type_):
    global token
    if token.type_ == type_:
        next()
        return True
    else:
        return False


def accept(type_):
    if not check(type_):
        raise ValueError("ERREUR FATALE")


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


def Begin():
    TableSymbole.append((" ", None))


def End():
    for valeur in reversed(TableSymbole):
        if valeur[0] != " ":
            TableSymbole.pop()
            continue
        else:
            break


def Chercher(nom):
    for valeur in reversed(TableSymbole):
        if valeur[0] == nom:
            return valeur[1]
    raise ValueError("ERREUR FATALE")


def Declarer(nom):
    for valeur in reversed(TableSymbole):
        if valeur[0] == nom:
            raise ValueError("ERREUR FATALE")
        if valeur[0] == " ":
            break
    S = Symbole(nom)
    TableSymbole.append((nom, S))
    return S


def atome():
    if check("CONSTANTE"):
        return Noeud("CONSTANTE", last.valeur)
    elif check("IDENTIFIER"):
        return Noeud("N_REFERENCE", last.valeur)
    elif check("PARENTHG"):
        N = expression(0)
        accept("PARENTHD")
        return N
    else:
        raise SyntaxError(f"Atome inattendu: {last.type_}")


def prefixe():
    if check("MOINS"):
        P = prefixe()
        N = Noeud("N_MOINS_UNAIRE", "")
        N.ajouter_enfant(P)
        return N
    elif check("PEXCLAMATION"):
        P = prefixe()
        N = Noeud("N_NOT", "")
        N.ajouter_enfant(P)
        return N
    elif check("PLUS"):
        P = prefixe()
        return P
    elif check("MULT"):
        P = prefixe()
        N = Noeud("N_INDIRECTION", last.valeur)
        N.ajouter_enfant(P)
        return N
    elif check("ESPERL"):
        P = prefixe()
        N = Noeud("N_ADRESSE", last.valeur)
        N.ajouter_enfant(P)
        return N
    else:
        S = suffixe()
        return S


def suffixe():
    A = atome()
    if check("PARENTHG"):
        N = Noeud("N_APPEL", "")
        N.ajouter_enfant(A)
        while not check("PARENTHD"):
            N.ajouter_enfant(expression(0))
            if check("PARENTHD"):
                break
            accept("VIRGULE")
        return N
    elif check("CROCHETG"):
        E = expression(0)
        accept("CROCHETD")
        N = Noeud("N_INDIRECTION", "")
        P = Noeud("N_PLUS", "")
        N.ajouter_enfant(P)
        P.ajouter_enfant(A)
        P.ajouter_enfant(E)
        return N
    else:
        return A


def expression(prioMin):
    N = prefixe()
    while operateur.get(token.type_) is not None:
        op = operateur[token.type_]
        if op["Priorite"] <= prioMin:
            break
        next()
        M = expression(op["Priorite"] - op["Aad"])
        noeud = Noeud(op["Noeud"], "")
        noeud.ajouter_enfant(N)
        noeud.ajouter_enfant(M)
        N = noeud
    return N


def instruction():
    if check("POINTVIRGULE"):
        return Noeud("NOEUD_VIDE", "")
    elif check("ACCOLOUVRANTE"):
        N = Noeud("N_BLOCK", "")
        while not check("ACCOLFERMANTE"):
            N.ajouter_enfant(instruction())
        return N
    elif check("IF"):
        accept("PARENTHG")
        E = expression(0)
        accept("PARENTHD")
        I1 = instruction()
        I2 = None
        if check("ELSE"):
            I2 = instruction()
        N = Noeud("N_COND", "")
        N.ajouter_enfant(E)
        N.ajouter_enfant(I1)
        if I2 is not None:
            N.ajouter_enfant(I2)
        return N
    elif check("DEBUG"):
        E = expression(0)
        accept("POINTVIRGULE")
        N = Noeud("N_DEBUG", "")
        N.ajouter_enfant(E)
        return N
    elif check("RETURN"):
        E = expression(0)
        accept("POINTVIRGULE")
        N = Noeud("N_RETURN", "")
        N.ajouter_enfant(E)
        return N
    elif check("INT"):
        N = Noeud("N_SEQUENCE", "")
        while True:
            accept("IDENTIFIER")
            N.ajouter_enfant(Noeud("N_DECLARE", last.valeur))
            if not check("VIRGULE"):
                break
        accept("POINTVIRGULE")
        return N
    elif check("WHILE"):
        accept("PARENTHG")
        E = expression(0)
        accept("PARENTHD")
        I = instruction()
        L = Noeud("N_LOOP", "")
        T = Noeud("N_TARGET", "")
        C = Noeud("N_COND", "")
        B = Noeud("N_BREAK", "")
        L.ajouter_enfant(T)
        L.ajouter_enfant(C)
        C.ajouter_enfant(E)
        C.ajouter_enfant(I)
        C.ajouter_enfant(B)
        return L
    elif check("FOR"):
        accept("PARENTHG")
        E1 = expression(0)
        accept("POINTVIRGULE")
        E2 = expression(0)
        accept("POINTVIRGULE")
        E3 = expression(0)
        accept("PARENTHD")
        I = instruction()
        S1 = Noeud("N_SEQUENCE", "")
        D1 = Noeud("N_DROP", " ")
        L = Noeud("N_LOOP", "")
        C = Noeud("N_COND", "")
        S2 = Noeud("N_SEQUENCE", "")
        T = Noeud("N_TARGET", "")
        D2 = Noeud("N_DROP", "")
        B = Noeud("N_BREAK", "")
        D2.ajouter_enfant(E3)
        S2.ajouter_enfant(I)
        S2.ajouter_enfant(T)
        S2.ajouter_enfant(D2)
        C.ajouter_enfant(E2)
        C.ajouter_enfant(S2)
        C.ajouter_enfant(B)
        L.ajouter_enfant(C)
        D1.ajouter_enfant(E1)
        S1.ajouter_enfant(D1)
        S1.ajouter_enfant(L)
        return S1
    else:
        N = expression(0)
        accept("POINTVIRGULE")
        D = Noeud("N_DROP", "")
        D.ajouter_enfant(N)
        return D


def analyseSyntaxique():
    accept("INT")
    accept("IDENTIFIER")
    N = Noeud("N_FONCTION", last.valeur)
    accept("PARENTHG")
    while check("INT"):
        accept("IDENTIFIER")
        N.ajouter_enfant(Noeud("N_DECLARE", last.valeur))
        if check("VIRGULE"):
            continue
        break
    accept("PARENTHD")
    i = instruction()
    N.ajouter_enfant(i)
    return N


def genecode(N):
    global nbLabel
    global labelContinue
    global labelBreak
    if N.type == "CONSTANTE":
        print(f"push {N.valeur}")
    elif N.type == "N_MOINS_UNAIRE":
        print("push 0")
        print("push " + N.enfants[0].valeur)
        print("sub")
    elif N.type == "NOT":
        genecode(N.enfants[0])
        print("not")
    elif N.type == "IDENTIFIER":
        pass
    elif N.type in [
        "N_PLUS",
        "N_MOINS",
        "N_MULT",
        "N_DIV",
        "N_MODULO",
        "N_EQUIVALENT",
        "N_DIFFERENT",
        "N_INFERIEUR",
        "N_INFERIEUROUEGALE",
        "N_SUPERIEUR",
        "N_SUPERIEUROUEGALE",
        "N_ET",
        "N_OU",
    ]:
        operation = ""
        if N.type == "N_PLUS":
            operation = "add"
        elif N.type == "N_MOINS":
            operation = "sub"
        elif N.type == "N_MULT":
            operation = "mul"
        elif N.type == "N_DIV":
            operation = "div"
        elif N.type == "N_MODULO":
            operation = "mod"
        elif N.type == "N_EQUIVALENT":
            operation = "cmpeq"
        elif N.type == "N_DIFFERENT":
            operation = "cmpne"
        elif N.type == "N_INFERIEUR":
            operation = "cmplt"
        elif N.type == "N_INFERIEUROUEGALE":
            operation = "cmple"
        elif N.type == "N_SUPERIEUR":
            operation = "cmpgt"
        elif N.type == "N_SUPERIEUROUEGALE":
            operation = "cmpge"
        elif N.type == "N_OU":
            operation = "or"
        elif N.type == "N_ET":
            operation = "and"
        genecode(N.enfants[0])
        genecode(N.enfants[1])
        print(f"{operation}")
    elif N.type == "N_DROP":
        genecode(N.enfants[0])
        print("drop 1")
    elif N.type == "N_DEBUG":
        genecode(N.enfants[0])
        print("dbg")
    elif N.type == "N_RETURN":
        genecode(N.enfants[0])
        print("ret")
    elif N.type == "N_APPEL":
        if N.enfants[0].type != "N_REFERENCE":
            raise ValueError("ERREUR FATALE")
        if N.enfants[0].symbole.type != "FONCTION":
            raise ValueError("ERREUR FATALE")
        print("prep " + str(N.enfants[0].valeur))
        for idx, enfant in enumerate(N.enfants):
            if idx == 0:
                continue
            genecode(enfant)
        print("call " + str(len(N.enfants) - 1))

    elif N.type == "N_DECLARE":
        pass
    elif N.type == "N_BLOCK":
        for enfant in N.enfants:
            genecode(enfant)
    elif N.type == "N_SEQUENCE":
        for enfant in N.enfants:
            genecode(enfant)
    elif N.type == "N_REFERENCE":
        if N.symbole.type == "VARLOC":
            print("get " + str(N.symbole.position))
        else:
            raise ValueError("ERREUR FATALE")
    elif N.type == "N_AFFECTATION":
        genecode(N.enfants[1])
        print("dup")
        if N.enfants[0].type == "N_REFERENCE":
            print("set " + str(N.enfants[0].symbole.position))
        elif N.enfants[0].type == "N_INDIRECTION":
            genecode(N.enfants[0].enfants[0])
            print("write")
        else:
            raise ValueError("ERREUR FATALE")
    elif N.type == "N_COND":
        l1 = 0
        l2 = 0
        if len(N.enfants) == 2:
            l1 = nbLabel
            nbLabel = nbLabel + 1
            genecode(N.enfants[0])
            print("jumpf l" + str(l1))
            genecode(N.enfants[1])
            print(".l" + str(l1))
        else:
            l1 = nbLabel
            nbLabel = nbLabel + 1
            l2 = nbLabel
            nbLabel = nbLabel + 1
            genecode(N.enfants[0])
            print("jumpf l" + str(l1))
            genecode(N.enfants[1])
            print("jump l" + str(l2))
            print(".l" + str(l1))
            genecode(N.enfants[2])
            print(".l" + str(l2))
    elif N.type == "N_TARGET":
        print(".l" + str(labelContinue))
    elif N.type == "N_BREAK":
        print("jump l" + str(labelBreak))
    elif N.type == "N_CONTINUE":
        print("jump l" + str(labelContinue))
    elif N.type == "N_LOOP":
        labelDebut = nbLabel
        nbLabel = nbLabel + 1
        saveContinue = labelContinue
        labelContinue = nbLabel
        nbLabel = nbLabel + 1
        labelBreak = nbLabel
        nbLabel = nbLabel + 1
        print(".l" + str(labelDebut))
        for enfant in N.enfants:
            genecode(enfant)
        print("jump l" + str(labelDebut))
        print(".l" + str(labelBreak))
        labelContinue = saveContinue
    elif N.type == "N_FONCTION":
        print("." + str(N.valeur))
        print("resn " + str(N.symbole.nbVar))
        genecode(N.enfants[-1])
        print("push 0")
        print("ret")
    elif N.type == "N_INDIRECTION":
        genecode(N.enfants[0])
        print("read")
    elif N.type == "N_ADRESSE":
        if N.enfants[0].type != "N_REFERENCE" and N.enfants[0].symbole.type == "VARLOC":
            raise ValueError("ERREUR FATALE")
        print("prep start")
        print("swap")
        print("drop 1")
        print("push", N.enfants[0].symbole.position + 1)
        print("sub")


def analyseSemantique(Noeud):
    global nbVar
    match Noeud.type:
        case "N_BLOCK":
            Begin()
            for enfant in Noeud.enfants:
                analyseSemantique(enfant)
            End()
        case "N_DECLARE":
            S = Declarer(Noeud.valeur)
            S.position = nbVar
            nbVar = nbVar + 1
            S.type = "VARLOC"
        case "N_REFERENCE":
            S = Chercher(Noeud.valeur)
            Noeud.symbole = S
        case "N_FONCTION":
            nbVar = 0
            S = Declarer(Noeud.valeur)
            Begin()
            for enfant in Noeud.enfants:
                analyseSemantique(enfant)
            End()
            S.type = "FONCTION"
            S.nbVar = nbVar - (len(Noeud.enfants) - 1)
            Noeud.symbole = S
        case _:
            for enfant in Noeud.enfants:
                analyseSemantique(enfant)


def compile(fichier):
    try:
        compile_fichier("lib.c")
        global position
        position = 0
        compile_fichier(fichier)
        print(".start")
        print("prep init")
        print("call 0")
        print("prep main")
        print("call 0")
        print("halt")
    except ValueError as e:
        print(e)


def compile_fichier(fichier):
    analyseLexicale(fichier)
    next()
    while token.type_ != "EOF":
        A = analyseSyntaxique()
        analyseSemantique(A)
        genecode(A)


codeSource = ""
position = 0
positionListeToken = 0
token = Token("", "")
last = Token("", "")
nbVar = 0
nbLabel = 0
labelContinue = 0
labelBreak = 0

if len(sys.argv) < 2:
    print("Veuillez spécifier le fichier en argument.")
    sys.exit(1)
fichier = sys.argv[1]
compile(fichier)
