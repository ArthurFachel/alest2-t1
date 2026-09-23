# Pennywise e as 10 crianças mais covardes

Trabalho 1 de Algoritmos e Estruturas de Dados II (ALEST II) — PUCRS.

CLI interativa que mantém, em memória, as **10 crianças mais covardes** de
Derry vistas até o momento, lendo os arquivos de região em **fluxo** e
guardando o resultado em uma **fila de prioridade (heap binário)**.

Quanto menor o escore, mais covarde a criança.

## Como executar

```bash
python3 pennywise.py
```

O caminho dos arquivos é relativo ao diretório de execução. Os cinco
arquivos de teste estão em `regioes/`.

### Comandos

| Comando              | Efeito                                                              |
|----------------------|---------------------------------------------------------------------|
| `consultar <arquivo>`| Lê a região, uma criança por vez, e atualiza o Top-10.              |
| `mostrar`            | Exibe as até 10 crianças, da mais covarde para a menos covarde.     |
| `limpar`             | Esvazia a estrutura. O Top-10 recomeça vazio.                       |
| `ajuda`              | Lista os comandos disponíveis.                                      |
| `sair`               | Encerra o programa.                                                 |

### Sessão de exemplo

```
Pennywise> consultar regioes/centro.txt
Região regioes/centro.txt lida.
Pennywise> mostrar
Crianças no Top-10:
1. Stephanie_Price 16
2. Stephen_Adams 23
3. Don_Hagarty 25
4. Betty_Ripsom 26
5. Sally_Mueller 30
6. Sonia_Kaspbrak 31
7. Greta_Bowie 48
8. Zack_Denbrough 50
9. Adrian_Mellon 58
10. Casey_Tremblay 61
Pennywise> consultar regioes/neibolt.txt
Região regioes/neibolt.txt lida.
Pennywise> mostrar
Crianças no Top-10:
1. Oscar_Wilson 5
2. Victor_Murray 7
3. Kay_Powell 10
4. Linda_Thompson 14
5. Stephanie_Price 16
6. Philip_Johnson 22
7. Stephen_Adams 23
8. Don_Hagarty 25
9. Betty_Ripsom 26
10. Sally_Mueller 30
Pennywise> limpar
Lista esvaziada.
Pennywise> mostrar
Nenhuma criança na lista.
Pennywise> sair
```

## Estrutura do projeto

| Arquivo               | Responsabilidade                                                    |
|-----------------------|---------------------------------------------------------------------|
| `pennywise.py`        | Interface de linha de comando: laço de comandos e mensagens.        |
| `top_covardes.py`     | Regra do Top-K e leitura em fluxo dos arquivos de região.           |
| `fila_prioridade.py`  | Heap binário de máximo com capacidade fixa (`subir` / `descer`).    |
| `crianca.py`          | Item armazenado: nome, escore e a chave de comparação.              |
| `testes.py`           | Bateria de testes, sem framework externo.                           |
| `regioes/`            | Os cinco arquivos de teste fornecidos com o enunciado.              |

## A solução

### Por que uma fila de prioridade de MÁXIMO

O objetivo é guardar as `K = 10` **menores** chaves de um fluxo. Quando a
estrutura já está cheia e chega uma criança nova, quem precisa sair é a
**menos covarde** entre as armazenadas, isto é, a de **maior** escore.

Uma max-heap mantém exatamente esse candidato ao descarte na raiz:

* consultar a pior guardada: `O(1)` (é `vetor[1]`);
* trocar a raiz pela criança nova: `O(log K)`.

Com uma min-heap, achar quem descartar exigiria varrer as folhas.

### O laço de atualização

Para cada criança lida:

1. se ainda cabe (`tamanho < K`), insere e faz `subir` (*swim*);
2. senão, compara com a raiz:
   * mais covarde que a raiz → `substituir_maximo`, que troca a raiz e faz
     `descer` (*sink*) uma única vez;
   * caso contrário, descarta a criança na hora.

### Representação do heap

Como nos slides da disciplina (Sedgewick, seção 2.4), a árvore binária
completa vive em um vetor **indexado a partir de 1**, sem ponteiros:

* pai do nó `k`: `k // 2`
* filhos do nó `k`: `2k` e `2k + 1`

A posição 0 fica propositalmente vazia para que essa aritmética valha.

### Desempate

A chave de comparação é a tupla `(escore, nome)`. Escores iguais são
desempatados pela **ordem lexicográfica do nome** — política determinística
e usada de forma consistente tanto na seleção quanto na exibição.

### Complexidade

Com `N` crianças lidas e `K = 10`:

| Operação                | Tempo      | Espaço |
|-------------------------|------------|--------|
| `inserir` / `remover`   | `O(log K)` | —      |
| processar um arquivo    | `O(N log K)` | `O(K)` |
| `mostrar`               | `O(K log K)` | `O(K)` |

O espaço é `O(K)` e **não** depende de `N`: é o ponto central do trabalho.

## Restrições do enunciado e como foram atendidas

* **Máximo de 10 crianças armazenadas** — a capacidade do heap é fixada no
  construtor; `inserir` levanta erro se a fila já estiver cheia, e o laço do
  Top-K nunca ultrapassa `K` porque usa `substituir_maximo`.
  Verificado em `testar_capacidade_nunca_excede`.
* **Proibido carregar o arquivo inteiro** — `consultar_arquivo` itera sobre o
  objeto de arquivo linha a linha; a linha é processada e descartada. Não há
  `readlines()`, `list()` nem acumulador do conteúdo do arquivo.
* **Proibido usar outra estrutura para o resultado** — a única estrutura que
  guarda crianças é `FilaPrioridadeMaxima`. A exceção prevista no enunciado é
  o vetor temporário de no máximo 10 posições em `listar_ordenado()`, usado
  só para imprimir; ele não altera o heap, que segue sendo o estado canônico.
* **Sem persistência em disco** — o estado vive só na memória e `limpar` o
  zera.
* **Sem listas de crianças no código-fonte** — os nomes vêm apenas dos
  arquivos informados em tempo de execução.
* **Arquivo inexistente** — o programa avisa e o Top-10 permanece intacto.
* **Linhas vazias** — ignoradas na leitura.

## Testes

```bash
python3 testes.py
```

A bateria cobre:

* operações básicas do heap (inserir, remover máximo, limpar);
* o limite de 10 itens nunca ser ultrapassado, região a região;
* os dois Top-10 da sessão de exemplo do enunciado, valor a valor;
* o Top-10 das cinco regiões comparado com uma referência ingênua que
  carrega tudo e ordena (o algoritmo em fluxo tem que dar o mesmo resultado);
* independência da ordem em que as regiões são consultadas;
* `limpar` zerando o estado de fato;
* desempate lexicográfico entre escores iguais;
* linhas vazias ignoradas e escore inválido detectado;
* arquivo inexistente preservando o Top-10;
* todos os comandos da CLI, incluindo comando desconhecido e linha em branco.
