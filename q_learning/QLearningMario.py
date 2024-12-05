import retro
import os

from q_learning.q_table.QTableInterface import QTableInterface
from typing import List
from q_learning.AcaoMario import AcaoMario
from rominfo import *
import utils


class QLearningMario:
    def __init__(self, fase: str):
        self.fase = fase
        pass

    def treinar(self, q_table: QTableInterface, alpha: float, gamma: float, epsilon: float, n_episodes: int,
                max_steps_per_episode: int, acoes: List[AcaoMario], compute_reward):
        radius = 6
        n_actions = len(acoes)
        # env = retro.make(game='SuperMarioWorld-Snes', state=self.fase, players=1)
        env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland1', players=1)
        for episode in range(n_episodes):
            print(f"Iniciando episódio {episode + 1}/{n_episodes}...")
            env.reset()
            ram = self.getRam(env)
            state, x, y = getState(ram, radius=radius)
            print(state)
            for step in range(max_steps_per_episode):

                if not q_table.estado_ja_existe(ram, step):
                    q_table.adicionar_novo_estado(ram, step, acoes)

                if 0.0 in [a.valor for a in q_table.retorna_acoes_estado(ram, step)]:
                    epsilon = 0.3
                else:
                    epsilon = 0

                # Escolha de ação (política epsilon-greedy)
                if np.random.uniform(0, 1) < epsilon:
                    indice_acao = np.random.randint(0, n_actions)  # Explorar
                else:
                    indice_acao = acoes.index(q_table.get_acao_maxima(ram, step))

                print(f"posicao mario: ({x}, {y})")
                print(f"Mario esta no chao? : {self.esta_no_chao(getState(ram, radius)[0], radius)}")
                self.printState(getState(ram, radius)[0], radius)
                print(150 * "-")
                # Executa ação no jogo
                rw, info = utils.performAction(acoes[indice_acao].codigo, env)
                env.render()
                ram_novo_estado = self.getRam(env)
                new_state, new_x, new_y = getState(ram_novo_estado, radius=radius)
                collision = False or ram_novo_estado[0x71]

                # Calcula recompensa
                reward = compute_reward(x, y, new_x, new_y, collision, info)

                # Inicializa o novo estado na Q-Table, se necessário
                if not q_table.estado_ja_existe(ram, step + 1):
                    q_table.adicionar_novo_estado(ram, step + 1, acoes)

                valor_atualizado = q_table.retorna_acoes_estado(ram, step)[indice_acao].valor + alpha * (
                        reward + gamma * q_table.get_acao_maxima(ram_novo_estado, step + 1).valor -
                        q_table.retorna_acoes_estado(ram, step)[indice_acao].valor)

                q_table.atualiza_valor_acao_estado(ram, step, indice_acao, valor_atualizado)

                # print( f"Adicionei o valor {q_table.retorna_acoes_estado(ram, step)} em qtable[{step}][{q_table.cria_chave(ram, step)}]")

                ram, state, x, y = ram_novo_estado, new_state, new_x, new_y
                # Verifica término do episódio
                if collision:
                    print(f"Episódio {episode + 1}: Mario morreu em {step + 1} passos.")
                    print(f"{100 * '#'}")
                    break
                elif step == max_steps_per_episode - 1:
                    print(f"Episódio {episode + 1}: Mario sobreviveu ao limite de passos.")
                    return
                if new_x >= 5014 or new_x == 0:
                    print(
                        f"Mario concluiu a fase com {step} iterações, após {episode} tentativas. posX é {new_x}; A tabela final é:")
                    env.close()
                    return

    def getStateMatrix(self, state, radius):
        state_n = np.reshape(state.split(','), (2 * radius + 1, 2 * radius + 1))
        _ = os.system("clear")
        mm = {'0': '  ', '1': '$$', '-1': '@@'}
        matrix = []
        for i, l in enumerate(state_n):
            line = list(map(lambda x: mm[x], l))
            if i == radius + 1:
                line[radius] = 'X'
            matrix.append(line)
        return matrix

    def printState(self, state, radius):
        state_n = np.reshape(state.split(','), (2 * radius + 1, 2 * radius + 1))
        _ = os.system("clear")
        mm = {'0': '  ', '1': '$$', '-1': '@@'}
        for i, l in enumerate(state_n):
            line = list(map(lambda x: mm[x], l))
            if i == radius + 1:
                line[radius] = 'X'
            print(line)

    def esta_no_chao(self, state, radius):
        matrix = self.getStateMatrix(state, radius)
        for i in range(len(matrix)):
            if 'X' in matrix[i]:
                indice_mario = matrix[i].index("X")
                return matrix[i + 1][indice_mario] == '$$'
        return False

    def getRam(self, env):
        ram = []
        for k, v in env.data.memory.blocks.items():
            ram += list(v)
        return np.array(ram)