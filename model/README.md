# 📚 `models/`: Projetando Seu Sistema Tutor Inteligente (ITS)

Bem-vindo(a) à pasta **model**! 🌟 Este é o coração do seu Sistema Tutor Inteligente (ITS), onde você encontrará três arquivos YAML chave: `domain.yml`, `learner.yml` e `pedagogy.yml`. Esses arquivos trabalham juntos como uma equipe 🤝 para definir o que seu ITS ensina, como ele acompanha os alunos e como os ajuda a ter sucesso.

Seja construindo um ITS para preparação para exames como o ENEM, aprendizado de idiomas ou algo totalmente único, este guia mostrará como planejar esses modelos passo a passo. Vamos começar! 🚀

---

## 📖 Entendendo Cada Modelo do ITS

Esta pasta contém três arquivos YAML essenciais:

- **`domain.yml`**: O **domínio de conhecimento**, o que seu ITS ensina.
- **`learner.yml`**: O **perfil do aluno**, o que acompanhamos sobre cada estudante.
- **`pedagogy.yml`**: A **estratégia pedagógica**, como o sistema orienta e apoia os alunos.

Esses arquivos são escritos em **YAML**, um formato super simples, fácil de ler e editar.


### 1. `domain.yml` – Seu Mapa de Conhecimento 🗺️

**O Que Faz**: Este arquivo descreve os tópicos e subtópicos que seu ITS cobrirá. Pense nele como um roteiro para o aprendizado!

**Como Escrever**:
- **Organize Hierarquicamente**: Comece com tópicos gerais e divida-os em partes menores. Por exemplo, "Matemática" pode ser dividido em "Álgebra", depois "Equações" e, finalmente, "Equações Lineares".
- **Seja Específico**: Os níveis mais profundos (ex: "Resolver para X") são os conceitos que os alunos irão dominar.
- **Personalize**: Adapte-o ao seu assunto - ciência, programação, música, qualquer coisa!

> Dica Rápida: Faça um brainstorming das áreas chave do seu assunto, depois detalhe. Mantenha claro e lógico!

### 2. `learner.yml` – Acompanhando a Jornada

**O Que Faz**: Este arquivo define quais variáveis você coletará sobre cada aluno, suas respostas ou progresso, para que seu ITS possa personalizar a experiência.

**Como Escrever**: Dê a cada aluno um identificador único (ex: id: "aluno123").

**Pontos de Dados**: Acompanhe itens como respostas a perguntas, pontuações ou tempo gasto.

**Mantenha Útil**: Inclua apenas o que ajuda seu sistema a se adaptar, não complique demais!

> Dica Rápida: Comece pequeno, acompanhe apenas o suficiente para dar um bom feedback e expanda conforme necessário.

### 3. `pedagogy.yml` – O Plano de Ensino 🧑‍🏫

**O Que Faz**: Este arquivo define as regras de como seu ITS interage com os alunos, como quando dar dicas ou celebrar suas vitórias.

**Como Escrever**:
- **Defina Condições**: Use lógica simples para guiar ações, como verificar pontuações ou progresso.
- **Adicione Incentivo**: Inclua feedback positivo para aumentar a motivação.
- **Mantenha Flexível**: Crie regras que se adaptem a diferentes níveis de habilidade.

> Dica Rápida: Teste suas regras com dados fictícios para ver como funcionam, ajuste até ficarem perfeitas! 🛠️

---

## 🎯 Tarefa: Construa Seus Próprios ITS!

Pronto(a) para exercitar sua criatividade? 🧠 Aqui está um desafio: **Projete seus próprios `domain.yml`, `learner.yml` e `pedagogy.yml` para um ITS de sua escolha!**

### Como Fazer:
1.  **Escolha um Tópico**: Selecione algo interessante, como culinária, astronomia ou design de jogos.
2.  **Escreva o `domain.yml`**: Liste os tópicos principais e divida-os em subtópicos.
3.  **Elabore o `learner.yml`**: Decida quais informações do aluno acompanhar.
4.  **Crie o `pedagogy.yml`**: Adicione três regras para orientar seus alunos.

### Antes de começar

> *“O que torna seu ITS especial?”*

Pense sobre: 

- Qual é o seu objetivo? 
- Para quem é? 
- Onde e quando eles o usarão? 
- Por que é importante? 
- Como ele se ajustará aos alunos e quanto esforço será necessário para construí-lo?

---

## 🌱 Aprimore Seu ITS

Assim que seus modelos estiverem prontos, você pode:
- **Expandir o `domain.yml`**: Adicione mais tópicos.
- **Melhorar o `learner.yml`**: Acompanhe detalhes extras como confiança ou velocidade.
- **Refinar o `pedagogy.yml`**: Adicione regras mais inteligentes e personalizadas.

O design é uma jornada. Comece simples, teste e continue melhorando! 🔄

---

## 🤗 Dúvidas ou Ideias?

Precisa de ajuda? Entre em contato:
- **GitHub Issues**: Relatos de bugs ou solicitações de funcionalidades vão para [github.com/adaj/its-enem/issues](https://github.com/adaj/its-enem/issues).

