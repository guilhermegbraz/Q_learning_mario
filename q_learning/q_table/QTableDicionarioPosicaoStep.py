from q_learning.q_table.QTableInterface import QTableInterface
from q_learning.AcaoMario import AcaoMario
from typing import List, Dict
import rominfo


class QTableDicionarioPosicaoStep(QTableInterface):
    def __init__(self):
        self.q_table: Dict[str, List[AcaoMario]] = {}

    def cria_chave(self, ram, step):
        x, y, _, _ = rominfo.getXY(ram)
        return f"step: {step}, posicao {x},{y}"

    def q_table(self) -> dict:
        return self.q_table


    def adicionar_novo_estado(self, ram, step, acoes: List[AcaoMario]):
        chave = self.cria_chave(ram, step)
        if not self.estado_ja_existe(ram, step):
            acoes_zeradas = list(map(lambda acao: acao.copiar(), acoes))
            self.q_table[chave] = acoes_zeradas

    def get_acao_maxima(self, ram, step) -> AcaoMario:
        if not self.estado_ja_existe(ram, step):
            acoes = next(iter(self.q_table.values()))
            self.adicionar_novo_estado(ram, step, acoes)
        chave = self.cria_chave(ram, step)
        acao_maxima = max(self.q_table[chave], key=lambda a: a.valor)

        return acao_maxima

    def estado_ja_existe(self, ram, step):
        chave = self.cria_chave(ram, step)
        return chave in self.q_table

    def atualiza_valor_acao_estado(self, ram, step, indice_acao: int, valor: float):
        chave = self.cria_chave(ram, step)
        if not self.estado_ja_existe(ram, step):
            raise ValueError(f"O estado {chave} não está na tabela Q.")

        self.q_table[chave][indice_acao].valor = valor


    def retorna_acoes_estado(self, ram, step) -> List[AcaoMario]:
        chave = self.cria_chave(ram, step)

        return self.q_table[chave]


    def to_string(self) -> str:
        linhas = []
        for chave, valor in self.q_table.items():
            linhas.append(f"{chave}: {valor}")
        return "\n".join(linhas)
