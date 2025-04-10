# 📚 `models/`: Projetando Seu Sistema Tutor Inteligente (ITS)

Bem-vindo(a) à pasta **model**! 🌟 Este é o coração do seu Sistema Tutor Inteligente (ITS), onde você encontrará três arquivos YAML chave: `domain.yml`, `learner.yml` e `pedagogy.yml`. Esses arquivos trabalham juntos como uma equipe 🤝 para definir o que seu ITS ensina, como ele acompanha os alunos e como os ajuda a ter sucesso.

## 🎯 Tarefa: Projetando os modelos do ITS

Etapa 1 - Delimite o problema: 

- *Qual o problema?"* 
- *Quem é a audiência do seu sistema de tutoria inteligente?*
- *Que estratégias de tutoria poderiam entregar mais valor para esse caso?*

Etapa 2 - Defina o design da solução para o problema: 

- *Quais as entradas são necessárias para acionar a tutoria?*
- *Quais as saídas esperadas da sua tutoria? Que tipos de feedack ("O que dizer?")*
- *Quais regras de feedback ("Quando dizer?")*

> Nessa fase de **design e modelagem**, não se preocupe muito com *como o feedback será entregue*, isso será necessário subsequentemente na implementação do controller.

Etapa 3 - Construa os Modelos Iniciais do ITS

- **`domain.yml`**: O **domínio de conhecimento**, o que seu ITS ensina. Estrutura de tópicos que compõem o conhecimento necessário à tarefa.
- **`pedagogy.yml`**: A **estratégia pedagógica**, como o sistema orienta e apoia os alunos.
- **`learner.yml`**: As **variáveis do estado do aluno**, o que acompanhamos sobre cada estudante, incluindo todas as variáves necessárias nas regras definidas na estratégia pedagógica.

Etapa 4 - Próximos passos

Refine o `pedagogy.yml` e `learner.yml` com o intuito de aprimorar o valor pedagógico das mensagens do ITS para os alunos:

- **Refinar o `pedagogy.yml`**: Adicione novos tipos de feedback, refraseie as mensagens.
- **Melhorar o `learner.yml`**: Adicione todas variáveis utilizadas no seu `pedagogy.yml` em seu `learner.yml`.
