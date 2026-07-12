import sys
import argparse
import json
import os
from pathlib import Path

parser = argparse.ArgumentParser(description="BackUp for MySql/MariaDB")

parser.add_argument(
    "-s",
    "--set",
    action="store_true",
    help="Definir Provider"
)
parser.add_argument(
    "-a",
    "--add",
    action="store_true",
    help="Adicionar um Provider"
)
parser.add_argument(
    "-d",
    "--delete",
    action="store_true",
    help="Excluir um Provider"
)


ARQUIVO_JSON = Path(__file__).parent.parent / "provider.json"
ARQUIVO_ENV = Path(__file__).parent.parent / ".env"

with open(ARQUIVO_JSON, "r") as arquivo:
    resultado_json = json.load(arquivo)

def limparTela():
    os.system("clear")

class setProvider:

    providers_names = []


    @staticmethod
    def MontarListaProviders():
        for usuarios in resultado_json:
            setProvider.providers_names.append(usuarios['NOME_PROVIDER'])

    @staticmethod
    def PrintarListaProviders():

        setProvider.MontarListaProviders()

        print("Providers Disponiveis: \n")

        for provider in resultado_json:
            print(f"{provider['ID']} {provider['NOME_PROVIDER']}")

    @staticmethod
    def EscreverEnv(db, user, password):
        with open(ARQUIVO_ENV, "w") as arquivo:
            conteudo = f"""DB_HOST=127.0.0.1
DB_USER='{user}'
DB_PASSWORD='{password}'
DB_NAME='{db}'
    """
            arquivo.write(conteudo)

    @staticmethod
    def set(id):  
        for p in resultado_json:
            if p['ID'] == int(id):
                DB = p['DB']
                USER = p['USER']
                PASSWORD = p['PASSWORD']

                setProvider.EscreverEnv(DB, USER, PASSWORD)

                print("\nProvider selecionado com sucesso.\n")
                return
            elif p['ID'] != id:
                continue
            print("\nProvider não encontrado.\n")
            input()
            Main()

    def main():
        limparTela()

        setProvider.PrintarListaProviders()

        try:
            id = int(input("\nID do provider que deseja selecionar: "))
            setProvider.set(id)
        except KeyboardInterrupt:
            limparTela()
            exit(0)
            


class addProvider:

    @staticmethod
    def DefinirID():

        if not resultado_json:
            return 1

        maior_id = max(provider["ID"] for provider in resultado_json)

        ID = maior_id + 1

        return ID

    @staticmethod
    def AdicionarProvider():
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            providers = json.load(arquivo)

        try:
            limparTela()
            nome_provider = input("\n\nProvider Name: \n~: ")
            limparTela()
            db = input("\n\nData Base: \n~: ")
            limparTela()
            user = input("\n\nUser: \n~: ")
            limparTela()
            password = input("\n\nPassword: \n~: ")
            limparTela()
        except KeyboardInterrupt:
            limparTela()
            exit(0)

        if any(p['NOME_PROVIDER'] == nome_provider for p in providers):
            print("Já existe um provider com esse nome.")
            return
        
        novo_provider = {
            "ID": addProvider.DefinirID(),
            "NOME_PROVIDER": nome_provider,
            "DB": db,
            "USER": user,
            "PASSWORD": password
        }

        providers.append(novo_provider)

        try:
            with open(ARQUIVO_JSON, "w") as arquivo:
                json.dump(providers, arquivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)

class delProvider:
    @staticmethod
    def ExcluirProvider():

        limparTela()

        print("Providers disponíveis:\n")

        for provider in resultado_json:
            print(f"{provider['ID']} - {provider['NOME_PROVIDER']}")

        try:
            provider_id = int(input("\nID do provider que deseja excluir: "))
        except (ValueError, KeyboardInterrupt):
            limparTela()
            return

        for provider in resultado_json:

            if provider["ID"] == provider_id:

                resultado_json.remove(provider)

                with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
                    json.dump(
                        resultado_json,
                        arquivo,
                        indent=4,
                        ensure_ascii=False
                    )

                print("\nProvider removido com sucesso.")
                return

        print("\nProvider não encontrado.")


limparTela()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)


def Main():
    args = parser.parse_args()

    if args.set:
        setProvider.main()
    if args.add:
        addProvider.AdicionarProvider()
    if args.delete:
        delProvider.ExcluirProvider()

if __name__ == "__main__":
    Main()