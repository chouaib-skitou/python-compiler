EOF = 'EOF'

TOKEN_TYPES = {
    'CONSTANT': 'CONSTANT',
    'PLUS': 'PLUS',
    'MINUS': 'MINUS',
    'MUL': 'MUL',
    'DIV': 'DIV',
    'EOF': EOF,
    'CLOSE_PAREN': 'CLOSE_PAREN',
    'OPEN_PAREN': 'OPEN_PAREN',
    'MOD': 'MOD',
    'IDENTIFIER': 'IDENTIFIER',
    'OR': 'OR',
    'AND': 'AND',
    'NOT': 'NOT',
    'AFFECTATION': 'AFFECTATION',
    'EQUAL': 'EQUAL',
    'NOT_EQUAL': 'NOT_EQUAL',
    'LESS_THAN': 'LESS_THAN',
    'LESS_THAN_EQUAL': 'LESS_THAN_EQUAL',
    'GREATER_THAN': 'GREATER_THAN',
    'GREATER_THAN_EQUAL': 'GREATER_THAN_EQUAL',
    'Point_virgule' : 'Point_virgule', # Ajout du token ; pour pouvoir gérer les instructions
    'CLOSE_ACCOLADE': 'CLOSE_ACCOLADE',
    'OPEN_ACCOLADE': 'OPEN_ACCOLADE',
    'DEBUG': 'DEBUG',

}
NODES_TYPES = {
    'Node_IDENTIFIER': 'Node_IDENTIFIER',
    'Node_CONSTANT': 'Node_CONSTANT',
    'Node_MINUS_UNARY': 'Node_MINUS_UNARY',
    'UNAIRE': '!',
    'BINAIRE': '-',
    'BINAIRE': '+',
    'BINAIRE' : '*',
    'BINAIRE' : '/',
    'BINAIRE' : '%',
    # Pour les instructions
    'Node_Empty' : 'Node_Empty',
    'Node_Block' : 'Node_Block',
    'Node_Debug' : 'Node_Debug',
    'Node_Drop' : 'Node_Drop',
    #Pour les variables
    'Node_Seq' : 'Node_Seq',
    'Node_Decla' : 'Node_Decla',
    'Node_Ref' : 'Node_Ref',
    'Node_Affectation' : 'Node_Affectation',


}
MOTS_CLES = {
    'int': 'int',
    'while': 'while',
    'if': 'if',
    'else': 'else',
    'return': 'return',
    'main': 'main',
    'void': 'void',
    'char': 'char',
    'float': 'float',
    'double': 'double',
    'for': 'for',
    'do': 'do',
    'switch': 'switch',
    'case': 'case',
    'break': 'break',
    'continue': 'continue',
    'struct': 'struct',
    'typedef': 'typedef',
    'enum': 'enum',
    'unsigned': 'unsigned',
    'long': 'long',
    'short': 'short',
    'signed': 'signed',
}



#Table des symboles, forme (nom de variable : Symbole de la variable)
TAB_SYMBOLE = dict()

class Symbole:
    def __init__(self, nom,type,position,nVar):
        self.nom = nom
        self.type = type # Les seuls types existant sont Fonction et VarLoc
        self.position = position
        self.nVar = nVar

    def affiche(self):
        print("SYMBOLE : nom : " + self.nom+" type : "+self.type+" position : "+self.position+" nVar : "+self.nVar)

class ValOpe:
    def __init__(self, nde, priority, AaD):
        self.nde = nde #type du noeud
        self.priority =priority #priorité de l'opération
        self.AaD = AaD # si l'opération est associative à droite, la valeur est de 1

# Table des Opérateurs avec les priorités
OPERATORS = {
    TOKEN_TYPES['PLUS']: ValOpe('BINAIRE',6,0),
    TOKEN_TYPES['MINUS']: ValOpe('Node_MINUS_BINAIRE',6,0),
    TOKEN_TYPES['MUL']: ValOpe('Node_MUL',7,0),
    TOKEN_TYPES['DIV']: ValOpe('Node_DIV',7,0),
    TOKEN_TYPES['MOD']: ValOpe('Node_MOD',7,0),
    TOKEN_TYPES['AFFECTATION']: ValOpe('Node_AFFECTATION',1,1),
    TOKEN_TYPES['OR']: ValOpe('Node_OR',2,0),
    TOKEN_TYPES['AND']: ValOpe('Node_AND',3,0),
    TOKEN_TYPES['EQUAL']: ValOpe('Node_EQUAL',4,0),
    TOKEN_TYPES['NOT_EQUAL']: ValOpe('Node_NOT_EQUAL',4,0),
    TOKEN_TYPES['GREATER_THAN']: ValOpe('Node_GREATER_THAN',5,0),
    TOKEN_TYPES['LESS_THAN']: ValOpe('Node_LESS_THAN',5,0),

}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def get_type(self):
        return self.type
    
    def get_value(self):
        return self.value

    def affiche(self):
        print("Le token est de type : ", self.type, " et sa valeur est : ", self.value)

    
class Node:
    symbole = None #par défaut on met symbole à None, car il ne concerne que les Noeud Ref
    def __init__(self, type, value,symbole):
        self.type = type
        self.value = value
        self.children = []
        self.symbole = symbole # Ajout de symbole dans les noeuds
    
    def get_type(self):
        return self.type
    
    def get_value(self):
        return self.value

    def get_children(self):
        return self.children

    def affiche(self):
        print("Le noeud est de type : ", self.type, " et sa valeur est : ", self.value)
        for child in self.children:
            child.affiche()
    def genecode(self):
        if self.type == "Node_CONSTANT":
            return [f"push {self.value}"]
        elif self.type == "Node_IDENTIFIER":
            return [f"push {self.value}"]
        elif self.type == "UNAIRE":
            if self.valeur == "!":
                genecode_enfant0 = self.children[0].genecode()
                return genecode_enfant0 + [f"not"]
        elif self.type == "BINAIRE":
            genecode_enfant0 = self.children[0].genecode()
            genecode_enfant1 = self.children[1].genecode()
            if self.value == "+":
                operation = "ADD"
            elif self.value == "-":
                operation = "SUB"
            elif self.value == "*":
                operation = "MUL"
            elif self.value == "/":
                operation = "DIV"
            return genecode_enfant0 + genecode_enfant1 + [f"push {operation}"]
        elif self.type == "Node_Debug":
            genecode_enfant = self.children[0].genecode()
            return genecode_enfant + [f"push dbg"]
        elif self.type == "Node_Drop":
            genecode_enfant = self.children[0].genecode()
            return genecode_enfant + [f"drop 1"]
        elif self.type == "Node_Decla":
            break
        elif self.type == "Node_Block" or self.type == "Node_Seq" :
            for child in self.children:
                child.genecode()
        else:
            self.affiche()
            raise ValueError("Type de nœud inconnu")

tokenG = Token(' ',0) #token courant
last = Token(' ',1) #token précédent 
Token_tab =[]

def AnaLex(chaine):   
    position = 0

    while (position < len(chaine)) : #tant qu'on est pas arrivé à la fin de la chaine, on incrémente position
        c = chaine[position]

        if c.isspace():
            position += 1
            continue  # Skip spaces
        elif c.isdigit():
            constant_value = c
            position += 1
            while position < len(chaine) and chaine[position].isdigit():
                constant_value += chaine[position]
                position += 1
            tokenG = Token(TOKEN_TYPES['CONSTANT'], constant_value)
        elif c == '+':
            tokenG = Token(TOKEN_TYPES['PLUS'], c)
        elif c == '-':
            tokenG = Token(TOKEN_TYPES['MINUS'], c)
        elif c == ';':
            tokenG = Token(TOKEN_TYPES['Point_virgule'], c)
        elif c == '*':
            tokenG = Token(TOKEN_TYPES['MUL'], c)
        elif c == '/':
            tokenG = Token(TOKEN_TYPES['DIV'], c)
        elif c == '%':
            tokenG = Token(TOKEN_TYPES['MOD'], c)
        elif c == '=':
            next_char = chaine[position + 1] if position + 1 < len(chaine) else None
            if next_char == '=':
                tokenG = Token(TOKEN_TYPES['EQUAL'], '==')
                position += 2
            else:
                tokenG = Token(TOKEN_TYPES['AFFECTATION'], c)
        elif c == '!':
            next_char = chaine[position + 1] if position + 1 < len(chaine) else None
            if next_char == '=':
                tokenG = Token(TOKEN_TYPES['NOT_EQUAL'], '!=')
                position += 2
            else:
                tokenG = Token(TOKEN_TYPES['NOT'], '!')
        elif c == '|':
            next_char = chaine[position + 1] if position + 1 < len(chaine) else None
            if next_char == '|':
                tokenG = Token(TOKEN_TYPES['OR'], '||')
                position += 2
            else:
                raise Exception("Le token est invalide")
        elif c == '&':
            next_char = chaine[position + 1] if position + 1 < len(chaine) else None
            if next_char == '&':
                tokenG = Token(TOKEN_TYPES['AND'], '&&')
                position += 2
            else:
                raise Exception("Le token est invalide")
        elif c == '<':
            next_char = chaine[position + 1] if position + 1 < len(chaine) else None
            if next_char == '=':
                tokenG = Token(TOKEN_TYPES['LESS_THAN_EQUAL'], '<=')
                position += 2
            else:
                tokenG = Token(TOKEN_TYPES['LESS_THAN'], c)
        elif c == '>':
            next_char = chaine[position + 1] if position + 1 < len(chaine) else None
            if next_char == '=':
                tokenG = Token(TOKEN_TYPES['GREATER_THAN_EQUAL'], '<=')
                position += 2
            else:
                tokenG = Token(TOKEN_TYPES['GREATER_THAN'], c)
        elif c == '(':
            tokenG = Token(TOKEN_TYPES['OPEN_PAREN'], c)
        elif c == ')':
            tokenG = Token(TOKEN_TYPES['CLOSE_PAREN'], c)
        elif c == '{':
            tokenG = Token(TOKEN_TYPES['OPEN_ACCOLADE'], c)
        elif c == '}':
            tokenG = Token(TOKEN_TYPES['CLOSE_ACCOLADE'], c)
        elif c == 'dbg':
            tokenG = Token(TOKEN_TYPES['DEBUG'], c)
        elif c.isalnum():
            identifier_value = c
            position += 1
            while position < len(chaine) and (chaine[position].isalnum() or chaine[position] == '_'):
                identifier_value += chaine[position]
                position += 1
            if identifier_value in MOTS_CLES:
                tokenG = Token(MOTS_CLES[identifier_value], identifier_value)
            else:
                tokenG = Token(TOKEN_TYPES['IDENTIFIER'], identifier_value)
        else:
            raise Exception("Le token est invalid")
        
        position = position + 1
        global Token_tab
        Token_tab.append(tokenG)

    Token_tab.append(Token("EOF",None))

positionToken_tab = 0
def next():
    global positionToken_tab
    global tokenG
    global last
    if positionToken_tab == 0:
        tokenG = Token_tab[positionToken_tab]
    elif positionToken_tab > 0 and positionToken_tab <= len(Token_tab) - 1:
        tokenG = Token_tab[positionToken_tab]
        last = Token_tab[positionToken_tab - 1]
    positionToken_tab = positionToken_tab + 1
    tokenG.affiche() #affichage du token en cours


def check(token_type):
    if(tokenG.type == TOKEN_TYPES[token_type]):
        next()
        return True
    else :
        return False

def accept(token_type):
    if not check(token_type):
        raise Exception("Le token est invalid  : " + str(token_type))

def Atome():
    if(check(TOKEN_TYPES['CONSTANT'])) :
        return Node(NODES_TYPES["Node_CONSTANT"],last.value)
    # elif(check(TOKEN_TYPES['IDENTIFIER'])):
    #     return Node(NODES_TYPES["Node_IDENTIFIER"],last.value)
    #Gestion des variables
    elif(check(TOKEN_TYPES['IDENTIFIER'])):
        return Node(NODES_TYPES["Node_Ref"],last.value)
    elif(check(TOKEN_TYPES['OPEN_PAREN'])):
        N = expression()
        while(last.type != TOKEN_TYPES['CLOSE_PAREN']):
            next()
        return N
    else :
        raise Exception("Token invalid !!!")


# def prefix():
#     if(check(TOKEN_TYPES['MINUS'])) :
#         N = prefix() 
#         return Node(NODES_TYPES["Node_MINUS_UNAIRY"],N)

#     elif(check(TOKEN_TYPES['NOT'])) :
#         N = prefix()
#         return Node(NODES_TYPES["Node_NOT"],N)

#     elif(check(TOKEN_TYPES['PLUS'])) :
#         N = prefix()
#         return N
#     else :
#         N = Atome()
#         return N


def prefix():

    if(check(TOKEN_TYPES['NOT'])) :
        N = prefix()
        L = Node(NODES_TYPES["UNAIRE"],None)
        L.children.append(N)
        return L

    elif(check(TOKEN_TYPES['PLUS'])) :
        N = prefix()
        return N
    elif(check(TOKEN_TYPES['MINUS'])) :
        N = prefix()
        return N
    elif(check(TOKEN_TYPES['MUL'])) :
        N = prefix()
        return N
    elif(check(TOKEN_TYPES['DIV'])) :
        N = prefix()
        return N
    else :
        N = Atome()
        return N

# Fonction pour analyser les expressions
def expression():
    noeud = prefix()
    while tokenG.type in OPERATORS:
        op = tokenG
        noeud_droit = prefix()
        noeud_gauche = noeud
        noeud = Node("BINAIRE", op.value)
        noeud.children.append(noeud_gauche)
        noeud.children.append(noeud_droit)
    return noeud

# Fonction des gestions des instructions, pour le moment pas encore adapté à notre nouvelle structure
def instruction():
    c = ','
    if(check(TOKEN_TYPES['Point_virgule'])) :
        return Node(NODES_TYPES["Node_Empty"],None)
    elif(check(TOKEN_TYPES['OPEN_ACCOLADE'])):
        N = Node(NODES_TYPES["Node_Block"],None)
        while(not check(TOKEN_TYPES['CLOSE_ACCOLADE'])):
            N.children.append(instruction())
        return N
    elif(check(TOKEN_TYPES['DEBUG'])):
        N = expression()
        accept(TOKEN_TYPES['Point_virgule'])
        return Node(NODES_TYPES["Node_Debug"],None)
    #Gestion des variables
    elif(check(TOKEN_TYPES['IDENTIFIER'])):
        N = Node(NODES_TYPES['Node_Seq'],None)
        while(c == ','):
            accept(TOKEN_TYPES['IDENTIFIER'])
            N.children.append(Node(NODES_TYPES['Node_Decla'],last.value))
        accept(TOKEN_TYPES['Point_virgule'])
        return N
    else: # le cas d'une expression suivit d'un point virgule
        N = expression()
        accept(TOKEN_TYPES['Point_virgule'])
        L = Node(NODES_TYPES["Node_Drop"],None)
        L.children.append(N)
        return L


def Begin():
    TAB_SYMBOLE.append(" ",None) #Ajout d'un élement dans la pile pour annoncer le début d'un bloc

def End():
    for element in TAB_SYMBOLE.keys():
        while(element != " "): #suppression des élements de la pile jusqu'au bloc suivant
            TAB_SYMBOLE.pop(element)

# Fonction pour les variables
def Declare(nom):
    global TAB_SYMBOLE
    for element in TAB_SYMBOLE.keys():
        if(element == nom): # si le nom de la var est déjà dans la pile on retourne une erreur
            raise Exception("Token invalid !!!")
        if(element == " "): # si c'est le début d'un bloc, on sort de la fonction
            break
        S = Symbole(nom,"VarLoc",None,None) # sinon, on crée un symbole et on remplie la pile
        TAB_SYMBOLE.append(nom,S) #Ajout du couple (nom,Symbole) dans la pile
        return S


def Chercher():
    global TAB_SYMBOLE
    for element in TAB_SYMBOLE.keys(): # si la variable est dans la pile, on retourne sont symbole
        if(element == nom):
            return TAB_SYMBOLE[element]
nbVar = 0
def AnaSem(N):
    global nbVar
    if(N.type == 'Node_Block'):
        Begin()
        for child in N.children:
            AnaSem(child)
        End()
    elif(N.type == 'Node_Decla'):
        S = Declare(N.valeur)
        S.position = nbVar
        nbVar += 1
        S.type = "VarLoc"
    elif(N.type == 'Node_Ref'):
        S = Chercher(N.valeur)
        N.symbole = S
    else:
        for e in N.children:
            AnaSem(e)




# def Expression(Prio_min): #Parseur de Brat, gestions des associativités et des priorités
#     N = prefix()
#     if(tokenG.type == 'EOF'):
#         return N
#     while(OPERATORS[tokenG.type] in OPERATORS):
#         Op = OPERATORS[tokenG.type]
#         if(Op.priority <= Prio_min) :
#             break
#         else:
#             next()
#             M = Expression(Op.priority - Op.AaD)
#             L = Node(Op.nde)
#             L.children[0] = N
#             L.children[1] = M
#             N = L
#     return N
        
# def  Genecode(N):
#     if N.type == 'Node_CONSTANT' :
#         print("push",N.value)
#     elif N.type == 'Node_NOT' :
#         Gencode(N.children[0])
#         print("not")
#     elif N.type == "BINAIRE" :
#         Genecode(N.children[0])
#         Genecode(N.children[1])
#         if N.value == '-':
#             print("sub")
#         elif N.value == '*':
#             print("mul")
#         elif N.value == '/':
#             print("div")
#         elif N.value == '%':
#             print("mod")
#         elif N.value == '+':
#             print("add")
#     N.affiche()


def AnaSyn():
    return instruction() #expression()  

# Main program
def main():
    with open('test_1.txt', 'r') as file: # ouverture du fichier
        text = file.read()
        AnaLex(text) #initialisation de l'analyse Lexicale
        next() #Appel à la fonction next
        while(tokenG.type != "EOF"):
            A = AnaSyn() # Analyse Synthaxique
            # Affichage de l'arbre
            A.affiche()
            assembleur = A.genecode() 
            for instruction in assembleur :
                # Affichage du code
                print(instruction)


if __name__ == '__main__':
    main()