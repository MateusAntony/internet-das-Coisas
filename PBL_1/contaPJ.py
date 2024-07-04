from contaBancaria import Conta

class ContaPJ(Conta):
    def __init__(self,numero,saldo,senha,cnpj):
        super().__init__(numero,saldo,senha)
        self.cnpj= cnpj
