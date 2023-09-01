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
}
NODES_TYPES = {
    'NODE_IDENTIFIER': 'NODE_IDENTIFIER',
    'NODE_CONSTANT': 'NODE_CONSTANT',
    'NODE_MINUS_UNARY': 'NODE_MINUS_UNARY',
    'NODE_MINUS_BINARY': 'NODE_MINUS_BINARY',
    'NODE_NOT': 'NODE_NOT',
    'NODE_PLUS': 'NODE_PLUS',

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
    TOKEN_TYPES['PLUS']: ValOpe('PLUS',6,0),
    TOKEN_TYPES['MINUS']: ValOpe('MINUS',6,0),
    TOKEN_TYPES['MUL']: ValOpe('MUL',7,0),
    TOKEN_TYPES['DIV']: ValOpe('DIV',7,0),
    TOKEN_TYPES['MOD']: ValOpe('MOD',7,0),

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

tokenG = Token('test',0) #token courant
last = Token('test',1) #token précédent 

def next(chaine):
        position = 0
    
        while (position < len(chaine)) : #tant qu'on est pas arrivé à la fin de la chaine, on incrémente position
            #déclaration de variable global
            global last
            global tokenG
            last = tokenG # last devient la dernier token reçu
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
            
            tokenG.affiche()
            position = position + 1

        return Token("EOF",None)

def check(self, token_type):
    if(tokenG.type == TOKEN_TYPES[token_type]):
        self.next()
        return True
    else :
        return False

def accept(self, token_type):
    if not self.check(token_type):
        raise Exception("Le token est invalid")

def Atome():
    if(check(TOKEN_TYPES['CONSTANT'])) :
        return Node(NODES_TYPES["NODE_CONSTANT"],tokenG.value)
    elif(check(TOKEN_TYPES['IDENTIFIER'])):
        return Node(NODES_TYPES["NODE_IDENTIFIER"],tokenG.value)
    elif(check(TOKEN_TYPES['OPEN_PAREN'])):
        N = E()
        accept(TOKEN_TYPES['CLOSE_PAREN'])
        return N
    else :
        raise Exception("Le token est invalid")

def prefix():
    if(check(TOKEN_TYPES['TOKEN_MINUS'])) :
        N = prefix()
        return Node(NODES_TYPES["NODE_MINUS_UNAIRY"],tokenG.value)

    elif(check(TOKEN_TYPES['TOKEN_NOT'])) :
        N = prefix()
        return Node(NODES_TYPES["NODE_NOT"],tokenG.value)

    elif(check(TOKEN_TYPES['TOKEN_PLUS'])) :
        N = prefix()
        return N

    else :
        N = Atome()
        return N

def Expression(Prio_min): #Parseur de Brat
    N = P()
    while(OPERATORS[tokenG.type] != None):
        Op = OPERATORS[tokenG.type]
        if(Op.priority <= Prio_min) :
            break
        else:
            next()
            M = E(Op.priority - Op.AaD)
            N = Node(Op.nde,N,M)
    return N
        
def  Genecode(N):
    if N.type == 'NODE_CONSTANT' :
        print("push",N.valeur)
    elif N.type == 'NODE_NOT' :
        Gencode(N.children[0])
        print("not")
    elif N.type == 'NODE_PLUS':
        Genecode(N.children[0])
        Genecode(N.children[1])
        print("add")
    elif N.type == 'NODE_MINUS_BINARY':
        Genecode(N.children[0])
        Genecode(N.children[1])
        print("sub")

# Main program
def main():
    with open('test_1.txt', 'r') as file:
        text = file.read()
    next(text)

if __name__ == '__main__':
    main()