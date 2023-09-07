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

}
NODES_TYPES = {
    'NODE_IDENTIFIER': 'NODE_IDENTIFIER',
    'NODE_CONSTANT': 'NODE_CONSTANT',
    'NODE_MINUS_UNARY': 'NODE_MINUS_UNARY',
    'NODE_NOT': 'NODE_NOT',
    'BINAIRE': '-',
    'BINAIRE': '+',
    'BINAIRE' : '*',
    'BINAIRE' : '/',
    'BINAIRE' : '%',

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

class ValOpe:
    def __init__(self, nde, priority, AaD):
        self.nde = nde
        self.priority =priority
        self.AaD = AaD

# Table des Opérateurs avec les priorités
OPERATORS = {
    TOKEN_TYPES['PLUS']: ValOpe('BINAIRE',6,0),
    TOKEN_TYPES['MINUS']: ValOpe('NODE_MINUS_BINAIRE',6,0),
    TOKEN_TYPES['MUL']: ValOpe('NODE_MUL',7,0),
    TOKEN_TYPES['DIV']: ValOpe('NODE_DIV',7,0),
    TOKEN_TYPES['MOD']: ValOpe('NODE_MOD',7,0),
    TOKEN_TYPES['AFFECTATION']: ValOpe('NODE_AFFECTATION',1,1),
    TOKEN_TYPES['OR']: ValOpe('NODE_OR',2,0),
    TOKEN_TYPES['AND']: ValOpe('NODE_AND',3,0),
    TOKEN_TYPES['EQUAL']: ValOpe('NODE_EQUAL',4,0),
    TOKEN_TYPES['NOT_EQUAL']: ValOpe('NODE_NOT_EQUAL',4,0),
    TOKEN_TYPES['GREATER_THAN']: ValOpe('NODE_GREATER_THAN',5,0),
    TOKEN_TYPES['LESS_THAN']: ValOpe('NODE_LESS_THAN',5,0),

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
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.children = []
    
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
        if self.type == "NODE_CONSTANT":
            return [f"push {self.value}"]
        elif self.type == "UNAIRE":
            if self.valeur == "!":
                # À compléter pour l'opérateur unaire !
                pass
        elif self.type == "BINAIRE":
            instructions_gauche = self.children[0].genecode()
            instructions_droite = self.children[1].genecode()
            if self.value == "+":
                operation = "ADD"
            elif self.value == "-":
                operation = "SUB"
            elif self.value == "*":
                operation = "MUL"
            elif self.value == "/":
                operation = "DIV"
            return instructions_gauche + instructions_droite + [f"push {operation}"]
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
    tokenG.affiche()


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
        return Node(NODES_TYPES["NODE_CONSTANT"],last.value)
    elif(check(TOKEN_TYPES['IDENTIFIER'])):
        return Node(NODES_TYPES["NODE_IDENTIFIER"],last.value)
    elif(check(TOKEN_TYPES['OPEN_PAREN'])):
        N = expression()
        while(last.type != TOKEN_TYPES['CLOSE_PAREN']):
            next()
        return N
    else :
        raise Exception("Token invalid !!!")
        

def prefix():
    # if(check(TOKEN_TYPES['MINUS'])) :
    #     N = prefix() 
    #     return Node(NODES_TYPES["NODE_MINUS_UNAIRY"],N)

    if(check(TOKEN_TYPES['NOT'])) :
        N = prefix()
        return Node(NODES_TYPES["NODE_NOT"],N)

    elif(check(TOKEN_TYPES['PLUS'])) :
        N = prefix()
        return N
    elif(check(TOKEN_TYPES['MINUS'])) :
        N = prefix()
        return N
    else :
        N = Atome()
        return N

# Fonction pour analyser les expressions
def expression():
    noeud = prefix()
    while tokenG.type in {"PLUS", "MINUS", "MUL", "DIV"}:
        op = tokenG
        noeud_droit = prefix()
        noeud_gauche = noeud
        noeud = Node("BINAIRE", op.value)
        noeud.children.append(noeud_gauche)
        noeud.children.append(noeud_droit)
    return noeud

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
#     if N.type == 'NODE_CONSTANT' :
#         print("push",N.value)
#     elif N.type == 'NODE_NOT' :
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
    return expression()  

# Main program
def main():
    with open('test_1.txt', 'r') as file:
        text = file.read()
        AnaLex(text)
        next()
        while(tokenG.type != "EOF"):
            A = AnaSyn()
            A.affiche()
            assembleur = A.genecode()
            for instruction in assembleur :
                print(instruction)


if __name__ == '__main__':
    main()