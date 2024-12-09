from q_learning.q_table.QTableDicionarioPosicaoStep import QTableDicionarioPosicaoStep
from q_learning.AcaoMario import AcaoMario
from typing import List, Dict
import rominfo


class QTableDicionarioState(QTableDicionarioPosicaoStep):
    def __init__(self):
        super().__init__()
        self.q_table: Dict[str, List[AcaoMario]] = {}

    def cria_chave(self, ram, step):
        state, _, _ = rominfo.getState(ram, 6)
        return f"state: {state}"

    def adiciona_elemento(self, chave: str, acoes: List[str], dicionario_codigos: dict) -> bool:
        if len(chave) >= 344:
            acoes_mario = list(map(lambda a: AcaoMario.from_string(a, dicionario_codigos), acoes))
            self.q_table[chave] = acoes_mario
            return True
        else:
            print(f"Chave com tamanho errado: {len(chave)}")
        return False

    def adiciona_elemento_step(self, step, acoes: List[str], dicionario_codigos: dict) -> bool:
        acoes_mario = list(map(lambda a: AcaoMario.from_string(a, dicionario_codigos), acoes))
        self.q_table[str(step)] = acoes_mario
        return True
