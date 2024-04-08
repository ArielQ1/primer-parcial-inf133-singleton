from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class Player:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.games = {}
        return cls._instance
 
    def to_dict(self):
        games_dict = {}
        for game_id, game_data in self.games.items():
            games_dict[str(game_id)] = {
                'player': game_data['player'],
                'number': game_data['number'],
                'attempts': game_data['attempts'],
                'status': game_data['status']
            }
        return games_dict
    
    def buscar_nombre(self, nombre):
        for game in self.games:
            if game == nombre:
                return game
        return None
    
    def create_game(self, player):
        game_id = len(self.games) + 1
        number_to_guess = random.randint(1, 100)
        game_data = {
            'player': player,
            'number': number_to_guess,
            'attempts': [],
            'status': 'En progreso'
        }
        self.games[game_id] = game_data
        return game_data

    def enviar_numero(self, data):
        Player.verificar_resultado(data, 1)
        self.games[1]["attemps"].append(data) 
        
    def verificar_resultado(self, numero_introducido, game_id):
        numero_revisar = self.games[1]["number"]
        if numero_introducido > numero_revisar :
            print("El numero a adivinar es menor")
        elif numero_introducido < numero_revisar:
            print("El numero a adivinar es menor")
        else:
            print("!Felicidades has adivinado!")
            
    def eliminar_game(self, id_game):
        if id_game in self.games:
            self.games.pop(id_game)
            return {"message": "partida eliminada"}
        return None
            
    
game_instance = Player()

class PlayerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/guess":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            player_data = json.dumps(player.to_dict())
            self.wfile.write(player_data.encode("utf-8"))
            
        elif self.path.startswith("/guess") and "player":
            nombre = self.path.split("/")[-1]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            player_data = json.dumps(player.buscar_nombre(nombre))
            self.wfile.write(player_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            
    def do_POST(self):
        if self.path == "/guess":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            player_name = data.get('player')
            if not player_name:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'nombre de jugador requerido'}).encode("utf-8"))
                return

            game_data = game_instance.create_game(player_name)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        if self.path == "/guess/1":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))
            game_data = game_instance.enviar_numero(data)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith("/guess/"):
            id = int(self.path.split("/")[-1])
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            player_data = json.dumps(player.eliminar_game(id))
            self.wfile.write(player_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global player
    player = Player()

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PlayerHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()