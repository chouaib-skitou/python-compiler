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
    return tokenG.type == TOKEN_TYPES[token_type]

def accept(self, token_type):
    if not self.check(token_type):
        self.next()
        return True
    return False
    

# Main program
def main():
    with open('test_1.txt', 'r') as file:
        text = file.read()
    print(next(text))

if __name__ == '__main__':
    main()