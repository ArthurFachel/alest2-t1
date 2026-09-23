"""CLI interativa do Pennywise: mantém o Top-10 das crianças mais covardes.

Uso:
    python pennywise.py

Comandos:
    consultar <arquivo>   lê a região em fluxo e atualiza o Top-10
    mostrar               exibe o Top-10 atual (escore crescente)
    limpar                esvazia a estrutura
    ajuda                 lista os comandos
    sair                  encerra o programa
"""

import sys

from top_covardes import CAPACIDADE_PADRAO, ErroDeFormato, TopCovardes

PROMPT = "Pennywise> "

AJUDA = """Comandos disponíveis:
  consultar <arquivo>  Lê o arquivo da região, uma criança por vez, e atualiza o Top-10.
  mostrar              Exibe as até 10 crianças armazenadas, da mais covarde para a menos.
  limpar               Esvazia a estrutura. O Top-10 recomeça vazio.
  ajuda                Lista os comandos disponíveis.
  sair                 Encerra o programa."""


def exec_consultar(top, argumento):
    """Trata o comando `consultar <arquivo>`."""
    if not argumento:
        print("Uso: consultar <arquivo>")
        return
    try:
        top.consultar_arquivo(argumento)
    except FileNotFoundError:
        print("Arquivo '{}' não encontrado. O Top-10 permanece como estava.".format(argumento))
    except IsADirectoryError:
        print("'{}' é um diretório, não um arquivo de região.".format(argumento))
    except PermissionError:
        print("Sem permissão para ler '{}'.".format(argumento))
    except (ErroDeFormato, UnicodeDecodeError) as erro:
        print("Arquivo '{}' com formato inválido: {}".format(argumento, erro))
    else:
        print("Região {} lida.".format(argumento))


def exec_mostrar(top):
    """Trata o comando `mostrar`."""
    if top.esta_vazio():
        print("Nenhuma criança na lista.")
        return
    print("Crianças no Top-{}:".format(top.capacidade()))
    for posicao, crianca in enumerate(top.listar_ordenado(), start=1):
        print("{}. {} {}".format(posicao, crianca.nome, crianca.score))


def exec_limpar(top):
    """Trata o comando `limpar`."""
    top.limpar()
    print("Lista esvaziada.")

# Aux de comandos
def interpretar_comando(linha):
    partes = linha.strip().split(maxsplit=1)
    if not partes:
        return "", ""
    comando = partes[0].lower()
    argumento = partes[1].strip() if len(partes) > 1 else ""
    return comando, argumento


def processar(top, linha):
    """Executa uma linha de comando. Devolve False quando for para sair."""
    comando, argumento = interpretar_comando(linha)
    if not comando:
        return True
    if comando == "consultar":
        exec_consultar(top, argumento)
    elif comando == "mostrar":
        exec_mostrar(top)
    elif comando == "limpar":
        exec_limpar(top)
    elif comando == "ajuda":
        print(AJUDA)
    elif comando == "sair":
        return False
    else:
        print("Comando desconhecido: '{}'. Digite 'ajuda' para ver a lista.".format(comando))
    return True


def main():
    top = TopCovardes(CAPACIDADE_PADRAO)
    print("Pennywise e as 10 crianças mais covardes. Digite 'ajuda' para os comandos.")
    while True:
        try:
            linha = input(PROMPT)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print("\nAté a próxima, Derry.")
            break
        if not processar(top, linha):
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
