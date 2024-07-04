from contaBancaria import Conta

class ContaFisica(Conta):
    def __init__(self,numero,saldo,senha,cpf):
        super().__init__(numero,saldo,senha)
        self.cpf=cpf
