# JOGO-JOKEMPO-COM-PYTHON-FLASK

Atividade Final - Jogo de Jokenpô 
(Pedra, Papel, Tesoura) via API


1. Informações do Projeto 

Opção Escolhida: Jogo de Jokenpô (Pedra, Papel, Tesoura) contra a CPU.
Tecnologias e Framework: Python com o framework Flask.
Persistência de Dados: Em memória (dicionários e listas Python), conforme permitido pelo requisito de armazenamento local

2.. Instruções de Como Rodar 

A aplicação deve ser testada via chamadas de API (Postman, Insomnia ou cURL)

Pré-requisitos

Python 3.x instalado.

Passos de Execução

Crie e Ative o Ambiente Virtual (venv):

python -m venv venv
# Para Windows (PowerShell):
venv\Scripts\activate
# Para Linux/macOS:
source venv/bin/activate

Instale o Flask:

(venv) pip install Flask

Defina a Aplicação e Execute o Servidor:

# Define o arquivo principal
$env:FLASK_APP = "app.py" 
# Inicia o servidor de desenvolvimento
(venv) flask run

A API estará rodando e pronta para ser testada em http://127.0.0.1:5000/.

3. Exemplos de Requisições (Endpoints) 

Todas as respostas são em formato JSON6. Use a URL base http://127.0.0.1:5000/.

A. Criar Jogador (POST /players) 

Método -  POST
URL -  /players

Body (JSON)

JSON{
    "name": "Maria"
}

Exemplo de Resposta (201 Created)

JSON{
    "player_id": "a1b2c3d4-e5f6-...",
    "name": "Maria"
}

B. Realizar Jogada (POST /jokenpo/play) 

Método - POST
URL -  /jokenpo/play

Body (JSON)

JSON{
    "player_id": "ID_DO_JOGADOR",
    "move": "PEDRA" /* Opções: PEDRA, PAPEL, TESOURA */
}

Exemplo de Resposta (200 OK) 

JSON{
    "player_id": "ID_DO_JOGADOR",
    "player_move": "PEDRA",        /* Jogada do jogador [cite: 142]*/
    "cpu_move": "TESOURA",       /* Jogada da CPU [cite: 143]*/
    "result": "WIN",             /* Resultado (WIN, LOSE, DRAW) [cite: 147]*/
    "message": "PEDRA quebra TESOURA. Você venceu!" [cite: 148]
}

C. Histórico do Jogador (GET /jokenpo/history/{player_id}) 

Lista as jogadas já realizadas pelo jogador

Método-  GET
URL -  /jokenpo/history/{player_id}

Exemplo de Resposta (200 OK - Parcial)

JSON{
    "player_id": "ID_DO_JOGADOR",
    "history": [
        {
            "player_move": "PAPEL",
            "cpu_move": "PEDRA",
            "result": "WIN"
        }
    ]
}

D. Placar Geral (GET /jokenpo/scoreboard) 

Mostra o placar resumido de Vitórias, Derrotas e Empates por jogador.

Método  - GET
URL  - /jokenpo/scoreboard

Exemplo de Resposta (200 OK - Parcial)

JSON{
    "scoreboard": [
        {
            "name": "Seu Nome",
            "wins": 5,
            "losses": 3,
            "draws": 2,
            "total_games": 10
        }
    ]
}

