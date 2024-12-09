
Q-Learning para Super Mario World
=========

![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)


Este projeto implementa uma solução de aprendizado por reforço usando Q-Learning para treinar o Mario a jogar a fase Yoshi's Island 1 no jogo Super Mario World. Ele utiliza a biblioteca Retro para interação com o ambiente do jogo.

## 💻 Tecnologias utilizadas

* **Python:** Linguagem de programação principal.
* **Gym:** Framework para criação de ambientes de jogos para aprendizado por reforço.
* **Gym-Retro:** Extensão do Gym para interagir com jogos clássicos, como o Super Mario World.
* **NumPy:** Biblioteca para computação numérica.
* **Pyglet:** Biblioteca para criação de janelas e gráficos.


## 🔧 Como executar

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.


### Pré-requisitos

É necessário, primeiramente, ter o Pyenv instalado para poder gerenciar diferentes versões do Python. Se você ainda não tem o Pyenv, instale-o de acordo com seu sistema operacional:
- Linux/MacOS: 
    Para estes sistemas operacionais, basta seguir o passo-a-passo do projeto do pyenv encontrado no seguinte link: 
    [`pyenv`](https://github.com/pyenv/pyenv/blob/master/README.md)
- Windows: 
    Como o pyenv não é suportado no Windows, é recomendado utilizar o projeto 
    [`pyenv-win`](https://github.com/pyenv-win/pyenv-win) feito por @kirankotari.

### Instalação das Dependências

- Instale a versão do Python: Certifique-se de instalar a versão correta do Python:
```
pyenv install 3.8
pyenv shell 3.8
```
- Clone o repositório: Se você tiver acesso ao código-fonte, clone o repositório para o seu computador local:
``` 
git clone https://[seu_repositorio]/nomeProjeto.git
```
- Navegue até o diretório do projeto
- Crie e ative um ambiente virtual (opcional, mas recomendado):
```
python -m venv nomeAmbiente
source nomeAmbiente/bin/activate
```
- Instale as dependências (opcional):
```
pip install gym==0.21.0
pip install gym-retro
```


### Execução do Projeto

Caso o ambiente tenha sido corretamente configurado, basta executar o script de teste:

```
python mario_q_learning.py treinar
ou
python mario_q_learning.py jogar
```
Substitua teste.py pelo nome do seu script principal, se for diferente.

## 📋 Implementação do Q-Learning
O código implementa o algoritmo Q-learning para treinar um agente a jogar Super Mario World. A ideia central é que o agente aprende a tomar as melhores decisões (ações) em cada estado do jogo, maximizando a recompensa a longo prazo.

Pontos-chave da implementação:

- Tabela Q: A tabela Q armazena os valores esperados de cada ação em cada estado.
- Ambiente: O ambiente é simulado usando a biblioteca retro, permitindo que o agente interaja com o jogo Super Mario World.
- Ciclo de treinamento: O agente interage com o ambiente, executa ações, recebe recompensas e atualiza a tabela Q de acordo com a equação de Bellman.
- Política Epsilon-Greedy: O agente utiliza uma política epsilon-greedy para explorar o espaço de ações e explorar as melhores ações conhecidas.
- Representação de estados: O estado do jogo é representado por um vetor de características, que inclui a posição do Mario e informações sobre o ambiente ao redor.
- Verificação da posição do Mario: O código verifica se o Mario está no chão, uma condição importante para o agente de aprendizado por reforço. Ele transforma o estado do jogo em uma matriz e verifica se há um bloco sólido abaixo do Mario. Se não houver, o agente realiza ações para fazer o Mario pular e esperar até que ele toque o chão novamente. Essa parte do código é responsável por melhorar significativamente o desempenho do agente.
- Recompensa: O sistema de recompensa incentiva o agente a avançar no jogo, evitando quedas e colisões. Ele premia o agente por avançar horizontalmente e penaliza por retroceder ou morrer. Além disso, o sistema desincentiva o agente ficar parado na mesma posição horizontal, penalizando-o.

## 🔍 Resultados
Utilizando o método q-learning, encontramos alguns problemas para obter um agente eficaz, o agente consegue terminar a fase eventualmente,
mas não fomos capazes de fazer com que apóes treinado, ele sempre execute exatamente os mesmos passos. Na modelagem escolhida
ao terminar a fase, o agente voltar atribuindo uma pontuação muito alta (5000) nas escolhas feitas na tentativa bem sucedida.
Porém ao reexecutar o agente, ele eventualmente acaba tomando caminhos diferentes (mesmo com o coeficiente de exploração igualado a 0).
Acreditamos que o motivo disso seja por termos usado o state (array de 0, 1 e -1, contendo uma representação do que é exibido na tela)
e os states nem sempre se repetem exatamente igual nas jogadas, então talvez seja necessário um treinamento muito maior para acumular uma coleção de jogadas que levam o agente a concluir a fase 