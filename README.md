# Problema 1: Internet das Coisas
**Autor**:Mateus Antony Medeiros Carvalho

**Departamento de Tecnologia** – Universidade Estadual de Feira de Santana (UEFS) 44036–900 – Feira de Santana – Bahia

**Resumo:** Uma startup que desenvolve dispositivos, adicionando capacidades de rede aos produtos, ainda não estabeleceu a comunicação entre os dispositivos e suas diversas aplicações. Nesse contexto, foi solicitado o desenvolvimento de um serviço para facilitar essa comunicação. Propusemos um serviço distribuído de comunicação utilizando o protocolo TCP/IP para comandos e uma abordagem não confiável para dados. Foi criado com sucesso um dispositivo virtual simulado para geração de dados fictícios, além de ser disponibilizada uma API RESTful para garantir a eficiente troca de dados e comandos.

## Índice
1. [Introdução](#introducao)
2. [Barema avaliativo](#Barema-avaliativo)
3. [Arquitetura da Solução](#Arquitetura-da-Solução)
4. [Protocolo de comunicação entre dispositivo e Broker](#Protocolo-de-comunicação-entre-dispositivo-e-Broker)
5. [Interface da Aplicação](#Interface-da-Aplicação)
6. [Formatacao, envio, tratamento de dados e Tratamento de conexões simultaneas](#Formatacao,-envio,-tratamento-de-dados-e-Tratamento-de-conexões-simultaneas)
7. [Considerações Finais](#Considerações-Finais)
8. [Conclusão](#conclusão)
9. [Como Usar](#como-usar)

<a id="introducao"></a>

## Introdução

Com a crescente atenção que o sistema de Internet das Coisas (Internet of Things, IoT) tem recebido por parte das instituições acadêmicas e empresas, devido à variedade de áreas que podem ser alcançadas por tal tecnologia, surge a necessidade de desenvolver middlewares distribuídos e aplicá-los de forma eficiente. Nesse sentido, muitas empresas se deparam com o desafio da elaboração da comunicação entre seus dispositivos e suas diferentes aplicações.

Sendo assim, o desafio por parte da nossa empresa é estabelecer uma comunicação plena entre os diversos dispositivos IoT e as suas aplicações, que necessitam dos dados oferecidos por esses dispositivos. A solução para esse problema envolve a criação de um serviço broker, dispositivos virtuais simulados, manipulação e uso de contêineres Docker, e uma Interface de Programação de Aplicação (API) no modelo arquitetural RESTful oferecida pelo broker. Assim, esse projeto propõe apresentar a solução implementando os recursos citados e evidenciando na prática tópicos de concorrência e conectividade. 

<a id="Barema-avaliativo"></a>

## Barema avaliativo

<p align="center">
  <img src="https://github.com/MateusAntony/internet-das-Coisas/assets/68971638/52a65dd7-c5fb-4660-9908-fa236a30048f" alt="Descrição da Imagem">
</p>
<p align="center">
  Imagem 3: Barema avaliativo
</p>

<a id="Arquitetura-da-Solução"></a>

## Arquitetura da Solução

Foram elaborados três componentes, sendo o broker, device e client. O broker é responsável por permitir a troca de mensagens entre o cliente e o dispositivo. Já o dispositivo simula uma cerca elétrica, contendo tudo aquilo que tem relação com o disposiivo virtual, seus métodos, atributos e estado da cerca elétrica. O client é uma interface disponibilizada no terminal onde vai lidar com as entradas do cliente.

Referente a sua comunicação,o dispositivo que se conecta ao broker,ou seja, é necessário executar o broker, logo após o dispositivo vai se conectar ao broker com uma conexão TCP. Além disso, o cliente se conecta ao broker atrevés de solitações http.

A respeito da ordem de mensagens trocada, elas se baseiam de acordo com a listagem abaixo:

1. Cliente envia uma requisição http para o broker;
2. O broker recebe a requisição feita e enviar um comando específico utilizando protocolo TCP para o dispositivo;
3. O dispositovo recebe o comando, trata e devolve os dados para o broker usando um abordagem UDP;
4. O broker avalia o dado, formata e envia para o cliente

<a id="Protocolo-de-comunicação-entre-dispositivo-e-Broker"></a>

## Protocolo de comunicação entre dispositivo e Broker

Foi utilizado o envio de comandos, como por exemplo: ON,OFF e RESTART para ser enviado para o dispositivo, onde ele recebe-o, muda o seu estado e envia uma confimação para o broker.

Para o envio de dados por parte dos dispositivos foi utilizada uma abordagem não confiável, ou seja, o dispositido envia dados UDP para o broker, já para lidar com os comandos recebidos, o broker envia para o dispositivo usando socket nativo TCP/IP como abordagem confiável, onde garante a entrega do comando entre o broker e o dispositivo virtual.

<a id="Interface-da-Aplicação"></a>

## Interface da Aplicação 

Foi desenvolvida uma API RESTful por meio do serviço broker, utilizando o framework Flask. Foi Realizado testes funcionais e de interação que têm como objetivo verificar e analisar as saídas da aplicação junto com o comportamento de cada módulo do projeto, com o propósito de prever possíveis erros e falhas do sistema. Também houve a realização de teste das rotas da API através do Postman, que permitiu simular solicitações HTTP.

Ocorreu a utilização dos verbos POST, GET E DELETE. Houve o desenvolvimento de um total de seis rotas da API, entre elas estão as rotas que interagem diretamente com o dispositivo, rotas como de ligar, desligar e reiniciar o dispositvo virtual. Outrossim, foi elaborado a rota de listagem de dispositvo apartir do seu id, usado para exibir a lista de dispositivos cadastrados, servindo no auxilio da funcionalidade de selecionar o dispositivo especifico. 

Além disso, temos a rota de conectar cliente e desconecta-lo, essa rota é responsável por lidar com id do cliente e permitir que haja a interação entre a inteface no terminal do usuário e o broker.


<a id="Formatacao,-envio,-tratamento-de-dados-e-Tratamento-de-conexões-simultaneas"></a>

## Formatacao, envio, tratamento de dados e Tratamento de conexões simultaneas
 

Houve a adoção de threads para lidar com a comunicação simultânea lidando com os dados UDP no broker, como também para executar o servidor broker junto com APIREST. Foi usado no arquivo do dispositivo virtual para receber os comando pelo broker e para enviar dados para o broker. Ocorreu o emprego  do Lock, tanto no broker quanto no dispositivo, para impedir que ocorra uma condição de corrida entre threads, ou seja, somente uma thread pode acessar um recurso compartilhado por vez. 

Vale ressaltar que verificou-se a necessidade de implementar uma fila para lidar com os dados recebidos pelos dispositivos, armazenando em ordem de chegada, e liberando obedecendo a ordem estabelecida. Além disso, foi utlizado o json para formatar o dados enviados para o cliente e os dados que são mostrados pelo broker. 
 
<a id="Considerações-Finais"></a>

## Considerações Finais

Foi implementado funcionalidades de controle, onde o usuário tem a possibilidade de ligar, reiniciar e desligar para interagir com o dispositivo selecionado.

Não houve a elaboração de uma interface gráfica, sendo de preferência do autor realizar as saídas e interagir com o próprio usuário através do próprio terminal.

Contudo, a respeito da confiabilidade, quando ao tirar ou realocar o cabo de rede de alguns dos nós, o sistema é interrompido, não cumprindo um dos requisitos necessários. Por fim, foi empregado o Docker para criar containers e imagens.


<a id="conclusao"></a>

## Conclusão

Ao testar e finalizar a solução, foi observado que grande parte dos requisitos exigidos foram cumpridos. As abordagens relacionadas a essa problemática permitiram que saíssemos do campo teórico percebendo a importância tanto do uso de alguns protocolos, a implementação de threads, além de nos apresentar conceitos e ferramentas que nunca tínhamos trabalhado a respoeito de redes. Em suma, esse projeto foi de ampla importância para o desenvolvimento de desenvolvedores e profissionais na área.

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
- Passo 1: Selecione o dispositivo
- Passo 2: Ligue
- Passo 3: Desligue
5. **Explorar outras funcionalidades:**
- Passo 1: Desconecte o device do sistema
- Passo 5: Desconecte o broker do sistema 


  



