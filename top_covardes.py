"""Top-K das crianças mais covardes, mantido em fluxo sobre os arquivos.

Regras do trabalho respeitadas aqui:
  * no máximo K = 10 crianças armazenadas a qualquer momento;
  * o arquivo NUNCA é carregado inteiro: lê-se linha a linha, atualiza-se
    o heap e a linha é descartada;
  * a única estrutura que guarda o resultado é a fila de prioridade.
"""

from crianca import Crianca
from fila_prioridade import FilaPrioridadeMaxima

CAPACIDADE_PADRAO = 10


class ErroDeFormato(Exception):
    """Linha do arquivo de região fora do formato NOME ESCORE."""


class TopCovardes:
    """Mantém as K crianças mais covardes vistas até agora."""

    def __init__(self, capacidade=CAPACIDADE_PADRAO):
        self._fila = FilaPrioridadeMaxima(capacidade)

    def quantidade(self):
        return self._fila.tamanho()

    def capacidade(self):
        return self._fila.capacidade()

    def esta_vazio(self):
        return self._fila.esta_vazia()

    def limpar(self):
        self._fila.limpar()

    # ------------------------------------------------------------------
    def oferecer(self, crianca):
        """Considera uma criança para o Top-K.

        Enquanto sobrar espaço, insere. Depois disso, só entra quem for
        mais covarde que a atual pior do conjunto (a raiz da max-heap),
        que é então descartada. Custo O(log K) por criança.
        """
        if not self._fila.esta_cheia():
            self._fila.inserir(crianca)
            return True
        if crianca.eh_mais_covarde_que(self._fila.maximo()):
            self._fila.substituir_maximo(crianca)
            return True
        return False

    # ------------------------------------------------------------------
    def consultar_arquivo(self, caminho):
        """Lê o arquivo em fluxo e atualiza o Top-K. Devolve quantas linhas leu.

        Levanta FileNotFoundError se o arquivo não existir; nesse caso o
        estado do Top-K não é tocado, porque nada chegou a ser lido.
        """
        lidas = 0
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for numero, linha in enumerate(arquivo, start=1):
                linha = linha.strip()
                if not linha:  # linhas vazias são ignoradas
                    continue
                self.oferecer(self._interpretar_linha(linha, numero))
                lidas += 1
                # A linha sai de escopo aqui: nada do arquivo é acumulado.
        return lidas

    @staticmethod
    def _interpretar_linha(linha, numero):
        partes = linha.split()
        if len(partes) != 2:
            raise ErroDeFormato(
                "linha {}: esperado 'NOME ESCORE', veio {!r}".format(numero, linha)
            )
        nome, texto_escore = partes
        try:
            escore = int(texto_escore)
        except ValueError:
            raise ErroDeFormato(
                "linha {}: escore {!r} não é um inteiro".format(numero, texto_escore)
            ) from None
        return Crianca(nome, escore)

    # ------------------------------------------------------------------
    def listar_ordenado(self):
        """Devolve as crianças da mais covarde para a menos covarde.

        Exceção prevista no enunciado: usa-se um vetor temporário de no
        máximo K posições SOMENTE para exibir. O estado canônico segue
        sendo o heap, que não é alterado por esta chamada.
        """
        temporario = list(self._fila.itens())
        temporario.sort(key=lambda c: c.chave())
        return temporario
