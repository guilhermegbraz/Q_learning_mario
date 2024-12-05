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
