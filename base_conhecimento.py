import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


def pegar_pontos(tupla):
    return tupla[0]


class BaseConhecimento:

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []  # lista de objetos Orientacao

    def carregar(self):
        self.orientacoes = []
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Erro: o arquivo {self.caminho} não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: o arquivo {self.caminho} está corrompido.")
            return False

        for item in dados:
            try:
                orientacao = Orientacao(
                    item["id"], item["categoria"], item["titulo"],
                    item["palavras_chave"], item["resposta"],
                    item["documentos"], item["onde"],
                    item["fonte"], item["verificado_em"]
                )
                self.orientacoes.append(orientacao)
            except (KeyError, TypeError):
                print("Aviso: um registro da base foi ignorado por estar incompleto.")

        return len(self.orientacoes) > 0

    def categorias(self):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                lista.append(orientacao)
        return lista

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = normalizar(pergunta)
        titulo_norm = normalizar(orientacao.titulo)
        pontos = 0

        # +3 para cada palavra-chave que aparece na pergunta
        for palavra_chave in orientacao.palavras_chave:
            if normalizar(palavra_chave) in pergunta_norm:
                pontos += 3

        # +1 para cada palavra da pergunta (4 letras ou mais) que aparece no título
        palavras_vistas = []
        for palavra in pergunta_norm.split():
            if len(palavra) >= 4 and palavra not in palavras_vistas:
                palavras_vistas.append(palavra)
                if " " + palavra + " " in titulo_norm:
                    pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=pegar_pontos, reverse=True)
        return resultados