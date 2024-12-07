from q_learning.QLearningMario import QLearningMario
from q_learning.q_table.QTableDicionarioPosicaoStep import QTableDicionarioPosicaoStep
from q_learning.AcaoMario import AcaoMario
from q_learning.q_table.QTableDicionarioState import QTableDicionarioState
from q_learning.q_table.QTableInterface import QTableInterface
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from q_learning.q_table.QTableDicionarioIntervaloState import QTableDicionarioIntervaloState
import os

os.environ['TERM'] = 'xterm'


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
        return -100
    if collision and new_y < old_y: return -100
    if collision: return -100
    if new_y > 354: return 0
    if new_x > old_x: recompensa += 5 + new_x - old_x
    if new_x < old_x: recompensa += 1
    if new_x == old_x: recompensa -= 5

    return recompensa


def main():
    nome_arquivo = "q_table_dicionario_state_continuacao.txt"
    q_table = QTableDicionarioPosicaoStep()
    q_table = QTableDicionarioState()
    # q_table = QTableDicionarioIntervaloState()
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
    for i in range(5):
        acoes = [AcaoMario(descricao, codigo) for descricao, codigo in actions_map.items()]
        carrega_arquivo_q_table(nome_arquivo, q_table, actions_map)
        print(f"APOS CARREGAR A TABELA:\n{len(q_table.q_table)}")
        q = QLearningMario("YoshiIsland1")
        jogadas = 120
        maximo_x, maximo_passo, play_mais_longe, play_mais_passos = q.treinar(
            q_table, 0.7, 0.95, 0.3, jogadas, 3000, acoes, recompensa_x
        )

        print(f"Ao final, mario atingiu a posx: {maximo_x}, e o maximo de passos foram {maximo_passo}")
        cabecalho = f"Nessa tabela, após {jogadas} tentativas, mario atingiu a posição maxima: {maximo_x}, com {maximo_passo} iterações"

        salvar_q_table(q_table, nome_arquivo, cabecalho)

    return


def reproduzir_frames(frames, fps=30):
    fig, ax = plt.subplots()
    img = ax.imshow(frames[0])  # Inicializa com o primeiro frame
    ax.axis('off')  # Remove os eixos para parecer mais com o jogo

    # Atualiza os frames da animação
    def update(frame):
        img.set_data(frame)
        return [img]

    # Calcula o intervalo entre frames com base no FPS
    intervalo = int(1000 / fps)

    # Animação
    anim = FuncAnimation(fig, update, frames=frames, interval=intervalo, blit=True)
    plt.show()


def carrega_arquivo_q_table(nome_arquivo: str, q_table: QTableInterface, actions_map: dict) -> None:
    if os.path.isfile(nome_arquivo):
        with open(nome_arquivo, 'r') as f:
            registros = f.readlines()
            for registro in registros:
                try:
                    adiciona_linha(q_table, registro, actions_map)
                except:
                    print("Exceção ao tentar inserir registro na q_table")
                    pass
    return


def adiciona_linha(q_table: QTableInterface, linha_tabela, actions_map):
    chave = linha_tabela.split(": [")[0]
    valor = linha_tabela.split("[")[1]
    valor = valor.strip().replace('[', '').replace(']', '').replace(" ", "")
    acoes = valor.split('},')
    for i in range(len(acoes)):
        acoes[i] = f"{acoes[i]}}}"
    r = q_table.adiciona_elemento(chave, acoes, actions_map)
    if not r:
        print(f"Não consegui adicionar a linha {linha_tabela}")


def salvar_q_table(q_table: QTableInterface, nome_arquivo: str, cabecalho: str) -> None:
    with open(nome_arquivo, 'w') as f:
        f.write(cabecalho)
        linhas_resultado = q_table.to_string()
        f.write(linhas_resultado)


main()

