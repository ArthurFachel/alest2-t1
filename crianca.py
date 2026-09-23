"""Representa uma criança de Derry com seu escore de covardia.

Quanto MENOR o escore, mais covarde a criança. A política de desempate
adotada no trabalho inteiro é determinística: escores iguais são
desempatados pela ordem lexicográfica do nome (nome menor = mais covarde).
"""


class Crianca:
    """Item imutável guardado na fila de prioridade."""

    __slots__ = ("nome", "escore")

    def __init__(self, nome, escore):
        self.nome = nome
        self.escore = escore

    def chave(self):
        """Chave de comparação canônica: (escore, nome).

        Comparar tuplas resolve o desempate lexicográfico de graça.
        """
        return (self.escore, self.nome)

    def eh_mais_covarde_que(self, outra):
        """True se esta criança for mais covarde (vem antes) que a outra."""
        return self.chave() < outra.chave()

    def __repr__(self):
        return "Crianca({!r}, {!r})".format(self.nome, self.escore)
