from contaFisica import ContaFisica
from contaPJ import ContaPJ
from contaConjunta import ContaConjunta
from threading import Lock 
import time

class Banco:
    def __init__(self, nome):
        self.nome= nome
        self.contas={}
        self.lock= Lock()
        self.locks={}
        self.transacoes_preparadas={}

    def criar_contaPF(self,numero,saldo,senha,cpf):
        with self.lock:
            if cpf in self.contas and self.contas[cpf]['numero'] == numero:
                print("Cliente já existe nesse banco")
                return False
            conta=ContaFisica(numero,saldo,senha,cpf)
            self.contas[conta.numero] = {'numero': conta.numero, 'saldo': conta.saldo, 'senha': conta.senha, 'cpf': conta.cpf}
            return conta

    
    def criar_contaPJ(self,numero,saldo,senha,cnpj):
        with self.lock:
            if cnpj in self.contas and self.contas[cnpj]['numero'] == numero:
                print("Cliente já existe nesse banco")
                return False
            else:
                conta=ContaPJ(numero,saldo,senha,cnpj)
                self.contas[conta.numero] = {'numero': conta.numero, 'saldo': conta.saldo, 'senha': conta.senha,'cpf': conta.cnpj}
                return conta
        
    def criar_contaConjunta(self,numero,saldo,senha,cpf1,cpf2):
        with self.lock:
            if (cpf1 in self.contas and self.contas[cpf1]['numero'] == numero) or (cpf2 in self.contas and self.contas[cpf2]['numero'] == numero):
                print("Cliente já tem uma conta nesse banco")
                return False
            else:
                conta=ContaConjunta(numero,saldo,senha,cpf1,cpf2)
                self.contas[conta.numero] = {'numero': conta.numero, 'saldo': conta.saldo, 'senha': conta.senha,'cpf1': conta.cpf1,'cpf2': conta.cpf2}
                return conta

    def get_conta(self,cpf_ou_cnpj,numero):
        with self.lock:
            conta = self.contas.get(numero)
            if conta:
                return conta
            return False
    
    def get_conta_por_cpf(self, cpf_ou_cnpj):
        with self.lock:
            contas_encontradas = []
            for numero, conta_info in self.contas.items():
                if conta_info.get('cpf') == cpf_ou_cnpj or conta_info.get('cnpj') == cpf_ou_cnpj or  conta_info.get('cpf1') == cpf_ou_cnpj or conta_info.get('cpf2') == cpf_ou_cnpj:
                    contas_encontradas.append(conta_info)
            return contas_encontradas if contas_encontradas else None
        
    def verificar_credenciais(self, cpf_ou_cnpj, senha,numero):
        with self.lock:
            conta = self.contas.get(numero)
            if conta and conta['senha'] == senha:
                return True
            return False
    
    def retirada(self,cpf_ou_cnpj,numero,valor):
        with self.lock:
            conta = self.contas.get(numero)
            if conta['saldo'] >= valor:
                    conta['saldo'] -= valor
                    return True
            return False
    
    def add(self,cpf_ou_cnpj,numero,valor):
        with self.lock:
            conta = self.contas.get(numero)
            conta['saldo'] += valor
            return True
    
    def lock_conta(self,numero):
        if numero not in self.locks:
            self.locks[numero]= Lock()
        self.locks[numero].acquire()
    
    def unlock_conta(self,numero):
        if numero in self.locks:
            self.locks[numero].release()
        
    def preparar(self,cpf,numero,valor):
        self.lock_conta(numero)
        try:
            time.sleep(1)
            if self.retirada(cpf,numero,valor):
                self.transacoes_preparadas[(cpf,numero)] = valor
                return True
            return False
        finally:
            self.unlock_conta(numero)
    
    def confirmar(self,numero,cpf):
        self.lock_conta(numero)
        try:
            if (cpf,numero) in self.transacoes_preparadas:
                valor= self.transacoes_preparadas.pop((cpf,numero))    
                return True
            return False
        finally:
            self.unlock_conta(numero)

    def rollback(self,numero,cpf):
        self.lock_conta(numero)
        try:
            if (cpf,numero) in self.transacoes_preparadas:
                valor= self.transacoes_preparadas.pop((cpf,numero))
                self.add(cpf,numero,valor)
                return True
            return False
        finally:
            self.unlock_conta(numero)


