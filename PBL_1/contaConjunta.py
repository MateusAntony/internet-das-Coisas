from contaBancaria import Conta

class ContaConjunta(Conta):
    def __init__(self, numero, saldo, senha,cpf1,cpf2):
        super().__init__(numero, saldo, senha)
        self.cpf1=cpf1
        self.cpf2=cpf2