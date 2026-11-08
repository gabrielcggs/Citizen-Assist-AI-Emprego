import csv
import json
import os
import time
from datetime import datetime


class Assistente:

    def __init__(self, nome, base):
        self.nome = nome
        self.base = base  # objeto BaseConhecimento (composição)
        self.caminho_historico = "data/historico.json"
        self.caminho_csv = "data/atendimentos.csv"
        self.historico = []
        self.carregar_historico()
        self.inicio_sessao = len(self.historico)  # para saber quais são desta sessão

    # ---------- histórico ----------
    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                self.historico = dados
        except (FileNotFoundError, json.JSONDecodeError):
            self.historico = []

    def salvar_historico(self):
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não foi possível salvar o histórico.")

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou,
                  tentativas, tempo):
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo
        }
        self.historico.append(registro)
        self.salvar_historico()

    # ---------- funções auxiliares ----------
    def tem_dado_pessoal(self, texto):
        if "@" in texto:
            return True
        digitos = 0
        for caractere in texto:
            if caractere.isdigit():
                digitos += 1
        return digitos >= 8

    def ler_numero(self, texto):
        try:
            return int(texto.strip())
        except ValueError:
            return None

    def perguntar_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta == "s":
                return True
            if resposta == "n":
                return False
            print("Resposta inválida. Digite s ou n.")

    # ---------- atendimento por pergunta ----------
    def perguntar(self):
        tentativas = 0
        inicio = time.time()
        ultima_pergunta = ""

        while True:
            texto = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if texto == "0":
                if tentativas > 0:
                    tempo = round(time.time() - inicio, 1)
                    self.registrar("pergunta", ultima_pergunta, None, False,
                                   False, tentativas, tempo)
                return

            if texto == "":
                print("Você não digitou nada. Escreva sua dúvida.")
                continue

            if self.tem_dado_pessoal(texto):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            ultima_pergunta = texto
            resultados = self.base.buscar(texto)

            if len(resultados) == 0 or resultados[0][0] < 3:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente usar outras palavras (ex.: cpf, carteira de trabalho, FGTS)")
                print("ou volte ao menu e use a navegação por categorias.")
                continue

            pontos, melhor = resultados[0]
            if pontos >= 6:
                confianca = "ALTA"
            else:
                confianca = "MÉDIA"

            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            melhor.exibir()

            # até duas alternativas
            alternativas = resultados[1:3]
            if len(alternativas) > 0:
                print("\nVeja também:")
                for pts, orientacao in alternativas:
                    print(f"  - {orientacao.titulo} ({pts} pontos)")

            ajudou = self.perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar("pergunta", texto, melhor.id, True, ajudou,
                           tentativas, tempo)

            # começa um novo atendimento
            tentativas = 0
            ultima_pergunta = ""
            inicio = time.time()

    # ---------- atendimento por categoria ----------
    def navegar(self):
        categorias = self.base.categorias()
        while True:
            print("\n=== Categorias ===")
            for numero, categoria in enumerate(categorias, start=1):
                print(f"{numero} - {categoria}")
            print("0 - Voltar")

            opcao = self.ler_numero(input("Escolha uma categoria: "))
            if opcao == 0:
                return
            if opcao is None or opcao < 1 or opcao > len(categorias):
                print("Opção inválida. Digite um número da lista.")
                continue

            self.navegar_categoria(categorias[opcao - 1])

    def navegar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        while True:
            print(f"\n=== {categoria} ===")
            for numero, orientacao in enumerate(orientacoes, start=1):
                print(f"{numero} - {orientacao.titulo}")
            print("0 - Voltar")

            inicio = time.time()
            opcao = self.ler_numero(input("Escolha uma orientação: "))
            if opcao == 0:
                return
            if opcao is None or opcao < 1 or opcao > len(orientacoes):
                print("Opção inválida. Digite um número da lista.")
                continue

            escolhida = orientacoes[opcao - 1]
            escolhida.exibir()
            ajudou = self.perguntar_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            tempo = round(time.time() - inicio, 1)
            self.registrar("categoria", "", escolhida.id, True, ajudou, 1, tempo)

    # ---------- nota de facilidade ----------
    def pedir_nota(self):
        if len(self.historico) == self.inicio_sessao:
            return
        while True:
            nota = self.ler_numero(input("\nDe 1 a 5, quão fácil foi usar o assistente? "))
            if nota is not None and 1 <= nota <= 5:
                break
            print("Nota inválida. Digite um número de 1 a 5.")

        for registro in self.historico[self.inicio_sessao:]:
            registro["nota_facilidade"] = nota
        self.salvar_historico()

    # ---------- indicadores ----------
    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nAinda não há atendimentos registrados.")
            return

        encontrados = 0
        ajudaram = 0
        soma_tempo = 0
        soma_tentativas = 0
        soma_notas = 0
        qtd_notas = 0
        sem_solucao = []

        for registro in self.historico:
            if registro.get("encontrou"):
                encontrados += 1
                soma_tempo += registro.get("tempo_segundos", 0)
            if registro.get("ajudou"):
                ajudaram += 1
            soma_tentativas += registro.get("tentativas", 0)

            if "nota_facilidade" in registro:
                soma_notas += registro["nota_facilidade"]
                qtd_notas += 1

            pergunta = registro.get("pergunta", "")
            if pergunta != "" and (not registro.get("encontrou") or not registro.get("ajudou")):
                if pergunta not in sem_solucao:
                    sem_solucao.append(pergunta)

        print("\n=== Indicadores ===")
        print(f"Total de atendimentos: {total}")
        print(f"Resposta encontrada: {round(encontrados / total * 100, 1)}%")
        print(f"Taxa de acerto (ajudou): {round(ajudaram / total * 100, 1)}%")

        if encontrados > 0:
            print(f"Tempo médio para encontrar: {round(soma_tempo / encontrados, 1)} s")
        else:
            print("Tempo médio para encontrar: sem dados")

        print(f"Tentativas por atendimento: {round(soma_tentativas / total, 1)}")

        if qtd_notas > 0:
            print(f"Facilidade de uso (1 a 5): {round(soma_notas / qtd_notas, 1)}")
        else:
            print("Facilidade de uso (1 a 5): sem dados")

        print("Dúvidas sem solução:")
        if len(sem_solucao) == 0:
            print("  (nenhuma)")
        else:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")

    # ---------- exportar CSV ----------
    def exportar_csv(self):
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                  "ajudou", "tentativas", "tempo_segundos", "nota_facilidade"]
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos, extrasaction="ignore")
                escritor.writeheader()
                for registro in self.historico:
                    escritor.writerow(registro)
            print(f"\nArquivo {self.caminho_csv} exportado com sucesso!")
        except OSError:
            print("Erro: não foi possível exportar o CSV.")