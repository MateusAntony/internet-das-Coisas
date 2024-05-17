# Problema 1: Internet das Coisas
**Autor**:Mateus Antony Medeiros Carvalho

**Departamento de Tecnologia** – Universidade Estadual de Feira de Santana (UEFS) 44036–900 – Feira de Santana – Bahia

**Resumo:** Uma startup que desenvolve dispositivos, adicionando capacidades de rede aos produtos, ainda não estabeleceu a comunicação entre os dispositivos e suas diversas aplicações. Nesse contexto, foi solicitado o desenvolvimento de um serviço para facilitar essa comunicação. Propusemos um serviço distribuído de comunicação utilizando o protocolo TCP/IP para comandos e uma abordagem não confiável para dados. Foi criado com sucesso um dispositivo virtual simulado para geração de dados fictícios, além de ser disponibilizada uma API RESTful para garantir a eficiente troca de dados e comandos.

## Índice
1. [Introdução](#introducao)
2. [Metodologia](#Arquitetura-da-Solução)
3. [Resultado e Discussões](#resultado-e-discussoes)
4. [Conclusão](#conclusao)
5. [Como Usar](#como-usar)


## Introdução
<a id="introducao"></a>

Com a crescente atenção que o sistema de Internet das Coisas (Internet of Things, IoT) tem recebido por parte das instituições acadêmicas e empresas, devido à variedade de áreas que podem ser alcançadas por tal tecnologia, surge a necessidade de desenvolver middlewares distribuídos e aplicá-los de forma eficiente. Nesse sentido, muitas empresas se deparam com o desafio da elaboração da comunicação entre seus dispositivos e suas diferentes aplicações.

Sendo assim, o desafio por parte da nossa empresa é estabelecer uma comunicação plena entre os diversos dispositivos IoT e as suas aplicações, que necessitam dos dados oferecidos por esses dispositivos. A solução para esse problema envolve a criação de um serviço broker, dispositivos virtuais simulados, manipulação e uso de contêineres Docker, e uma Interface de Programação de Aplicação (API) no modelo arquitetural RESTful oferecida pelo broker. Assim, esse projeto propõe apresentar a solução implementando os recursos citados e evidenciando na prática tópicos de concorrência e conectividade. 

## Arquitetura da Solução
<a id=" Arquitetura-da-Solução"></a>

Para o envio de dados por parte dos dispositivos foi utilizada uma abordagem não confiável, ou seja, o dispositido envia dados UDP para o broker, já para lidar com os comandos recebidos, o broker envia para o dispositivo usando socket nativo TCP/IP como abordagem confiável, onde garante a entrega do comando entre o broker e o dispositivo virtual.

Foi implementado funcionalidades de controle, onde o usuário tem a possibilidade de ligar, reiniciar e desligar para interagir com o dispositivo selecionado. Foi desenvolvida uma API RESTful por meio do serviço broker, utilizando o framework Flask. Foi Realizado testes funcionais e de interação que têm como objetivo verificar e analisar as saídas da aplicação junto com o comportamento de cada módulo do projeto, com o propósito de prever possíveis erros e falhas do sistema. Foi feito teste das rotas da API através do Postman, que permitiu simular solicitações HTTP.

Houve a adoção de threads para lidar com a comunicação simultânea, para lidar com os dados UDP no broker, para executar o servidor broker junto com APIREST e usando no arquivo do dispositivo virtual para receber os comando pelo broker e para enviar dados para o broker. Ocorreu o emprego  do Lock para impedir que ocorra uma condição de corrida entre threads, ou seja, somente uma thread pode acessar um recurso compartilhado por vez. 

Vale ressaltar que verificou-se a necessidade de implementar uma fila para lidar com os dados recebidos pelos dispositivos, armazenando em ordem de chegada, e liberando obedecendo a ordem estabelecida.

Ademais, logo abaixo o barema avaliativo onde contém todas as funcionalidades que deve compor o programa para o funcionamente eficiênte:


<p align="center">
  <img src="https://github.com/MateusAntony/internet-das-Coisas/assets/68971638/52a65dd7-c5fb-4660-9908-fa236a30048f" alt="Descrição da Imagem">
</p>
<p align="center">
  Imagem 3: Barema avaliativo
</p>

## Resultado e Discussões
<a id="resultado-e-discussoes"></a>

Ao testar e finalizar a solução, foi observado que grande parte dos requisitos exigidos foram cumpridos. Houve o desenvolvimento dos componentes, onde o Broker se comunica com o Device e o Client, já o Device só se comunica com o Broker semelhantemente ao Client. 

<p align="center">
  <img src="https://github.com/MateusAntony/internet-das-Coisas/assets/68971638/b5d8287c-c088-4534-85df-7fb7e83f0ce1" alt="Descrição da Imagem">
</p>
<p align="center">
  Imagem 4: Duas Thread sendo utilizadas no dispostivo, uma é para receber os comandos do broker e outra para enviar
</p>

Assim, foi utilizado TCP/IP para lidar com o comando que parte do Broker para o Device, e UDP para lidar com os dados que partem do Device e vão até o broker. A comunicação que é feita entre Broker e Client é baseada em HTTP. Foi elaborado funções para tratar os dados específicos, permitindo a compreensão das mensagens.


<p align="center">
  <img src="https://github.com/MateusAntony/internet-das-Coisas/assets/68971638/cbee7f8b-3acc-4402-90bc-6535c0d5193d" alt="Configuração para aceitar conexões TCP.">
</p>

<p align="center">
  Imagem 5: Configuração para aceitar conexões TCP.
</p>

<p align="center">
  <img src="https://github.com/MateusAntony/internet-das-Coisas/assets/68971638/9fc662d1-e6ae-40e3-93bf-f51513e4ec20" alt="Configuração para aceitar conexões TCP.">
</p>

<p align="center">
  Imagem 6: Função responsável por tratar os comandos que o broker envia para o device.
</p>



Foi criado um total de 7 rotas, sendo rota de reiniciar, ligar e desligar o dispositivo, rota para listagem de dispositivos e rotas para tratar com a conexão e desconexão do cliente. Sendo assim, é possível ligarmos, desligarmos e selecionarmos um dispositivo específico, além da funcionalidade de listagem dos dispositivos.

<p align="center">
  <img src="https://github.com/MateusAntony/internet-das-Coisas/assets/68971638/438b7cb4-7a36-4f90-9956-a0b964a2e863" alt="Método que chama a função de enviar o comando para o dispositivo e logo após enviar os dados formatadas para o cliente.">
</p>

<p align="center">
  Imagem 7: Método que chama a função de enviar o comando para o dispositivo e logo após enviar os dados formatados para o cliente.
</p>


Não houve a elaboração de uma interface gráfica, sendo de preferência do autor realizar as saídas e interagir com o próprio usuário através do próprio terminal.

<p align="center">
  <img src="https://github.com/MateusAntony/internet-das-Coisas/assets/68971638/4aebe0ba-ca03-4ed0-8786-54a275b164a1" alt="Método que chama a função de enviar o comando para o dispositivo e logo após enviar os dados formatadas para o cliente.">
</p>

<p align="center">
  Imagem 7: Interface no terminal
</p>


Contudo, a respeito da confiabilidade, quando tentado tirar ou realocar os cabos de alguns dos nós, o sistema é interrompido, não cumprindo um dos requisitos necessários. Outrossim, a respeito do desempenho embora tenha usado threads, dicionários e filas, o objetivo central não para o autor era cumprir a funcionalidade principal, ou seja, a comunicação não atentando especificamente para uma melhora no tempo da aplicação. Por fim, o sistema dorcker não foi implementado de um maneira efetiva, ou seja, a solução funcionará rodando sem utilizar o docker

## Conclusão
<a id="conclusao"></a>

Embora não atingindo o resultado que esperava, as abordagens relacionadas a essa problemática permitiram que saíssemos do campo teórico percebendo a importância tanto do uso de alguns protocolos, a implementação de threads, além de nos apresentar conceitos e ferramentas que nunca tínhamos trabalhado. Em suma, esse projeto foi de ampla importância para o desenvolvimento de desenvolvedores e profissionais na área.

## Como Usar
<a id="como-usar"></a>

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


  



