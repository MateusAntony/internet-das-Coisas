# Problema 1: Internet das Coisas
**Autor**:Mateus Antony Medeiros Carvalho

Departamento de Tecnologia – Universidade Estadual de Feira de Santana (UEFS) 44036–900 – Feira de Santana – Bahia


**Resumo:** Uma startup que desenvolve dispositivos, adicionando capacidades de rede aos produtos, ainda não estabeleceu a comunicação entre os dispositivos e suas diversas aplicações. Nesse contexto, foi solicitado o desenvolvimento de um serviço para facilitar essa comunicação. Propusemos um serviço distribuído de comunicação utilizando o protocolo TCP/IP para comandos e uma abordagem não confiável para dados. Foi criado com sucesso um dispositivo virtual simulado para geração de dados fictícios, além de ser disponibilizada uma API RESTful para garantir a eficiente troca de dados e comandos.

## Introdução

Com a crescente atenção que o sistema de Internet das Coisas (Internet of Things, IoT) tem recebido por parte das instituições acadêmicas e empresas, devido à variedade de áreas que podem ser alcançadas por tal tecnologia, surge a necessidade de desenvolver middlewares distribuídos e aplicá-los de forma eficiente. Nesse sentido, muitas empresas se deparam com o desafio da elaboração da comunicação entre seus dispositivos e suas diferentes aplicações.

Sendo assim, o desafio por parte da nossa empresa é estabelecer uma comunicação plena entre os diversos dispositivos IoT e as suas aplicações, que necessitam dos dados oferecidos por esses dispositivos. A solução para esse problema envolve a criação de um serviço broker, dispositivos virtuais simulados, manipulação e uso de contêineres Docker, e uma Interface de Programação de Aplicação (API) no modelo arquitetural RESTful oferecida pelo broker. Assim, esse projeto propõe apresentar a solução implementando os recursos citados e evidenciando na prática tópicos de concorrência e conectividade. 

## Metodologia
Para o envio de dados por parte dos dispositivos foi utilizada uma abordagem não confiável, ou mais especificamente UDP, já para lidar com os comandos recebidos foi usado uma abordagem confiável, usando socket nativo TCP/IP, onde garante a entrega entre o broker e o dispositivo virtual.

Foi implementado funcionalidades de controle, como ligar, reiniciar e desligar, para interagir com o dispositivo selecionado, além da possibilidade de visualizar os dados. Foi desenvolvida uma API RESTful por meio do serviço broker. Realizamos testes funcionais e de interação que têm como objetivo verificar e analisar as saídas da aplicação junto com o comportamento de cada módulo do projeto, com o propósito de prever possíveis erros e falhas do sistema. Foi feito teste das rotas da API através do Postman, que permitiu simular solicitações HTTP.

Houve a adoção de threads para lidar com a comunicação simultânea, utilizando também o Lock para impedir que ocorra uma condição de corrida entre threads, ou seja, somente uma thread pode acessar um recurso compartilhado por vez. Foi manuseado o framework Flask para o desenvolvimento da API RESTful.

Ademais, logo abaixo o barema avaliativo onde contém todas as funcionalidades que deve compor o programa para o funcionamente eficiênte:


<p align="center">
  <img src="https://github.com/MateusAntony/internet-das-Coisas/assets/68971638/52a65dd7-c5fb-4660-9908-fa236a30048f" alt="Descrição da Imagem">
</p>

## Resultado e Discussões

Ao testar e finalizar a solução, foi observado que grande parte dos requisitos exigidos foram cumpridos. Houve o desenvolvimento dos componentes, onde o Broker se comunica com o Device e o Client, já o Device só se comunica com o Broker semelhantemente ao Client. Assim, foi utilizado TCP/IP para lidar com o comando que parte do Broker para o Device, e UDP para lidar com os dados que partem do Device e vão até o broker. A comunicação que é feita entre Broker e Client é baseada em HTTP. Foi elaborado funções para tratar os dados específicos, permitindo a compreensão das mensagens.

Foi criado um total de 7 rotas, sendo rota de reiniciar, ligar e desligar o dispositivo, rota para listagem de dispositivos e rotas para tratar com a conexão e desconexão do cliente. Sendo assim, é possível ligarmos, desligarmos e selecionarmos um dispositivo específico, além da funcionalidade de listagem dos dispositivos. Não houve a elaboração de uma interface gráfica, sendo de preferência do autor realizar as saídas e interagir com o próprio usuário através do próprio terminal.

Contudo, a respeito da confiabilidade, quando tentado tirar ou realocar os cabos de alguns dos nós, o sistema é interrompido, não cumprindo um dos requisitos necessários. Outrossim, a respeito do desempenho embora tenha usado threads, dicionários e filas, o objetivo central não para o autor era cumprir a funcionalidade principal, ou seja, a comunicação não atentando especificamente para uma melhora no tempo da aplicação.

## Conclusão

Embora não atingindo o resultado que esperava, as abordagens relacionadas a essa problemática permitiram que saíssemos do campo teórico percebendo a importância tanto do uso de alguns protocolos, a implementação de threads, além de nos apresentar conceitos e ferramentas que nunca tínhamos trabalhado. Em suma, esse projeto foi de ampla importância para o desenvolvimento de desenvolvedores e profissionais na área.

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


  



