"""Fila de prioridade de máximo (heap binário), no estilo visto em aula.

Implementação baseada nos slides de Filas de Prioridade da disciplina
(Sedgewick/Wayne, seção 2.4): árvore binária completa representada em um
vetor indexado a partir de 1, com as operações `subir` (swim) e
`descer` (sink).

Por que fila de MÁXIMO se queremos as 10 MENORES?
    Guardando as 10 menores vistas até agora, o item que precisa sair
    quando chega alguém mais covarde é justamente o MAIOR escore do
    conjunto. Uma max-heap deixa esse candidato a descarte sempre na
    raiz, com acesso em tempo constante e remoção em O(log K).

A capacidade é fixa (K = 10 no trabalho): o vetor interno nunca cresce.
"""


class FilaPrioridadeMaxima:
    """Heap binário de máximo com capacidade fixa.

    A prioridade de uma criança é a chave (escore, nome). "Máximo" aqui
    significa o item menos covarde armazenado, ou seja, o próximo a ser
    descartado quando a fila estiver cheia.
    """

    def __init__(self, capacidade):
        if capacidade < 1:
            raise ValueError("A capacidade da fila precisa ser pelo menos 1.")
        self._capacidade = capacidade
        # Posição 0 fica vazia de propósito: a aritmética de pai/filho
        # (pai = k // 2, filhos = 2k e 2k + 1) só vale começando em 1.
        self._vetor = [None] * (capacidade + 1)
        self._n = 0

    # ------------------------------------------------------------------
    # Consultas básicas
    # ------------------------------------------------------------------
    def esta_vazia(self):
        return self._n == 0

    def esta_cheia(self):
        return self._n == self._capacidade

    def tamanho(self):
        return self._n

    def capacidade(self):
        return self._capacidade

    def maximo(self):
        """Devolve (sem remover) o item de maior chave: a raiz do heap."""
        if self.esta_vazia():
            raise IndexError("Fila de prioridade vazia.")
        return self._vetor[1]

    # ------------------------------------------------------------------
    # Operações de modificação
    # ------------------------------------------------------------------
    def inserir(self, item):
        """Insere no fim do vetor e faz o item subir até a posição correta."""
        if self.esta_cheia():
            raise OverflowError("Fila de prioridade cheia.")
        self._n += 1
        self._vetor[self._n] = item
        self._subir(self._n)

    def remover_maximo(self):
        """Remove e devolve a raiz, trocando-a com o último e afundando-a."""
        if self.esta_vazia():
            raise IndexError("Fila de prioridade vazia.")
        maximo = self._vetor[1]
        self._trocar(1, self._n)
        self._vetor[self._n] = None  # evita "lixo" (referência pendurada)
        self._n -= 1
        self._descer(1)
        return maximo

    def substituir_maximo(self, item):
        """Troca a raiz pelo item e reorganiza o heap.

        Equivale a `remover_maximo()` seguido de `inserir(item)`, mas com
        um único `descer`, sem passar pelo estado intermediário.
        """
        if self.esta_vazia():
            raise IndexError("Fila de prioridade vazia.")
        antigo = self._vetor[1]
        self._vetor[1] = item
        self._descer(1)
        return antigo

    def limpar(self):
        """Esvazia a fila, liberando as referências guardadas."""
        for i in range(1, self._n + 1):
            self._vetor[i] = None
        self._n = 0

    # ------------------------------------------------------------------
    # Auxiliares do heap
    # ------------------------------------------------------------------
    def _subir(self, k):
        """swim: enquanto o pai for menor que o filho, sobe o filho."""
        while k > 1 and self._menor(k // 2, k):
            self._trocar(k, k // 2)
            k = k // 2

    def _descer(self, k):
        """sink: enquanto houver filho maior, afunda o pai."""
        while 2 * k <= self._n:
            j = 2 * k
            if j < self._n and self._menor(j, j + 1):
                j += 1  # escolhe o maior dos dois filhos
            if not self._menor(k, j):
                break
            self._trocar(k, j)
            k = j

    # ------------------------------------------------------------------
    # Auxiliares do vetor
    # ------------------------------------------------------------------
    def _menor(self, i, j):
        """True se a chave em i for menor que a chave em j."""
        return self._vetor[i].chave() < self._vetor[j].chave()

    def _trocar(self, i, j):
        self._vetor[i], self._vetor[j] = self._vetor[j], self._vetor[i]

    # ------------------------------------------------------------------
    # Acesso somente-leitura usado apenas na impressão
    # ------------------------------------------------------------------
    def itens(self):
        """Itera sobre os itens armazenados, em ordem de vetor (não ordenada).

        Não expõe o vetor interno: quem chama não consegue alterar o heap.
        """
        for i in range(1, self._n + 1):
            yield self._vetor[i]
