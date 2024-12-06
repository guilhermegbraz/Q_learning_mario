from q_learning.QLearningMario import QLearningMario
from q_learning.q_table.QTableDicionarioPosicaoStep import QTableDicionarioPosicaoStep
from q_learning.AcaoMario import AcaoMario
from q_learning.q_table.QTableDicionarioState import QTableDicionarioState

import os
os.environ['TERM'] = 'xterm'

q_table = QTableDicionarioPosicaoStep()
q_table = QTableDicionarioState()
actions_map = {
    'runright': 130,
    'runjumpright': 131,
    # 'right': 128,
    # 'down': 32,
    # 'jump': 1,
    'left': 64,
    # 'jumpright': 129,
    # 'spin': 256,
    'spinright': 384
}

def compute_reward(old_x, old_y, new_x, new_y, collision, info):
    recompensa = 0
    if collision:
        return -100
    if new_x > old_x: recompensa += 500
    if new_x < old_x: recompensa -= 5
    if new_y > old_y: recompensa += 30
    if new_y < old_y: recompensa -= 10
    if new_x == old_x: recompensa -= 500

    return recompensa


def recompensa_x(old_x, old_y, new_x, new_y, collision, info) -> int:
    recompensa = 0
    if collision and new_y > old_y:
        return 0
    if collision and new_y < old_y: return -100
    if collision: return -100
    if new_y > 354: return 0
    if new_x > old_x: recompensa += 5 + new_x - old_x
    if new_x < old_x: recompensa -= (1 + old_x - new_x)
    if new_x == old_x: recompensa -= 5

    return recompensa

acoes = [AcaoMario(descricao, codigo) for descricao, codigo in actions_map.items()]
q = QLearningMario("YoshiIsland1")
maximo_x, maximo_passo = q.treinar(
    q_table, 0.7, 0.95, 0.3, 250, 3000, acoes, recompensa_x
)

print(f"Ao final, mario atingiu a posx: {maximo_x}, e o maximo de passos foram {maximo_passo}")

with open("q_table_dicionario_state.txt", 'w') as f:
    linhas_resultado = q_table.to_string()
    f.write(linhas_resultado)
