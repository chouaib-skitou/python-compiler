EOF = 'EOF'

TOKEN_TYPES = {
    'INTEGER': 'INTEGER',
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

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def get_type(self):
        return self.type
    
    def get_value(self):
        return self.value

    def __str__(self):
        return f"Token({self.type}, {self.value})"
    

class Lexer:
    def __init__(self, text):
        self.tokens = text.split()
        self.pos = 0
        self.token = None
        self.last = None
        self.next()

    def next(self):
        if self.pos < len(self.tokens):
            self.last = self.token
            token = self.tokens[self.pos]
            self.pos += 1

            if token.isdigit():
                self.token = Token(TOKEN_TYPES['INTEGER'], token)
            elif token == '+':
                self.token = Token(TOKEN_TYPES['PLUS'], token)
            elif token == '-':
                self.token = Token(TOKEN_TYPES['MINUS'], token)
            elif token == '*':
                self.token = Token(TOKEN_TYPES['MUL'], token)
            elif token == '/':
                self.token = Token(TOKEN_TYPES['DIV'], token)
            elif token == '%':
                self.token = Token(TOKEN_TYPES['MOD'], token)
            elif token == '(':
                self.token = Token(TOKEN_TYPES['OPEN_PAREN'], token)
            elif token == ')':
                self.token = Token(TOKEN_TYPES['CLOSE_PAREN'], token)
            elif token.isalnum():
                self.token = Token(TOKEN_TYPES['IDENTIFIER'], token)
            else:
                raise Exception("Invalid token")
        else:
            self.token = Token(TOKEN_TYPES['EOF'], None)
            self.last = None

    def check(self, token_type):
        return self.token.type == TOKEN_TYPES[token_type]

    def accept(self, token_type):
        if self.check(token_type):
            self.next()
            return True
        return False

    def lecture(self):
        if self.token is not None:
            return self.token.value
        return None
    

# Main program
def main():
    with open('test_1.txt', 'r') as file:
        text = file.read()
    lexer = Lexer(text)

    while lexer.token.type != EOF:
        print(lexer.token)
        lexer.next()

if __name__ == '__main__':
    main()