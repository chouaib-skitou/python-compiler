class token:

        def __init__(self,sontype, valeur):
                self.sontype = sontype
                self.valeur = valeur
        
        def affiche(self): #méthode de la classe
            print("Le token est de type : ", self.sontype, " et sa valeur est : ", self.valeur)
        

tokenG = token('test',0) #token courant
last = token('test',1) #token précédent

def next(chaine):
    position = 0
    
    while (position < len(chaine)) : #tant qu'on est pas arrivé à la fin de la chaine, on incrémente position
        #déclaration de variable global
        global last
        global tokenG
        last = tokenG # last devient la dernier token reçu
        c = chaine[position]
        if c.isdigit() :
            tokenG = token("constante",c)
        elif c == '+':
            tokenG = token("plus",None)
        elif c == '-':
            tokenG = token("moins",None)
        elif c == '=':
            tokenG = token("égale",None)
        else:
            tokenG = token("inconnu",None)
        tokenG.affiche()
        position = position + 1
    return token("EOF",None) # sinon on retourne le token EOF



def check(T):
    if tokenG.sontype == T :
        next()
        return True
    else :
        return False

def accept(T):
    if not (check(T)) :
        raise SystemExit('Erreur de token')

# Token des différents mots-clé
tokenInt = token("int",None)
tokenFor = token("for",None)
tokenWhile = token("while",None)
tokenIf = token("if",None)
tokenElse = token("else",None)
tokenDo = token("do",None)
tokenBreak = token("break",None)
tokencontinue = token("continue",None)
tokenreturn = token("return",None)


cha = "1+2=3"
print(next(cha))

