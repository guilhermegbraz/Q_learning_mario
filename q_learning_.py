import utils
import retro
from rominfo import *
import random
import re
from functools import reduce
import os
import numpy as np

radius = 6


class MarioStatus:
    def __init__(self):
        self.vidas = 4
        self.score = 0

    def check_morte(self, vidas: int):
        if vidas < self.vidas:
            return True
        self.vidas = vidas
        return False

    def update_score(self, score: int):
        self.score = score


def getRam(env):
    ram = []
    for k, v in env.data.memory.blocks.items():
        ram += list(v)
    return np.array(ram)


def carrega_q_table(max_steps_per_episode, n_actions):
    path_arquivo = "q_table.txt"
    q_table = np.zeros((max_steps_per_episode, n_actions))
    if not os.path.isfile(path_arquivo):
        return q_table
    try:
        with open(path_arquivo, 'r') as arq:
            linhas = arq.readlines()
            for linha in range(len(linhas)):
                colunas = linhas[linha].replace("\n",'').split(";")
                for coluna in range(len(colunas)):
                    q_table[linha][coluna] = float(colunas[coluna])
        return q_table
    except Exception as e:
        print("Vou criar a q-table do 0")
        print(e)
        os.remove(path_arquivo)
        return np.zeros((max_steps_per_episode, n_actions))

# Testar essa linha para tentar pegar morte: https://github.com/GuiFG/super-mario-ia
# dead = ram[0x71]

def cria_chave_estado(step, x, y) -> str:
    return f"step: {step}, posicao {x},{y}"
def qlearning():
    try:
        # Configurações do Q-Learning
        alpha = 0.1  # Taxa de aprendizado
        gamma = 0.99  # Fator de desconto
        epsilon = 0.1  # Probabilidade de explorar
        actions_list = [130, 131, 128, 1, 3, 0, 32, 3, 64, 65, 128, 128, 256]
        n_actions = len(actions_list)  # Número de ações disponíveis (exemplo: [andar, pular, voltar])
        n_episodes = 1000  # Número de episódios de treinamento
        max_steps_per_episode = 4800  # Máximo de passos por episódio
        radius = 6  # Raio de percepção do Mario
        # q_table = carrega_q_table(max_steps_per_episode, n_actions)  # Inicializa a Q-Table
        q_table = {}
        env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland1', players=1)
        for episode in range(n_episodes):
            print(f"Iniciando episódio {episode + 1}/{n_episodes}...")
            env.reset()
            mario = MarioStatus()
            ram = getRam(env)
            state, x, y = getState(ram, radius=radius)  # Obtém o estado inicial

            for step in range(max_steps_per_episode):
                estado_chave = cria_chave_estado(step, x, y)
                if estado_chave not in q_table:
                    q_table[estado_chave] = [0.0] * n_actions
                if 0.0 in q_table[estado_chave]:
                    epsilon = 0.3
                else:
                    epsilon = 0
                # Escolha de ação (política epsilon-greedy)
                if np.random.uniform(0, 1) < epsilon:
                    action = np.random.randint(0, n_actions)  # Explorar
                else:
                    # action = np.argmax(q_table[step])  # Explorar np array
                    action = np.argmax(q_table[estado_chave])  # Explorar dicionario
                # Executa ação no jogo
                rw, info = utils.performAction(actions_list[action], env)
                env.render()
                ram = getRam(env)
                new_state, new_x, new_y = getState(ram, radius=radius)

                mario.update_score(int(info["score"]))
                morte = mario.check_morte(info["lives"])
                collision = morte or ram[0x71]

                # Calcula recompensa
                reward = compute_reward(x, y, new_x, new_y, collision, info)

                # Inicializa o novo estado na Q-Table, se necessário
                nova_chave_estado = cria_chave_estado(step + 1, new_x, new_y)
                if nova_chave_estado not in q_table:
                    q_table[nova_chave_estado] = [0] * n_actions

                q_table[estado_chave][action] = q_table[estado_chave][action] + alpha * (
                        reward + gamma * np.max(q_table[nova_chave_estado]) - q_table[estado_chave][action])

                if collision:
                    # print(f"Morte detectada:")
                    # marioX, marioY, layer1x, layer1y = getXY(ram)
                    # sprites = getSprites(ram)
                    # print(f"Mario x,y: {marioX}, {marioY}\nSprites {sprites}")
                    # print(f"Q-table após iteração {step} {50 * '#'}")
                    # for value in q_table:
                    #     if reduce(lambda x, y: x + y, value) != 0:
                    #         print(value)
                    pass
                print(f"Adicionei o valor {q_table[estado_chave]} em qtable[{estado_chave}][{action}]")

                # Atualiza o estado atual
                state = new_state
                x= new_x
                y = new_y
                # Verifica término do episódio
                if collision:
                    print(f"Episódio {episode + 1}: Mario morreu em {step + 1} passos.")
                    print(f"{100 * '#'}")
                    break
                elif step == max_steps_per_episode - 1:
                    print(f"Episódio {episode + 1}: Mario sobreviveu ao limite de passos.")
                if new_x >= 5023:
                    print(f"Mario concluiu a fase com {step} iterações, após {episode} tentativas a tabela final é:")
                    map(print, q_table.values())
                    raise Exception("Final da fase")
    except Exception:
        pass
    finally:
        with open("resultados_q_table_2.txt", 'w') as f:
            for chave, valor in sorted(q_table.items(), key=lambda item: extrair_numero(item[0])):
                f.write(f"chave: {chave} : actions: {valor}\n")
    # save_q_table(q_table)

    return

# Função para extrair o número da chave
def extrair_numero(chave):
    # Encontra o primeiro número inteiro na string
    return int(re.search(r'step: \d+', chave).group())

def save_q_table(q_table):
    with open("q_table.txt", "w") as f:
        for linha in q_table:
            texto = ";".join(map(str, linha)) + "\n"
            f.writelines(texto)
            # f.writelines(texto)


def compute_reward(old_x, old_y, new_x, new_y, collision, info):
    recompensa = 0
    if collision:
        return -1000
    if new_x > old_x: recompensa += 500
    if new_x < old_x: recompensa -= 50
    if new_y > old_y: recompensa += 30
    if new_y < old_y: recompensa -= 10

    return recompensa


def initialize_q_table(action_space):
    Qtable = np.zeros((1, action_space))
    return Qtable


def epsilon_greedy_policy(Qtable, state, epsilon, n_actions):
    random_int = random.uniform(0, 1)
    if random_int > epsilon:
        action = np.argmax(Qtable[state])
    else:
        action = np.random.randint(0, n_actions)
    return action


def train(n_training_episodes, min_epsilon, max_epsilon, decay_rate, env, max_steps, Qtable):
    for episode in trange(n_training_episodes):

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
        # Reset the environment
        state = env.reset()
        step = 0
        done = False

        # repeat
        for step in range(max_steps):

            action = epsilon_greedy_policy(Qtable, state, epsilon)

            new_state, reward, done, info = env.step(action)

            Qtable[state][action] = Qtable[state][action] + learning_rate * (
                    reward + gamma * np.max(Qtable[new_state]) - Qtable[state][action])

            # If done, finish the episode
            if done:
                break

            # Our state is the new state
            state = new_state
    return Qtable


def check_collision(ram):
    """
    Verifica se o Mario colidiu com um inimigo ou caiu em um buraco.
    """
    marioX, marioY, layer1x, layer1y = getXY(ram)
    sprites = getSprites(ram)
    # Verifica colisão com sprites (inimigos e obstáculos dinâmicos)
    # print(f"Mario x,y: {marioX}, {marioY}\nSprites {sprites}")
    for sprite in sprites:
        # Checa se a posição do Mario (marioX, marioY) sobrepõe o sprite
        if abs(marioX - sprite['x']) < 12 and abs(marioY - sprite['y']) < 12:
            print("Mario colidiu")
            return True  # Colisão com inimigo ou obstáculo dinâmico

    return False  # Sem colisões


def main():
    qlearning()


if __name__ == "__main__":
    gamma = 0
    learning_rate = 0


    def trange(): return 0


    main()
