import re
import sys
MENOR_TAMANHO = 3 # MENOR TAMANHO DE SAIDA
MAIOR_TAMANHO = 16 # MAIOR TAMANHO DE SAIDA

class Anagrama(object):
    def __init__(self, letra='', final=False, tamanho=0):
        self.letra = letra
        self.final = final
        self.tamanho = tamanho
        self.children = {}

    def add(self, palavra):
        ana = self
        for index, letra in enumerate(palavra):
            if letra not in ana.children:
                ana.children[letra] = Anagrama(letra, index==len(palavra)-1, index+1)
            ana = ana.children[letra]

    def anagram(self, palavra):
        lobj = {}
        for letra in palavra:
            lobj[letra] = lobj.get(letra, 0) + 1
        min_length = len(palavra)
        return self._anagram(lobj, [], self, min_length)

    def _anagram(self, lobj, path, root, min_length):
        if self.final and self.tamanho >= MENOR_TAMANHO and self.tamanho <= MAIOR_TAMANHO:
            word = ''.join(path)
            length = len(word.replace(' ', ''))
            if length >= min_length:
                yield word
            path.append(' ')
            for word in root._anagram(lobj, path, root, min_length):
                yield word
            path.pop()
        for letra, ana in self.children.iteritems():
            count = lobj.get(letra, 0)
            if count == 0:
                continue
            lobj[letra] = count - 1
            path.append(letra)
            for word in ana._anagram(lobj, path, root, min_length):
                yield word
            path.pop()
            lobj[letra] = count
#FIM ana

def clean(palavar):    
    checking = bool(re.search(r'[^A-Z ]', palavar))
    if checking == True:
        return checking
    else:    
        sys.exit()


def load_dictionary(path):
    resultado = Anagrama()
    for line in open(path, 'r'):
        word = line.strip().upper()
        resultado.add(word)
    return resultado

def main():
    palavras = load_dictionary('palavras.txt')
    while True:
        palavra = raw_input('Digite uma palavra... : ')
        if clean(palavra) == True:
            palavra = palavra.upper()
            palavra = palavra.replace(' ', '')
            if not palavra:
                break
            for word in palavras.anagram(palavra):
                print word

if __name__ == '__main__':
    main()