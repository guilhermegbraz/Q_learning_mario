class AcaoMario:
    def __init__(self, descricao: str, codigo: int):
        self._descricao = descricao  # Atributos privados (convenção)
        self._codigo = codigo
        self._valor = 0.0

    # Getter e setter para 'descricao'
    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, nova_descricao: str):
        if not nova_descricao:
            raise ValueError("A descrição não pode ser vazia.")
        self._descricao = nova_descricao

    # Getter e setter para 'codigo'
    @property
    def codigo(self) -> int:
        return self._codigo

    @codigo.setter
    def codigo(self, novo_codigo):
        if not isinstance(novo_codigo, int) or novo_codigo < 0:
            raise ValueError("O código deve ser um número inteiro positivo.")
        self._codigo = float(novo_codigo)

    # Getter e setter para 'valor'
    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        if not isinstance(novo_valor, (int, float)):
            raise ValueError("O valor deve ser um número não negativo.")
        self._valor = float(novo_valor)

    def copiar(self):
        acao = AcaoMario(self.descricao, self.codigo)
        return acao

    def __str__(self):
        return f"{{descricao: {self._descricao}, valor: {self._valor} }}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, AcaoMario):
            return False
        return self.codigo == other.codigo


if __name__ == "__main__":
    acoes = [
        AcaoMario("Ação de pulo", 1),
        AcaoMario("Ação de corrida", 2),
        AcaoMario("Ação de ataque", 3)
    ]

    # Imprimindo a lista de objetos
    print(acoes[0])
    print(acoes)