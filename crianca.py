"""Representa uma criança de Derry com seu score de covardia.

Quanto MENOR o score, mais covarde a criança. A política de desempate
é determinística: scores iguais são desempatados pelo nome (nome menor = mais covarde).
"""


class Crianca:
    """Item imutável guardado na fila de prioridade."""

    __slots__ = ("nome", "score")

    def __init__(self, nome, score):
        self.nome = nome
        self.score = score

    def chave(self):
        """Chave de comparação canônica: (escore, nome).

        Comparar tuplas resolve o desempate lexicográfico de graça.
        """
        return (self.score, self.nome)

    def eh_mais_covarde_que(self, outra):
        """True se esta criança for mais covarde (vem antes) que a outra."""
        return self.chave() < outra.chave()

    def __repr__(self):
        return "Crianca({!r}, {!r})".format(self.nome, self.score)
