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
    'VIRGULE': 'VIRGULE',
    "int": "int",
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
    'Node_Cond' : 'Node_Cond',
    #Pour les variables
    'Node_Seq' : 'Node_Seq',
    'Node_Decla' : 'Node_Decla',
    'Node_Ref' : 'Node_Ref',
    'Node_Affectation' : 'Node_Affectation',
    'Node_OR' : '||',
    'Node_AND' : '&&',
    'Node_EQUAL' : '==',
    'Node_NOT_EQUAL' : '!=',
    'Node_GREATER_THAN' : '>',
    'Node_LESS_THAN' : '<',
}

MOTS_CLES = {
    "int": "int",
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



#Table des symboles, dans laquelle on mettra des tuples de la forme (nom de variable : Symbole de la variable)
TAB_SYMBOLE = []

class Symbole:
    def __init__(self, nom,type,position,nVar):
        self.nom = nom
        self.type = type # Les seuls types existant sont Fonction et VarLoc
        self.position = position
        self.nVar = nVar

    def affiche(self):
        print("SYMBOLE : nom : " , self.nom , " type : " , self.type , " position : " , self.position ," nVar : " ,self.nVar)

class ValOpe:
    def __init__(self, ndeType,ndeVal,ndeSymb, priority, AaD):
        self.ndeType = ndeType #type du noeud
        self.ndeVal = ndeVal #valeur du noeud
        self.ndeSymb = ndeSymb #symbole du noeud
        self.priority =priority #priorité de l'opération
        self.AaD = AaD # si l'opération est associative à droite, la valeur est de 1

# Table des Opérateurs avec les priorités
OPERATORS = {
    TOKEN_TYPES['PLUS']: ValOpe('BINAIRE','+',None,6,0),
    TOKEN_TYPES['MINUS']: ValOpe('BINAIRE','-',None,6,0),
    TOKEN_TYPES['MUL']: ValOpe('BINAIRE','*',None,7,0),
    TOKEN_TYPES['DIV']: ValOpe('BINAIRE','/',None,7,0),
    TOKEN_TYPES['MOD']: ValOpe('BINAIRE','%',None,7,0),
    TOKEN_TYPES['AFFECTATION']: ValOpe('Node_Affectation','=',None,1,1),  
    TOKEN_TYPES['OR']: ValOpe('Node_OR','||',None,2,0),
    TOKEN_TYPES['AND']: ValOpe('Node_AND','&&',None,3,0),
    TOKEN_TYPES['EQUAL']: ValOpe('Node_EQUAL','==',None,4,0),
    TOKEN_TYPES['NOT_EQUAL']: ValOpe('Node_NOT_EQUAL','!=',None,4,0),
    TOKEN_TYPES['GREATER_THAN']: ValOpe('Node_GREATER_THAN','>',None,5,0),
    TOKEN_TYPES['LESS_THAN']: ValOpe('Node_LESS_THAN','<',None,5,0),
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
    def __init__(self, type, value = None, symbole = None):
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

    # def affiche(self):
    #     if(self.symbole == None):
    #         print("Noeud de type : ", self.type, ", Valeur est : ", self.value , " , Pas de Symbole")
    #     else :
    #         print("Noeud de type : ", self.type, ", Valeur est : ", self.value , " , Symbole : ", self.symbole)
    #     for child in self.children:
    #         child.affiche()
    def affiche(self, niveau=0):
        indent = "  " * niveau
        print(f"{indent}{self.type}: {self.value}")
        for enfant in self.children:
            enfant.affiche(niveau + 1)
    def genecode(self):
        if self.type == "Node_CONSTANT":
            result = f"push {self.value}"
            return result
        elif self.type == "Node_IDENTIFIER":
            result = f"push {self.value}"
            return result
        elif self.type == "UNAIRE":
            if self.valeur == "!":
                genecode_enfant0 = self.children[0].genecode()
                return genecode_enfant0 + [f"not"]
        elif self.type == "BINAIRE":
            genecode_enfant0 = self.children[0].genecode()
            genecode_enfant1 = self.children[1].genecode()
            operation = ""
            if self.value == "+":
                operation = "add"
            elif self.value == "-":
                operation = "sub"
            elif self.value == "*":
                operation = "mul"
            elif self.value == "/":
                operation = "div"
            return genecode_enfant0 + genecode_enfant1 + [f"{operation}"]
        elif self.type == "Node_Debug":
            genecode_enfant = self.children[0].genecode()
            return genecode_enfant + [f"push dbg"]
        elif self.type == "Node_Drop":
            genecode_enfant = self.children[0].genecode()
            return genecode_enfant , [f"drop 1"]
        elif self.type == "Node_Decla": #gestion noeud de déclaration
            pass
        elif self.type == "Node_Empty": #gestion noeud de déclaration
            pass
        elif self.type == "Node_Block" or self.type == "Node_Seq" : #gestions des noeuds de Block et de Séquence
            for child in self.children:
                child.genecode()
        elif self.type == "Node_Ref" : #gestions des noeuds de variables
            if(self.symbole.type == "VarLoc"):
                print("get "+ self.symbole.position)
        elif self.type == "Node_Cond" :
            indice1 = 0
            indice2 = 0
            global nbLabel
            if len(self.children) == 2:
                indice1 = nbLabel
                nbLabel += 1
                self.children[0].genecode()
                print("jumpf l" + str(indice1))
                self.children[1].genecode()
                print(".l" + str(indice1))
        elif self.type == "Node_Affectation" :
            print(self.children[1].genecode())
            print("dup")
            if(self.children[0].type != "Node_Ref"):
                raise Exception("Il ne s'agit pas d'une variable")
            if(self.children[0].symbole.type == "VarLoc"):
                result = f"set {self.children[0].symbole.position}"
                print(result)
        else:
            print(self.type)
            raise ValueError("Type de nœud inconnu")


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
            position -= 1  # move back the position by 1 so as to not skip the next character

        elif c == '+':
            tokenG = Token(TOKEN_TYPES['PLUS'], c)
        elif c == ',':
            tokenG = Token(TOKEN_TYPES['VIRGULE'], c)
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
            while position + 1 < len(chaine) - 1 and (chaine[position + 1].isalnum() or chaine[position + 1] == '_'):
                position += 1
                identifier_value += str(chaine[position])
            if identifier_value in MOTS_CLES:
                tokenG = Token(MOTS_CLES[identifier_value], identifier_value)
            else:
                tokenG = Token(TOKEN_TYPES['IDENTIFIER'], identifier_value)
        else:
            raise Exception("Le token est invalid")
        
        #tokenG.affiche()
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


def check(token_type):
    if(tokenG.type == TOKEN_TYPES[token_type]):
        next()
        return True
    else :
        return False

def accept(token_type):
    if not check(token_type):
        raise Exception("Le token est invalid  : " + str(token_type) + " requis : " + tokenG.type)

def Atome():
    if(check(TOKEN_TYPES['CONSTANT'])) :
        return Node(NODES_TYPES["Node_CONSTANT"],last.value)
    elif(tokenG.type in MOTS_CLES):
        pass
    #Gestion des variables
    elif(check(TOKEN_TYPES['IDENTIFIER'])):
        return Node(NODES_TYPES["Node_Ref"],last.value,(None,"VarLoc",None,None))
    elif(check(TOKEN_TYPES['OPEN_PAREN'])):
        N = Expression(0)
        while(last.type != TOKEN_TYPES['CLOSE_PAREN']):
            next()
        return N
    else :
        raise Exception(f"Atome inattendu: {last.type}")




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

def Expression(Prio_min): #Parseur de Brat, gestions des associativités et des priorités
    N = prefix()
    if(tokenG.type == 'EOF'):
        return N
    while OPERATORS.get(tokenG.type) is not None:
        Op = OPERATORS[tokenG.type]
        if(Op.priority <= Prio_min) :
            break
        else:
            next()
            M = Expression(Op.priority - Op.AaD)
            L = Node(Op.ndeType,Op.ndeVal,Op.ndeSymb)
            L.children.append(N)
            L.children.append(M)
            N = L
    return N

# Fonction des gestions des instructions, pour le moment pas encore adapté à notre nouvelle structure
def instruction():
    c = ','
    if(check(TOKEN_TYPES['Point_virgule'])) :
        return Node(NODES_TYPES["Node_Empty"],None,None)
    elif(check(TOKEN_TYPES['OPEN_ACCOLADE'])):
        N = Node(NODES_TYPES["Node_Block"],None,None)
        while(not check(TOKEN_TYPES['CLOSE_ACCOLADE'])):
            N.children.append(instruction())
        return N
    elif(check(TOKEN_TYPES['DEBUG'])):
        N = Expression(0)
        accept(TOKEN_TYPES['Point_virgule'])
        return Node(NODES_TYPES["Node_Debug"],None,None)
    #Gestion des variables
    elif(check(MOTS_CLES["int"])): 
        N = Node(NODES_TYPES['Node_Seq'],None,None)
        while True:
            accept(TOKEN_TYPES['IDENTIFIER'])
            N.children.append(Node(NODES_TYPES['Node_Decla'],last.value,(None,"VarLoc",None,None)))
            if not check(TOKEN_TYPES['VIRGULE']):
                break
        accept(TOKEN_TYPES['Point_virgule'])
        return N
    elif(check(MOTS_CLES["if"])):
        accept(TOKEN_TYPES['OPEN_PAREN'])
        N = Expression(0)
        accept(TOKEN_TYPES['CLOSE_PAREN'])
        I = instruction()
        ND = Node(NODES_TYPES['Node_Cond'],None)
        ND.children.append(N)
        ND.children.append(I)
        return ND
    else: # le cas d'une expression suivit d'un point virgule
        N = Expression(0)
        accept(TOKEN_TYPES['Point_virgule'])
        L = Node(NODES_TYPES["Node_Drop"],None,None)
        L.children.append(N)
        return L

# Fonction pour les variables
def Begin():
    TAB_SYMBOLE.append((" ", None)) #Ajout d'un élement dans la pile pour annoncer le début d'un bloc


def End():
    for valeur in reversed(TAB_SYMBOLE):
        if valeur[0] != " ":
            TAB_SYMBOLE.pop() #suppression des élements de la pile jusqu'au bloc suivant
            continue
        else:
            break


def Chercher(nom):
    for valeur in reversed(TAB_SYMBOLE):
        if valeur[0] == nom:
            return valeur[1] # si la variable est dans la pile, on retourne sont symbole
    raise ValueError("Erreur : Variable non définie dans le bloc") # sinon erreur


def Declarer(nom):
    for valeur in reversed(TAB_SYMBOLE):
        if valeur[0] == nom: # si le nom de la var est déjà dans la pile on retourne une erreur
            raise ValueError("Erreur : Variable déjà déclarée dans le bloc")
        if valeur[0] == " ": # si c'est le début d'un bloc, on sort de la fonction
            break
    S = Symbole(nom,"VarLoc",None,None)  # sinon, on crée un symbole et on remplie la pile
    TAB_SYMBOLE.append((nom, S)) #Ajout du couple (nom,Symbole) dans la pile
    return S



def AnaSem(N):
    global nbVar
    if(N.type == 'Node_Block'):
        Begin()
        for child in N.children:
            AnaSem(child)
        End()
    elif(N.type == 'Node_Decla'):
        S = Declarer(N.value)
        S.position = nbVar
        nbVar += 1
        S.type = "VarLoc"
    elif(N.type == 'Node_Ref'):
        S = Chercher(N.value)
        N.symbole = S
    else:
        for e in N.children:
            AnaSem(e)




# def expression(prioMin):
#     N = prefixe()
#     while OPERATORS.get(token.type) is not None:
#         op = OPERATORS[token.type_]
#         if op["Priorite"] <= prioMin:
#             break
#         next()
#         M = expression(op["Priorite"] - op["Aad"])
#         noeud = Noeud(op["Noeud"], "")
#         noeud.ajouter_enfant(N)
#         noeud.ajouter_enfant(M)
#         N = noeud
#     return N

# # Fonction pour analyser les expressions
# def expression():
#     noeud = prefix()
#     while tokenG.type in OPERATORS:
#         op = tokenG
#         noeud_droit = prefix()
#         noeud_gauche = noeud
#         noeud = Node("BINAIRE", op.value,None)
#         noeud.children.append(noeud_gauche)
#         noeud.children.append(noeud_droit)
#     return noeud     
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
    global nbVar
    global nbLabel
    with open('test_1.txt', 'r') as file: # ouverture du fichier
        text = file.read()
        AnaLex(text) #initialisation de l'analyse Lexicale
        next() #Appel à la fonction next
        print("Liste des tokens :")
        for x in Token_tab:
            x.affiche()
        print()
        while(tokenG.type != "EOF"):
            A = AnaSyn() # Analyse Synthaxique
            # Affichage de l'arbre
            A.affiche()
            AnaSem(A)
            A.genecode() 
         # redirection of execution result inside a file.txt
    # with open('./msm/msm/result.txt', 'w') as file:
    #     file.write(str(".start\n"))
    #     for instruction in assembleur :
    #         file.write('    '+str(instruction)+'\n')
    #     file.write(str("    dbg\n"))
    #     file.write(str("halt"))
    #     file.close()
    # for e in TAB_SYMBOLE:
    #     print(e)
nbVar = 0
nbLabel = 0
tokenG = Token(' ',0) #token courant
last = Token(' ',1) #token précédent 
Token_tab =[]
if __name__ == '__main__':
    main()