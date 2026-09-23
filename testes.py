"""Testes do Top-10 e da fila de prioridade.

Rodar:  python testes.py
Não usa framework externo: só asserts e uma contagem simples.
"""

import io
import os
import sys
import tempfile

from crianca import Crianca
from fila_prioridade import FilaPrioridadeMaxima
from pennywise import processar
from top_covardes import ErroDeFormato, TopCovardes

DIRETORIO = os.path.dirname(os.path.abspath(__file__))
REGIOES = os.path.join(DIRETORIO, "regioes")

_falhas = []


def verificar(condicao, descricao):
    if condicao:
        print("  ok   {}".format(descricao))
    else:
        print("  FALHA {}".format(descricao))
        _falhas.append(descricao)


def caminho_regiao(nome):
    return os.path.join(REGIOES, nome)


def ler_top_de_referencia(nomes_de_arquivo, k=10):
    """Referência ingênua: carrega tudo e ordena. Só para conferir os testes."""
    todas = []
    for nome in nomes_de_arquivo:
        with open(caminho_regiao(nome), encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    nome_crianca, escore = linha.split()
                    todas.append((int(escore), nome_crianca))
    todas.sort()
    return todas[:k]


def top_como_tuplas(top):
    return [(c.escore, c.nome) for c in top.listar_ordenado()]


# ----------------------------------------------------------------------
def testar_heap_basico():
    print("teste: operações básicas da fila de prioridade")
    fila = FilaPrioridadeMaxima(3)
    verificar(fila.esta_vazia(), "fila nasce vazia")
    fila.inserir(Crianca("A", 10))
    fila.inserir(Crianca("B", 30))
    fila.inserir(Crianca("C", 20))
    verificar(fila.esta_cheia(), "fila cheia com 3 itens")
    verificar(fila.maximo().nome == "B", "raiz é o maior escore (B, 30)")
    verificar(fila.remover_maximo().nome == "B", "remover_maximo devolve B")
    verificar(fila.maximo().nome == "C", "nova raiz é C (20)")
    verificar(fila.tamanho() == 2, "tamanho cai para 2")
    fila.limpar()
    verificar(fila.esta_vazia() and fila.tamanho() == 0, "limpar esvazia a fila")


def testar_capacidade_nunca_excede():
    print("teste: capacidade máxima de 10 é respeitada")
    top = TopCovardes(10)
    for nome in os.listdir(REGIOES):
        top.consultar_arquivo(caminho_regiao(nome))
        verificar(
            top.quantidade() <= 10,
            "após {}: {} crianças armazenadas (<= 10)".format(nome, top.quantidade()),
        )


def testar_uma_regiao():
    print("teste: centro.txt sozinho bate com a sessão de exemplo")
    top = TopCovardes(10)
    top.consultar_arquivo(caminho_regiao("centro.txt"))
    esperado = [
        (16, "Stephanie_Price"),
        (23, "Stephen_Adams"),
        (25, "Don_Hagarty"),
        (26, "Betty_Ripsom"),
        (30, "Sally_Mueller"),
        (31, "Sonia_Kaspbrak"),
        (48, "Greta_Bowie"),
        (50, "Zack_Denbrough"),
        (58, "Adrian_Mellon"),
        (61, "Casey_Tremblay"),
    ]
    verificar(top_como_tuplas(top) == esperado, "Top-10 de centro.txt confere")


def testar_duas_regioes():
    print("teste: centro.txt + neibolt.txt bate com a sessão de exemplo")
    top = TopCovardes(10)
    top.consultar_arquivo(caminho_regiao("centro.txt"))
    top.consultar_arquivo(caminho_regiao("neibolt.txt"))
    esperado = [
        (5, "Oscar_Wilson"),
        (7, "Victor_Murray"),
        (10, "Kay_Powell"),
        (14, "Linda_Thompson"),
        (16, "Stephanie_Price"),
        (22, "Philip_Johnson"),
        (23, "Stephen_Adams"),
        (25, "Don_Hagarty"),
        (26, "Betty_Ripsom"),
        (30, "Sally_Mueller"),
    ]
    verificar(top_como_tuplas(top) == esperado, "Top-10 acumulado confere")


def testar_todas_as_regioes_contra_referencia():
    print("teste: cinco regiões contra a referência por ordenação total")
    arquivos = ["centro.txt", "neibolt.txt", "barrens.txt", "canal.txt", "quarry.txt"]
    top = TopCovardes(10)
    for nome in arquivos:
        top.consultar_arquivo(caminho_regiao(nome))
    verificar(
        top_como_tuplas(top) == ler_top_de_referencia(arquivos),
        "Top-10 global igual ao obtido por ordenação completa",
    )


def testar_ordem_de_consulta_nao_importa():
    print("teste: a ordem das consultas não altera o resultado")
    arquivos = ["centro.txt", "neibolt.txt", "barrens.txt", "canal.txt", "quarry.txt"]
    primeiro = TopCovardes(10)
    for nome in arquivos:
        primeiro.consultar_arquivo(caminho_regiao(nome))
    segundo = TopCovardes(10)
    for nome in reversed(arquivos):
        segundo.consultar_arquivo(caminho_regiao(nome))
    verificar(top_como_tuplas(primeiro) == top_como_tuplas(segundo), "resultado idêntico")


def testar_limpar():
    print("teste: limpar zera o estado")
    top = TopCovardes(10)
    top.consultar_arquivo(caminho_regiao("centro.txt"))
    top.limpar()
    verificar(top.esta_vazio(), "estrutura fica vazia")
    top.consultar_arquivo(caminho_regiao("neibolt.txt"))
    esperado_neibolt = ler_top_de_referencia(["neibolt.txt"])
    verificar(top_como_tuplas(top) == esperado_neibolt, "após limpar, só conta a nova região")


def testar_empate_lexicografico():
    print("teste: empate de escore é desempatado pelo nome")
    top = TopCovardes(3)
    for nome in ("Zoe", "Ana", "Bia"):
        top.oferecer(Crianca(nome, 50))
    verificar(
        [c.nome for c in top.listar_ordenado()] == ["Ana", "Bia", "Zoe"],
        "ordem lexicográfica entre escores iguais",
    )
    trocou = top.oferecer(Crianca("Aaa", 50))
    verificar(trocou, "'Aaa' entra no lugar de 'Zoe' (mesmo escore, nome menor)")
    verificar(
        [c.nome for c in top.listar_ordenado()] == ["Aaa", "Ana", "Bia"],
        "Top final após o desempate",
    )


def testar_linhas_vazias_e_formato():
    print("teste: linhas vazias ignoradas e formato inválido detectado")
    with tempfile.TemporaryDirectory() as pasta:
        bom = os.path.join(pasta, "bom.txt")
        with open(bom, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n\nAna 5\n\n   \nBia 7\n\n")
        top = TopCovardes(10)
        lidas = top.consultar_arquivo(bom)
        verificar(lidas == 2, "apenas 2 linhas úteis lidas")
        verificar(top_como_tuplas(top) == [(5, "Ana"), (7, "Bia")], "conteúdo correto")

        ruim = os.path.join(pasta, "ruim.txt")
        with open(ruim, "w", encoding="utf-8") as arquivo:
            arquivo.write("Ana cinco\n")
        erro = None
        try:
            TopCovardes(10).consultar_arquivo(ruim)
        except ErroDeFormato as capturado:
            erro = capturado
        verificar(erro is not None, "escore não inteiro levanta ErroDeFormato")


def testar_arquivo_inexistente_preserva_estado():
    print("teste: arquivo inexistente não altera o Top-10")
    top = TopCovardes(10)
    top.consultar_arquivo(caminho_regiao("centro.txt"))
    antes = top_como_tuplas(top)
    saida = io.StringIO()
    original = sys.stdout
    sys.stdout = saida
    try:
        processar(top, "consultar nao_existe.txt")
    finally:
        sys.stdout = original
    verificar("não encontrado" in saida.getvalue(), "CLI avisa que o arquivo não existe")
    verificar(top_como_tuplas(top) == antes, "Top-10 permanece igual")


def testar_comandos_da_cli():
    print("teste: comandos da CLI")
    top = TopCovardes(10)
    saida = io.StringIO()
    original = sys.stdout
    sys.stdout = saida
    try:
        continua_vazio = processar(top, "mostrar")
        processar(top, "consultar " + caminho_regiao("centro.txt"))
        processar(top, "mostrar")
        processar(top, "limpar")
        processar(top, "ajuda")
        processar(top, "xyz")
        continua_apos_comandos = processar(top, "")
        encerra = processar(top, "sair")
    finally:
        sys.stdout = original
    texto = saida.getvalue()
    verificar(continua_vazio, "comando 'mostrar' mantém o laço rodando")
    verificar("Nenhuma criança na lista." in texto, "mensagem de lista vazia")
    verificar("1. Stephanie_Price 16" in texto, "formato numerado da listagem")
    verificar("Lista esvaziada." in texto, "mensagem de limpar")
    verificar("Comandos disponíveis:" in texto, "comando ajuda imprime a lista")
    verificar("Comando desconhecido" in texto, "comando inválido é avisado")
    verificar(continua_apos_comandos, "linha em branco não encerra o programa")
    verificar(encerra is False, "comando 'sair' encerra o laço")


def testar_comandos_sem_diferenciar_maiusculas():
    print("teste: comandos aceitos em maiúsculas")
    top = TopCovardes(10)
    saida = io.StringIO()
    original = sys.stdout
    sys.stdout = saida
    try:
        processar(top, "MOSTRAR")
    finally:
        sys.stdout = original
    verificar("Nenhuma criança na lista." in saida.getvalue(), "'MOSTRAR' funciona")


def principal():
    testes = [
        testar_heap_basico,
        testar_capacidade_nunca_excede,
        testar_uma_regiao,
        testar_duas_regioes,
        testar_todas_as_regioes_contra_referencia,
        testar_ordem_de_consulta_nao_importa,
        testar_limpar,
        testar_empate_lexicografico,
        testar_linhas_vazias_e_formato,
        testar_arquivo_inexistente_preserva_estado,
        testar_comandos_da_cli,
        testar_comandos_sem_diferenciar_maiusculas,
    ]
    for teste in testes:
        teste()
        print()
    if _falhas:
        print("{} verificação(ões) falharam:".format(len(_falhas)))
        for descricao in _falhas:
            print("  - {}".format(descricao))
        return 1
    print("Todos os testes passaram.")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
