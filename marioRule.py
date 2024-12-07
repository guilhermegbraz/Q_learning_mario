#!/usr/bin/env python
# marioRule.py
# Author: Fabrício Olivetti de França
#
# Agente baseado em regras para o SMW

import sys
import retro

import numpy as np
from numpy.random import uniform, choice, random
import pickle
import os
import time
import rominfo

# from utils import *
import utils

radius = 6


def dec2bin(dec):
    binN = []
    while dec != 0:
        binN.append(dec % 2)
        dec = dec / 2
    return binN


def printState(state):
    state_n = np.reshape(state.split(','), (2 * radius + 1, 2 * radius + 1))
    _ = os.system("clear")
    mm = {'0': '  ', '1': '$$', '-1': '@@'}
    for i, l in enumerate(state_n):
        line = list(map(lambda x: mm[x], l))
        if i == radius + 1:
            line[radius] = 'X'
        print(line)


def getStateMatrix(state):
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

def esta_no_chao(state):
    matrix = getStateMatrix(state)
    for i in range(len(matrix)):
        if 'X' in matrix[i]:
            indice_mario = matrix[i].index("X")
            return matrix[i + 1][indice_mario] == '$$'
    return False


def getRam(env):
    ram = []
    for k, v in env.data.memory.blocks.items():
        ram += list(v)
    return np.array(ram)


# Função de recompensa
def compute_reward(old_x, old_y, new_x, new_y, collision, info):
    recompensa = 0
    if collision or info["lives"] == 3:
        recompensa = -1000  # Penalidade por colisão
    if new_x > old_x: recompensa += 500
    if new_x < old_x: recompensa -= 50
    if new_y > old_y: recompensa += 50
    if new_y < old_y: recompensa -= 5
    recompensa += info["score"]
    return recompensa  # Recompensa por avançar na fase

def qlearning():
    # Configurações do Q-Learning
    alpha = 0.1  # Taxa de aprendizado
    gamma = 0.99  # Fator de desconto
    epsilon = 0.1  # Probabilidade de explorar
    n_actions = 6  # Número de ações disponíveis (exemplo: [andar, pular, voltar])
    actions_list = [128, 130, 129, 64, 131, 386]
    n_episodes = 1000  # Número de episódios de treinamento
    max_steps_per_episode = 4800  # Máximo de passos por episódio
    radius = 6  # Raio de percepção do Mario
    q_table = {}  # Inicializa a Q-Table

    env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland1', players=1)
    for episode in range(n_episodes):
        print(f"Iniciando episódio {episode + 1}/{n_episodes}...")
        env.reset()
        ram = getRam(env)
        state, x, y = rominfo.getState(ram, radius=radius)  # Obtém o estado inicial
        print(state)
        for step in range(max_steps_per_episode):
            # Inicializa estado na Q-Table, se necessário
            if state not in q_table:
                q_table[state] = [0] * n_actions

            # Escolha de ação (política epsilon-greedy)
            if np.random.uniform(0, 1) < epsilon:
                action = np.random.randint(0, n_actions)  # Explorar
            else:
                action = np.argmax(q_table[state])  # Explorar

            print(f"posicao mario: ({x}, {y})")
            print(f"Mario esta no chao? : {esta_no_chao(rominfo.getState(ram, radius)[0])}")
            printState(rominfo.getState(ram, radius)[0])
            print(150 * "-")

            # Executa ação no jogo
            rw, info = utils.performAction(actions_list[action], env)
            env.render()
            ram = getRam(env)
            new_state, new_x, new_y = rominfo.getState(ram, radius=radius)
            collision = check_collision(ram)  # Verifica colisões

            # Calcula recompensa
            reward = compute_reward(x, y, new_x, new_y, collision, info)

            # Inicializa o novo estado na Q-Table, se necessário
            if new_state not in q_table:
                q_table[new_state] = [0] * n_actions

            # Atualiza a Q-Table
            q_table[state][action] += alpha * (
                    reward + gamma * max(q_table[new_state]) - q_table[state][action]
            )

            # Atualiza o estado atual
            state = new_state
            # print(f"vidas: {info['lives']}")
            # Verifica término do episódio
            if collision or info["lives"] == 3:
                print(f"Episódio {episode + 1}: Mario morreu em {step + 1} passos.")
                break
            elif step == max_steps_per_episode - 1:
                print(f"Episódio {episode + 1}: Mario sobreviveu ao limite de passos.")



def rule():
    env = retro.make(game='SuperMarioWorld-Snes', state='YoshiIsland1', players=1)
    env.reset()
    valores_vistos = set()
    total_reward = 0
    long_jump = False
    try:
        while not env.data.is_done():
            ram = getRam(env)
            try:
                print("RAM memoria morte: " + ram[7E0906])
                return
            except:
                pass
            state, x, y = rominfo.getInputs(ram)
            print(f"posicao mario: ({x}, {y})")
            print(f"Mario esta no chao? : {esta_no_chao(rominfo.getState(ram, radius)[0])}")
            printState(rominfo.getState(ram, radius)[0])
            print(150*"-")

            for i in state:
                valores_vistos.add(i)
            state_mtx = np.reshape(state, (2 * radius + 1, 2 * radius + 1))
            # ob, rew, done, info = env.step(dec2bin(128))
            # total_reward += rew
            # env.render()
            # check_collision(ram = getRam(env))
            # print(info)

            if long_jump:
                print("Pulo duplo")
                total_reward_1, _ = utils.performAction(386, env)
                total_reward_2, _ = utils.performAction(386, env)
                total_reward = total_reward_1 + total_reward_2
                long_jump = False
            else:
                if state_mtx[7, 9] == -1 or state_mtx[7, 8] == -1:
                    ob, rew, done, info = env.step(dec2bin(384))
                    total_reward += rew
                elif state_mtx[5, 11] == -1:
                    ob, rew, done, info = env.step(dec2bin(130))
                    total_reward += rew
                elif state_mtx[5, 9] == -1 or state_mtx[5, 8] == -1:
                    if state_mtx[4, 9] == -1 or state_mtx[4, 8] == -1:
                        ob, rew, done, info = env.step(dec2bin(128))
                        total_reward += rew
                    else:
                        ob, rew, done, info = env.step(dec2bin(131))
                        total_reward += rew
                        long_jump = True
                else:
                    ob, rew, done, info = env.step(dec2bin(128))
                    total_reward += rew
                env.render()
                # print(info)
            dead = ram[0x71]
            # print(dead)
            if dead:
                env.reset()

        return total_reward
    except:
        return rule()
    finally:
        print(f"Valores vistos: {valores_vistos}")


def check_collision(ram):
    """
    Verifica se o Mario colidiu com um inimigo ou caiu em um buraco.
    """
    marioX, marioY, layer1x, layer1y = rominfo.getXY(ram)
    sprites = rominfo.getSprites(ram)
    # Verifica colisão com sprites (inimigos e obstáculos dinâmicos)
    # print(f"Mario x,y: {marioX}, {marioY}\nSprites {sprites}")
    for sprite in sprites:
        # Checa se a posição do Mario (marioX, marioY) sobrepõe o sprite
        if abs(marioX - sprite['x']) < 12 and abs(marioY - sprite['y']) < 12:
            print("Mario colidiu")
            return True  # Colisão com inimigo ou obstáculo dinâmico

    return False  # Sem colisões


def main():
    r = rule()
    # qlearning()


if __name__ == "__main__":
    main()
