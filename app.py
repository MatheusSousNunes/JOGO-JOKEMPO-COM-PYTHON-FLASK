from flask import Flask, request, jsonify
import random
import uuid 

app = Flask(__name__)

# --- Persistência em Memória (Armazenamento Local) ---
# Dicionário para armazenar jogadores e seus placares
# Estrutura: {player_id: {"name": str, "wins": int, "losses": int, "draws": int}}
PLAYERS = {} 

# Lista para armazenar o histórico de jogadas
# Estrutura: [{"player_id": str, "player_move": str, "cpu_move": str, "result": str}, ...]
GAME_HISTORY = []

# Opções válidas para Jokenpô
MOVES = ["PEDRA", "PAPEL", "TESOURA"]

def generate_player_id():
    """Gera um ID único para o jogador."""
    return str(uuid.uuid4())

def get_cpu_move():
    """Retorna uma jogada aleatória para a CPU."""
    return random.choice(MOVES)

def determine_winner(player_move, cpu_move):
    """Determina o resultado da jogada (WIN, LOSE, DRAW)."""
    if player_move == cpu_move:
        return "DRAW", f"{player_move} contra {cpu_move}. Empate!" #cite: 118
    elif (
        (player_move == "PEDRA" and cpu_move == "TESOURA") or #cite: 114
        (player_move == "TESOURA" and cpu_move == "PAPEL") or #cite: 116
        (player_move == "PAPEL" and cpu_move == "PEDRA")      #cite: 117
    ):
        return "WIN", f"{player_move} vence {cpu_move}. Você venceu!"
    else:
        return "LOSE", f"{cpu_move} vence {player_move}. Você perdeu."

# --- ENDPOINT 1: POST /players (Cria um jogador) ---
@app.route('/players', methods=['POST'])
def create_player():
    data = request.get_json()
    player_name = data.get('name')

    if not player_name:
        return jsonify({"error": "O nome do jogador é obrigatório.", "code": 400}), 400

    player_id = generate_player_id()
    PLAYERS[player_id] = {
        "name": player_name,
        "wins": 0, "losses": 0, "draws": 0
    }

    response = {"player_id": player_id, "name": player_name} #cite: 54, 55
    return jsonify(response), 201

# --- ENDPOINT 2: POST /jokenpo/play (Realiza uma jogada) ---
@app.route('/jokenpo/play', methods=['POST'])
def play_jokenpo():
    data = request.get_json()
    player_id = data.get('player_id')
    player_move = data.get('move', '').upper()

    # Tratamento de Erros
    if player_id not in PLAYERS:
        # 404 - jogador não encontrado
        return jsonify({"error": "Jogador não encontrado.", "code": 404}), 404 
    
    if player_move not in MOVES:
        # 400 - jogada inválida (diferente de pedra/papel/tesoura)
        return jsonify({"error": f"Jogada inválida. Escolha entre: {', '.join(MOVES)}", "code": 400}), 400

    # Lógica do Jogo
    cpu_move = get_cpu_move()
    result, message = determine_winner(player_move, cpu_move)

    # Atualiza o Placar
    if result == "WIN":
        PLAYERS[player_id]['wins'] += 1
    elif result == "LOSE":
        PLAYERS[player_id]['losses'] += 1
    else:
        PLAYERS[player_id]['draws'] += 1

    # Registra no Histórico
    play_record = {
        "player_id": player_id, "player_move": player_move, 
        "cpu_move": cpu_move, "result": result
    }
    GAME_HISTORY.append(play_record)
    
    response = {
        "player_id": player_id,
        "player_move": player_move, #cite: 142
        "cpu_move": cpu_move,       #cite: 143
        "result": result,           #cite: 147
        "message": message          #cite: 148
    }
    return jsonify(response), 200

# --- ENDPOINT 3: GET /jokenpo/history/{player_id} (Histórico por jogador) ---
@app.route('/jokenpo/history/<string:player_id>', methods=['GET'])
def get_player_history(player_id):
    if player_id not in PLAYERS:
        return jsonify({"error": "Jogador não encontrado.", "code": 404}), 404

    # Filtra as jogadas feitas por este jogador
    player_history = [
        game for game in GAME_HISTORY if game['player_id'] == player_id
    ]

    response = {
        "player_id": player_id,
        "name": PLAYERS[player_id]['name'],
        "history": player_history
    }
    # Retorna as jogadas realizadas pelo jogador, incluindo resultado
    return jsonify(response), 200

# --- ENDPOINT 4: GET /jokenpo/scoreboard (Placar geral) ---
@app.route('/jokenpo/scoreboard', methods=['GET'])
def get_scoreboard():
    scoreboard = []
    
    for player_id, data in PLAYERS.items():
        scoreboard.append({
            "player_id": player_id,
            "name": data['name'],
            "wins": data['wins'],
            "losses": data['losses'],
            "draws": data['draws'],
            "total_games": data['wins'] + data['losses'] + data['draws']
        })

    # Mostra o placar resumido (Vitórias, Derrotas e Empates) por jogador
    scoreboard.sort(key=lambda x: x['wins'], reverse=True)
    
    response = {"scoreboard": scoreboard}
    return jsonify(response), 200


# --- Ponto de Entrada para Execução ---
#if __name__ == '__main__':
    # Configuração para rodar na porta 5000 com modo de depuração ativado
    #app.run(debug=True, host='0.0.0.0', port=5000)