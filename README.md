# Problema 1: Internet das Coisas


**Resumo:** Uma startup que desenvolve dispositivos, adicionando capacidades de rede aos produtos, ainda não estabeleceu a comunicação entre os dispositivos e suas diversas aplicações. Nesse contexto, foi solicitado o desenvolvimento de um serviço para facilitar essa comunicação. Propusemos um serviço distribuído de comunicação utilizando o protocolo TCP/IP para comandos e uma abordagem não confiável para dados. Foi criado com sucesso um dispositivo virtual simulado para geração de dados fictícios, além de ser disponibilizada uma API RESTful para garantir a eficiente troca de dados e comandos.

## Introdução

Com a crescente atenção que o sistema de Internet das Coisas (Internet of Things, IoT) tem recebido por parte das instituições acadêmicas e empresas, devido à variedade de áreas que podem ser alcançadas por tal tecnologia, surge a necessidade de desenvolver middleware distribuídos e aplicá-los de forma eficiente. Nesse sentido, muitas empresas se deparam com o desafio da elaboração da comunicação entre seus dispositivos e suas diferentes aplicações. 
  
Sendo assim, o desafio por parte da nossa empresa é estabelecer uma comunicação plena entre os diversos dispositivos IoT e as suas aplicações, que necessitam dos dados oferecidos por esses dispositivos. A solução para esse problema envolve a criação de um serviço broker, dispositivos virtuais simulados, manipulação e uso de contêineres Docker, e uma Interface de Programação de Aplicação (API) no modelo arquitetural RESTful oferecida pelo broker. Assim, esse projeto propõe apresentar a solução implementando os recursos citados e evidenciando na prática tópicos de concorrência e conectividade. 

## Metodologia
- Para o envio de dados por parte dos dispositivos foi utilizado um abodagem não confiavel, ou mais especificamente UDP, já para lidar com os comandos recebidos foi usado um abordagem confiável, usando socket nativo TCP/IP, onde garantia a entrega entre o broker e o dispositivo virtual.
- Foi implementado funcionalidades de controle, como ligar, reiniciar e desligar, para interagir com o dispositivo selecionado., além de possiblidade de visualizar os dados.
- Foi desenvolvido uma ApiRESTfull por meio do serviço broker.
- Foi realizados testes funcionais e de interação que tem como objetivo verificar e analisar as saídas da aplicação junto com o comportamento de cada môdulo do projeto, com o propósito de prever possíveis erros e falhas do sistema.
- Foi feito teste das rotas da Api através do Postman, que permitiu simular solicitações HTTP.


## Como Usar

Para utilizar este projeto, siga os seguintes passos:


1. **Clonar o repositório**
2. **Configurar o ambiente**
3.  **Executar o projeto**
- Passo 1: Execute o broker
- Passo 2: Execute o device
- Passo 3: Execute o client
4. **Interagir com o projeto:**
- Passo 1: Selecione um dispositivo
- Passo 2: Ligue
- Passo 3: Desligue
- Passo 4: Selecione outro
- Passo 5: Repita o passo 2 e 3
5. **Explorar outras funcionalidades:**
- Passo 1: Desconecte o device do sistema
- Passo 5: Desconecte o broker do sistema 


  



