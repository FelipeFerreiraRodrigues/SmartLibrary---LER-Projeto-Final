# SmartLibrary - Documentação IEEE 29148

## 1 - Introdução

### 1.1 - Propósito

- Esse documento serve de especificação para os requisitos funcionais e não-funcionais do sistema produzido para a SmartLibrary, definindo regras de negócio, funcionalidades e etc para os requerimentos do sistema.

### 1.2 - Escopo

- O SmartLibrary se trata de um sistema CLI de gestão de biblioteca produzido para gerenciar o catálogo de livros, registrar usuários, registrar empréstimos e devoluções e etc. O sistema atende tanto ao bibliotecário (Operador) quanto ao usuário (Leitor), de forma que atenda as leis da legislação.

### 1.3 - Definições e Acrônimos

- CLI -> Command Line Interface (Interface de Linha de Comando).
- RF -> Requisito Funcional.
- RNF -> Requisito Não-Funcional.
- Operador -> Administrador responsável por registrar chegadas/saídas e gerir o sistema.
- ACID -> Atomicity, Consistency, Isolation, Durability (Atomicidade, Consistência, Isolamento e Durabilidade) | Propriedades fundamentais para transações seguras em banco de dados.

## 2 - Descrição Geral

### 2.1 - Perspectiva do Produto

- O SmartLibrary irá operar como uma plataforma que conecta bibliotecas e usuários independentes aos leitores. Exigindo armazenamento de dados seguro, capaz de lidar com acessos simultâneos e garantir privacidade de seus usuários.

### 2.2 Documentação Inicial

- https://docs.google.com/document/d/1gEkKwmalr_-uOFeyLcoOqTpf5qjKjKeiD20Wkq7_4D4/edit?usp=sharing

### 2.3 - Perfil dos Usuários

#### Operador

- Observar entrada e saída de livros, acessar dados não sensíveis de clientes, monitorar limite de livros por usuário e seus prazos.

#### Usuário Registrado

- Acessar conta, validar idade legalmente, atuar como emprestador de livros.

#### Usuário Não Registrado

- Navegar pelo catálogo livre, criar conta.

## 3 - Requisitos Específicos

### 3.1 - Regras de Negócio (RN)

- RN-001 (Prazo de Empréstimo): O prazo limite para um usuário realizar a devolução de um livro é de, no máximo, 7 dias corridos.
- RN-002 (Cálculo de Multa): Em caso de atraso (após o sétimo dia da data de empréstimo), o sistema aplicará uma multa diária de R$ 1,50 por dia de atraso.
- RN-003 (Cota de Empréstimo): Um usuário pode ter sob sua posse um limite máximo de 3 livros simultaneamente. O sistema bloqueará novas solicitações se este teto for atingido.
- RN-004 (Restrição de Faixa Etária): O empréstimo e a visualização de livros de teor "Adulto" são restritos a usuários que passaram pelo processo de validação legal de idade.

### 3.2 - Requisitos Funcionais (RF)

- RF-001 (Gestão de Cadastro e Autenticação de Usuários): O sistema deve prover uma interface segura para a criação de contas e login, armazenando os dados necessários de acesso a sua conta na biblioteca.

  *Rastreabilidade:* Nenhuma.
- RF-002 (Validação de Maioridade Legal): O sistema deve possuir uma funcionalidade de checagem de dados pessoais (conforme a legislação) para comprovar a idade do usuário, atualizando seu status de permissão no banco de dados para "Validado".

  *Rastreabilidade* RF-001.
- RF-003 (Catálogo e Pesquisa Avançada): O sistema deve exibir o acervo e permitir visualizações detalhadas por especificações (título, autor, gênero e faixa etária). O sistema deve esconder livros de classificação "Adulto" caso o usuário não possua o status validado.

  *Rastreabilidade:* RF-002, RF-003.
- RF-004 (Cadastro e Gestão de Acervo): O sistema deve permitir que usuários cadastrados insiram novos livros no catálogo informando obrigatoriamente: Título, Autor, Gênero e Faixa Etária.

  *Rastreabilidade:* RF-001
- RF-005: Controle de Transações (Empréstimos e Devoluções): O sistema deve processar as saídas de livros, definindo as datas de devolução esperadas e bloqueando o item para novos empréstimos. Também deve calcular automaticamente o valor de multa em caso de devoluções fora do prazo.

  *Rastreabilidade:* RF-001, RF-004.

- RF-006 (Painel de Monitoramento do Operador e Bloqueio): O sistema deve fornecer um painel de administrador para o operador monitorar a quantidade de livros ativos na posse de um cliente. O sistema bloqueará automaticamente novos empréstimos se o limite máximo por usuário for atingido.

  *Rastreabilidade:* RF-005.

### 3.3 - Requisitos Não-Funcionais (RNF)

- RNF-001 (Segurança e Criptografia | Privacidade): A interface de verificação e o banco de dados devem esconder dados sensíveis (ex: CPF, documentos). O Operador deve visualizar apenas os dados inofensivos e estritamente necessários para uma possível operação.

  *Categoria:* Segurança e Conformidade Legal (LGPD).
- RNF-002 (Desempenho e Concorrência): O sistema deve processar consultas e transações de maneira rápida, fluida e sem gargalos, mesmo com múltiplos acessos simultâneos.

  *Categoria:* Performance.
- RNF-003 (Confiabilidade de Banco de Dados | ACID): O sistema deve garantir as propriedades ACID em todas as transações de banco de dados. Em caso de falha de conexão ou erro no meio de um procedimento (como registro de empréstimo), o sistema deve executar um rollback, cancelando a operação para evitar inconsistências no catálogo.

  *Categoria:* Confiabilidade / Integridade de Dados.
