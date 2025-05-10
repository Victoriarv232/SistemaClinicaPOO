# Projeto: Sistema de Fila Clínica
Nesse projeto, você encontrará um sistema de gerenciamento de fila numa Clínica, desenvolvido com Python e Flask.
(Com geração de senhas a depender da especialidade procurada, e fluxo baseado na simulação de 2 guichês operando atendimento).

## Funcionalidades

- Geração de senhas por tipo de atendimento;
- Fila com prioridade para Preferenciais;
- Limite de senhas por consultório;
- Remoção automática da senha da fila após o atendimento;
- Armazenamento das senhas em banco de dados (Para exibição das mesmas, informando visualmente quais e quantas senhas estão na fila);
- Mecanismo de resetar as senhas (Pensado para quando um novo dia de atendimento se iniciar, havendo a necessidade de recomeçar a contagem de senhas).
- Interface web com navegação entre páginas:
  - Página 1: Gerar senhas / Ir para o Painel / Resetar senhas;
  - Página 2: Painel com senhas em atendimento e em espera / Chamar senhas / Voltar para Gerar Senhas.
    
## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- HTML / CSS (e Bootstrap)
