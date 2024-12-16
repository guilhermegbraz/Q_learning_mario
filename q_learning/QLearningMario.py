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
        env = retro.make(game='SuperMarioWorld-Snes', state=self.fase, players=1)
        pos_x = 0
        for episode in range(n_episodes):
            score_atual = 0
            play, escolhas = [], []
            print(f"Iniciando episódio {episode + 1}/{n_episodes}...")
            env.reset()
            self.salva_frame_play(play, env)
            ram = self.getRam(env)
            state, x, y = getState(ram, radius=radius)
            for step in range(max_steps_per_episode):
                if not q_table.estado_ja_existe(ram, step):
                    q_table.adicionar_novo_estado(ram, step, acoes)
                epsilon_ = self.get_epsilon(q_table, ram, step, epsilon)
                indice_acao = self.escolhe_acao(acoes, epsilon_, q_table, ram, step, n_actions)

                rw, info = utils.performAction(acoes[indice_acao].codigo, env)
                self.salva_frame_play(play, env)
                ram_novo_estado = self.getRam(env)
                new_state, new_x, new_y = getState(ram_novo_estado, radius=radius)
                collision = self.mario_esta_morto(ram_novo_estado)
                escolhas.append({"state": q_table.cria_chave(ram, step), "acao": indice_acao})

                if not self.mario_esta_no_chao(getState(ram_novo_estado, radius)[0], radius) and not collision:
                    info, collision = self.espera_mario_voltar_chao(env, radius, play)
                    ram_novo_estado = self.getRam(env)
                    new_state, new_x, _ = getState(ram_novo_estado, radius=radius)

                # Calcula recompensa
                reward = compute_reward(x, y, new_x, new_y, collision, info, score_atual)
                score_atual = info["score"]

                # Inicializa o novo estado na Q-Table, se necessário
                if not q_table.estado_ja_existe(ram, step + 1):
                    q_table.adicionar_novo_estado(ram, step + 1, acoes)

                valor_atualizado = q_table.retorna_acoes_estado(ram, step)[indice_acao].valor + alpha * (
                        reward + gamma * q_table.get_acao_maxima(ram_novo_estado, step + 1).valor -
                        q_table.retorna_acoes_estado(ram, step)[indice_acao].valor)
                q_table.atualiza_valor_acao_estado(ram, step, indice_acao, valor_atualizado)

                if collision:
                    break
                elif step == max_steps_per_episode - 1:
                    print(f"Episódio {episode + 1}: Mario sobreviveu ao limite de passos.")
                    env.close()
                    return pos_x, step, play
                if new_x >= 4900 or new_x == 0:
                    self.pontuar_linha_vencedora(q_table, escolhas)
                    env.close()

                    return pos_x, step, play
                ram, state, x, y = ram_novo_estado, new_state, new_x, new_y
        env.close()
        return pos_x, step, play

    def escolhe_acao(self, acoes, epsilon, q_table, ram, step, n_actions):
        if np.random.uniform(0, 1) < epsilon:
            indice_acao = np.random.randint(0, n_actions)  # Explorar
        else:
            indice_acao = acoes.index(q_table.get_acao_maxima(ram, step))
        return indice_acao

    def pontuar_linha_vencedora(self, q_table: QTableInterface, escolhas: List[dict]):
        for escolha in escolhas:
            q_table.q_table[escolha['state']][escolha['acao']].valor = 50000

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

    def mario_esta_no_chao(self, state, radius) -> bool:
        matrix = self.getStateMatrix(state, radius)
        for i in range(len(matrix)):
            if 'X' in matrix[i]:
                indice_mario = matrix[i].index("X")
                return matrix[i + 1][indice_mario] == '$$' or matrix[i + 1][indice_mario] == '@@'
        return False

    def espera_mario_voltar_chao(self, env, radius, play: list) -> (any, bool):
        rw, info = None, None
        while not self.mario_esta_no_chao(getState(self.getRam(env), radius)[0], radius):
            _, info = utils.performAction(131, env)
            self.salva_frame_play(play, env)
            _, info = utils.performAction(1, env)
            self.salva_frame_play(play, env)
            if self.mario_esta_morto(self.getRam(env)): return info, True
        return info, False

    def getRam(self, env):
        ram = []
        for k, v in env.data.memory.blocks.items():
            ram += list(v)
        return np.array(ram)

    def mario_esta_morto(self, ram) -> bool:
        return False or ram[0x71]


    def salva_frame_play(selfself, play, env):
        img = env.render(mode='rgb_array')
        play.append(img)
        env.render()

    def get_epsilon(self, q_table, ram, step, epsilon):
        if (0.0 in [a.valor for a in q_table.retorna_acoes_estado(ram, step)] or
                all(x.valor < 0.0 for x in q_table.retorna_acoes_estado(ram, step))):
            epsilon_ = epsilon
        else:
            epsilon_ = 0
        return epsilon_
