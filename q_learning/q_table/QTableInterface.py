from abc import ABC, abstractmethod

from typing import List

from q_learning.AcaoMario import AcaoMario

class QTableInterface(ABC):

    @abstractmethod
    def q_table(self):
        """Devolve a tabela Q."""
        pass

    @abstractmethod
    def adicionar_novo_estado(self, ram, step, acoes: List[AcaoMario]):
        """Adiciona um novo estado à tabela Q."""
        pass

    @abstractmethod
    def get_acao_maxima(self, ram, step):
        """Retorna a ação com o maior valor Q para um estado."""
        pass

    @abstractmethod
    def estado_ja_existe(self, ram, step):
        """Verifica se um estado já existe na tabela Q."""
        pass

    @abstractmethod
    def atualiza_valor_acao_estado(self, ram, step, indice_acao, valor):
        """Atualiza o valor Q para uma determinada ação em um estado."""
        pass

    @abstractmethod
    def retorna_acoes_estado(self, ram, step) -> List[AcaoMario]:
        """Verifica se um estado já existe na tabela Q."""
        pass
