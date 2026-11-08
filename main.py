from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível carregar a base de conhecimento.")
        print("Verifique o arquivo data/base_conhecimento.json.")
        return

    assistente = Assistente("Citizen Assist AI", base)

    print(f"=== {assistente.nome} ===")
    print("Orientação para jovens no primeiro emprego.")
    print("Aviso: este assistente NÃO é um canal oficial.")
    print("Não digite CPF, telefone, e-mail ou outros dados pessoais.")

    while True:
        print("\n=== MENU ===")
        print("1 - Fazer uma pergunta")
        print("2 - Navegar por categorias")
        print("3 - Ver indicadores")
        print("4 - Exportar atendimentos para CSV")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            assistente.pedir_nota()
            print("Obrigado por usar o assistente. Até logo!")
            break
        else:
            print("Opção inválida. Digite 1, 2, 3, 4 ou 0.")


if __name__ == "__main__":
    main()