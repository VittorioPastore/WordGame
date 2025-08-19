#!/usr/bin/env python3
"""
Multiplayer Impostor Word Game Server
Handles WebSocket connections, room management, and game state
"""

import asyncio
import websockets
import json
import random
import string
import time
import threading
from typing import Dict, Set, Optional, List
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
try:
    import netifaces
    NETIFACES_AVAILABLE = True
except ImportError:
    NETIFACES_AVAILABLE = False
    print("Warning: netifaces not available, using fallback IP detection")
import uuid

class GameRoom:
    def __init__(self, room_code: str, host_player):
        self.room_code = room_code
        self.host_player = host_player
        self.players = {}  # Host is not a player, so start with empty players dict
        self.game_state = "lobby"  # lobby, playing, results
        self.secret_word = ""
        self.impostor_id = ""
        self.concepts = [
                # --- Original Seeds ---
                "Pizza", "Hamburger", "Sushi", "Tacos", "Pasta", "Sandwich", "Coffee",
                "Ice Cream", "Chocolate", "Apple", "Dog", "Cat", "Lion", "Tiger",
                "Elephant", "Butterfly", "Fish", "Bird", "Horse", "Rabbit", "Ocean",
                "Mountain", "River", "Forest", "Beach", "Sunset", "Rainbow", "Star",
                "Moon", "Tree", "Car", "Airplane", "Bicycle", "Train", "Boat",
                "Rocket", "Bus", "Motorcycle", "Helicopter", "Ship", "Phone",
                "Computer", "Television", "Camera", "Clock", "Book", "Music",
                "Movie", "Game", "Ball", "Happy", "Excited", "Calm", "Surprised",
                "Grateful", "Curious", "Brave", "Creative", "Friendly", "Peaceful",

                # --- Food & Drinks ---
                "Steak", "Fries", "Donut", "Pancake", "Waffle", "Croissant", "Bagel", "Hot Dog",
                "Cereal", "Milkshake", "Smoothie", "Orange", "Banana", "Strawberry", "Blueberry", "Pineapple",
                "Watermelon", "Mango", "Avocado", "Guacamole", "Nachos", "Popcorn", "Cake", "Cookie",
                "Brownie", "Cheesecake", "Lasagna", "Ramen", "Curry", "Fried Rice", "Spring Roll", "Dumpling",
                "Falafel", "Shawarma", "Hummus", "Paella", "Burrito", "Quesadilla", "Chili", "Soup",
                "Salad", "Cheese", "Wine", "Beer", "Tea", "Espresso", "Latte", "Hot Chocolate",

                # --- Animals ---
                "Wolf", "Bear", "Giraffe", "Zebra", "Kangaroo", "Koala", "Panda", "Penguin",
                "Seal", "Shark", "Whale", "Octopus", "Jellyfish", "Turtle", "Crocodile", "Alligator",
                "Eagle", "Owl", "Falcon", "Parrot", "Peacock", "Chicken", "Cow", "Pig",
                "Sheep", "Goat", "Duck", "Goose", "Frog", "Snake", "Lizard", "Chameleon",
                "Spider", "Ant", "Bee", "Wasp", "Dragonfly", "Ladybug", "Crab", "Lobster",

                # --- Places & Landmarks ---
                "Eiffel Tower", "Big Ben", "Statue of Liberty", "Colosseum", "Great Wall", "Pyramids", "Taj Mahal", "Machu Picchu",
                "Mount Everest", "Grand Canyon", "Niagara Falls", "Sahara Desert", "Amazon Rainforest", "Antarctica", "North Pole", "South Pole",
                "London", "Paris", "Rome", "New York", "Tokyo", "Beijing", "Sydney", "Rio de Janeiro",
                "Los Angeles", "Chicago", "Berlin", "Dubai", "Las Vegas", "Hawaii", "Alaska", "Iceland",

                # --- Professions ---
                "Doctor", "Nurse", "Teacher", "Scientist", "Engineer", "Pilot", "Chef", "Artist",
                "Musician", "Singer", "Actor", "Writer", "Farmer", "Athlete", "Dancer", "Astronaut",
                "Firefighter", "Police Officer", "Soldier", "Politician", "Lawyer", "Judge", "Programmer", "Designer",
                "Photographer", "Journalist", "Mechanic", "Electrician", "Plumber", "Architect", "Student", "Professor",

                # --- Everyday Objects ---
                "Table", "Chair", "Bed", "Sofa", "Lamp", "Bottle", "Glass", "Plate",
                "Fork", "Spoon", "Knife", "Pen", "Pencil", "Paper", "Notebook", "Backpack",
                "Shoes", "Shirt", "Jacket", "Hat", "Gloves", "Scarf", "Sunglasses", "Wallet",
                "Keys", "Door", "Window", "Mirror", "Toothbrush", "Soap", "Towel", "Shampoo",
                "Guitar", "Drum", "Piano", "Violin", "Trumpet", "Flute", "Microphone", "Headphones",

                # --- Fantasy & Fun ---
                "Dragon", "Unicorn", "Mermaid", "Fairy", "Wizard", "Witch", "Vampire", "Zombie",
                "Ghost", "Alien", "Robot", "Monster", "Superhero", "Knight", "Princess", "King",
                "Queen", "Castle", "Treasure", "Pirate", "Spaceship", "Magic Wand", "Crystal Ball", "Time Machine",

                # --- Emotions & Concepts ---
                "Love", "Hate", "Joy", "Sadness", "Fear", "Anger", "Hope", "Dream",
                "Luck", "Wisdom", "Knowledge", "Faith", "Trust", "Patience", "Honesty", "Loyalty",
                "Kindness", "Confidence", "Determination", "Ambition", "Freedom", "Justice", "Equality", "Peace",

                # --- Sports ---
                "Soccer", "Basketball", "Baseball", "Tennis", "Volleyball", "Golf", "Hockey", "Cricket",
                "Rugby", "Boxing", "Martial Arts", "Skateboard", "Snowboard", "Skiing", "Surfing", "Swimming",
                "Running", "Cycling", "Gymnastics", "Bowling", "Wrestling", "Climbing", "Archery", "Fencing",

                # --- Technology ---
                "Smartphone", "Laptop", "Tablet", "Smartwatch", "Drone", "VR Headset", "Game Console", "Keyboard",
                "Mouse", "Printer", "Speaker", "Calculator", "Charger", "Battery", "Lightbulb", "Remote Control",

                # --- Nature & Weather ---
                "Snow", "Rain", "Thunder", "Lightning", "Storm", "Cloud", "Wind", "Fire",
                "Volcano", "Earthquake", "Tornado", "Hurricane", "Desert", "Cave", "Island", "Glacier",

                # --- Events & Locations ---
                "Festival", "Carnival", "Concert", "Circus", "Parade", "Market", "School", "Hospital",
                "Library", "Museum", "Zoo", "Aquarium", "Park", "Playground", "Restaurant", "Hotel",
                "Bridge", "Tower", "Tunnel", "Road", "Highway", "Airport", "Harbor", "Train Station",

                # --- Expansion: Countries & Cities ---
                "Italy", "Spain", "Germany", "Canada", "Mexico", "Brazil", "Argentina", "India",
                "China", "Japan", "South Korea", "Egypt", "South Africa", "Kenya", "Australia", "New Zealand",
                "Iraq", "Turkey", "Sweden", "Norway", "Finland", "Denmark", "Netherlands", "Belgium",
                "Switzerland", "Austria", "Greece", "Portugal", "Poland", "Russia", "Ukraine", "Thailand",

                # --- Expansion: Famous People (fictional & real) ---
                "Einstein", "Newton", "Da Vinci", "Shakespeare", "Cleopatra", "Caesar", "Napoleon", "Alexander the Great",
                "Gandhi", "Mandela", "Martin Luther King", "Lincoln", "Washington", "Churchill", "Queen Elizabeth", "Elon Musk",
                "Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Taylor Swift", "Beyonce", "Michael Jackson", "Elvis", "Madonna",
                "Batman", "Superman", "Spiderman", "Iron Man", "Thor", "Hulk", "Captain America", "Wonder Woman"
        ]
        self.players_ready = set()
        
    def add_player(self, player):
        self.players[player.player_id] = player
        
    def remove_player(self, player_id: str):
        if player_id in self.players:
            del self.players[player_id]
            self.players_ready.discard(player_id)
            
    def get_player_list(self):
        return [
            {
                "id": p.player_id,
                "name": p.name,
                "isHost": False,  # Players are never hosts since host is separate
                "connected": p.connected,
                "ready": p.player_id in self.players_ready
            }
            for p in self.players.values()
        ]
        
    def start_game(self):
        if len(self.players) < 3:
            return False
            
        self.game_state = "playing"
        self.secret_word = random.choice(self.concepts)
        impostor_player = random.choice(list(self.players.values()))
        self.impostor_id = impostor_player.player_id
        self.players_ready.clear()
        return True
        
    def all_players_ready(self):
        return len(self.players_ready) == len(self.players)
        
    def mark_player_ready(self, player_id: str):
        self.players_ready.add(player_id)

class Player:
    def __init__(self, websocket, player_id: str, name: str):
        self.websocket = websocket
        self.player_id = player_id
        self.name = name
        self.room_code = None
        self.connected = True
        self.last_seen = time.time()
        
    def update_connection(self, websocket):
        """Update websocket connection for reconnecting player"""
        self.websocket = websocket
        self.connected = True
        self.last_seen = time.time()

class GameServer:
    def __init__(self):
        self.rooms: Dict[str, GameRoom] = {}
        self.players: Dict[str, Player] = {}
        self.websocket_to_player: Dict[websockets.WebSocketServerProtocol, Player] = {}
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        
        # Simple game state for single room mode
        self.game_state = "lobby"
        self.room_code = self.generate_room_code()
        self.current_players: List[Player] = []
        
    def generate_room_code(self) -> str:
        """Generate a unique 4-character room code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            if code not in self.rooms:
                return code
                
    def create_room(self, player: Player) -> str:
        """Create a new room with the player as host"""
        room_code = self.generate_room_code()
        room = GameRoom(room_code, player)
        self.rooms[room_code] = room
        player.room_code = room_code
        return room_code
        
    def join_room(self, player: Player, room_code: str) -> bool:
        """Add player to existing room"""
        print(f"🔍 Available rooms: {list(self.rooms.keys())}")
        
        if room_code not in self.rooms:
            print(f"❌ Room {room_code} not found")
            return False
            
        room = self.rooms[room_code]
        if room.game_state != "lobby":
            print(f"❌ Room {room_code} is not in lobby state (current: {room.game_state})")
            return False
            
        room.add_player(player)
        player.room_code = room_code
        print(f"✅ Player '{player.name}' added to room {room_code}")
        return True
        
    def leave_room(self, player: Player):
        """Remove player from their room"""
        if not player.room_code or player.room_code not in self.rooms:
            return
            
        room = self.rooms[player.room_code]
        room.remove_player(player.player_id)
        
        # If room is empty, delete room (host leaving doesn't delete room since they're separate)
        if not room.players:
            del self.rooms[player.room_code]
        
        player.room_code = None
        
    async def broadcast_to_room(self, room_code: str, message: dict, exclude_player: Optional[str] = None):
        """Send message to all players in a room"""
        if room_code not in self.rooms:
            return
            
        room = self.rooms[room_code]
        disconnected_players = []
        
        # Send to all players in the room
        for player in room.players.values():
            if exclude_player and player.player_id == exclude_player:
                continue
                
            try:
                await player.websocket.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                disconnected_players.append(player.player_id)
        
        # Also send to the host (who is not in the players list)
        if room.host_player and room.host_player.websocket:
            if not exclude_player or room.host_player.player_id != exclude_player:
                try:
                    await room.host_player.websocket.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    # Host disconnected - this is more serious, might want to handle differently
                    pass
                
        # Clean up disconnected players
        for player_id in disconnected_players:
            room.remove_player(player_id)
            if player_id in self.players:
                del self.players[player_id]
                
    async def handle_message(self, websocket, message_data: dict):
        """Handle incoming WebSocket message"""
        player = self.websocket_to_player.get(websocket)
        message_type = message_data.get("type")
        
        try:
            if message_type == "join_server":
                # Player connecting with name
                player_id = message_data.get("playerId")  # Allow reconnection with existing ID
                name = message_data.get("name", f"Player{len(self.players)+1}")[:15]
                
                # Check if this is a reconnection
                if player_id and player_id in self.players:
                    # Reconnecting player
                    player = self.players[player_id]
                    player.update_connection(websocket)
                    self.websocket_to_player[websocket] = player
                    
                    print(f"🔄 Player '{name}' reconnected with ID: {player_id}")
                    
                    await websocket.send(json.dumps({
                        "type": "reconnection_established",
                        "playerId": player_id,
                        "name": name,
                        "roomCode": player.room_code if player.room_code else None
                    }))
                    
                    # Notify room if player was in one
                    if player.room_code and player.room_code in self.rooms:
                        await self.broadcast_to_room(player.room_code, {
                            "type": "player_reconnected",
                            "players": self.rooms[player.room_code].get_player_list()
                        })
                else:
                    # New player
                    if not player_id:
                        player_id = str(uuid.uuid4())
                    
                    player = Player(websocket, player_id, name)
                    self.players[player_id] = player
                    self.websocket_to_player[websocket] = player
                    
                    print(f"👤 Player '{name}' joined server with ID: {player_id}")
                    
                    await websocket.send(json.dumps({
                        "type": "connection_established",
                        "playerId": player_id,
                        "name": name
                    }))
                
            elif message_type == "create_room":
                if not player:
                    return
                    
                room_code = self.create_room(player)
                room = self.rooms[room_code]
                
                print(f"🏠 Room created: {room_code} by host '{player.name}'")
                
                await websocket.send(json.dumps({
                    "type": "room_created",
                    "roomCode": room_code,
                    "players": room.get_player_list(),
                    "isHost": True  # Mark this connection as the host
                }))
                
            elif message_type == "join_room":
                if not player:
                    print("❌ Join room failed: No player found")
                    return
                    
                room_code = message_data.get("roomCode", "").upper()
                print(f"🚪 Player '{player.name}' trying to join room: {room_code}")
                success = self.join_room(player, room_code)
                
                if success:
                    room = self.rooms[room_code]
                    print(f"✅ Player '{player.name}' successfully joined room {room_code}")
                    print(f"📊 Room {room_code} now has {len(room.players)} players")
                    
                    # Notify all players in room
                    await self.broadcast_to_room(room_code, {
                        "type": "player_joined",
                        "players": room.get_player_list()
                    })
                    
                    await websocket.send(json.dumps({
                        "type": "room_joined",
                        "roomCode": room_code,
                        "players": room.get_player_list(),
                        "isHost": False  # Mark this connection as not the host
                    }))
                else:
                    print(f"❌ Player '{player.name}' failed to join room {room_code}")
                    await websocket.send(json.dumps({
                        "type": "join_failed",
                        "error": "Room not found or game in progress"
                    }))
                    
            elif message_type == "start_game":
                if not player or not player.room_code:
                    return
                    
                room = self.rooms[player.room_code]
                if player.player_id != room.host_player.player_id:
                    return
                    
                if room.start_game():
                    await self.broadcast_to_room(player.room_code, {
                        "type": "game_started",
                        "gameState": {
                            "phase": "playing",
                            "playerCount": len(room.players)
                        }
                    })
                    
            elif message_type == "get_role":
                if not player or not player.room_code:
                    return
                    
                room = self.rooms[player.room_code]
                if room.game_state != "playing":
                    return
                
                # Host doesn't get a role since they're not playing
                if player.player_id == room.host_player.player_id:
                    await websocket.send(json.dumps({
                        "type": "host_status",
                        "message": "You are the host - monitor the game!"
                    }))
                    return
                    
                is_impostor = player.player_id == room.impostor_id
                
                await websocket.send(json.dumps({
                    "type": "role_assigned",
                    "isImpostor": is_impostor,
                    "secretWord": "" if is_impostor else room.secret_word,
                    "playerName": player.name
                }))
                
            elif message_type == "role_revealed":
                if not player or not player.room_code:
                    return
                    
                room = self.rooms[player.room_code]
                # Only count role reveals from actual players, not the host
                if player.player_id != room.host_player.player_id:
                    room.mark_player_ready(player.player_id)
                
                await self.broadcast_to_room(player.room_code, {
                    "type": "role_reveal_status",
                    "readyCount": len(room.players_ready),
                    "totalCount": len(room.players),
                    "allReady": room.all_players_ready()
                })
                
            elif message_type == "show_results":
                if not player or not player.room_code:
                    return
                    
                room = self.rooms[player.room_code]
                # Only allow host to show results
                if player.player_id != room.host_player.player_id:
                    return
                    
                impostor_name = room.players[room.impostor_id].name if room.impostor_id in room.players else "Unknown"
                
                await self.broadcast_to_room(player.room_code, {
                    "type": "game_results",
                    "secretWord": room.secret_word,
                    "impostorName": impostor_name,
                    "impostorId": room.impostor_id
                })
                
            elif message_type == "new_round":
                if not player or not player.room_code:
                    return
                    
                room = self.rooms[player.room_code]
                if player.player_id != room.host_player.player_id:
                    return
                    
                if room.start_game():
                    await self.broadcast_to_room(player.room_code, {
                        "type": "new_round_started",
                        "gameState": {
                            "phase": "playing",
                            "playerCount": len(room.players)
                        }
                    })
                    
            elif message_type == "leave_room":
                if not player:
                    return
                    
                old_room_code = player.room_code
                self.leave_room(player)
                
                if old_room_code and old_room_code in self.rooms:
                    room = self.rooms[old_room_code]
                    await self.broadcast_to_room(old_room_code, {
                        "type": "player_left",
                        "players": room.get_player_list()
                    })
                    
        except Exception as e:
            print(f"Error handling message: {e}")
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Server error occurred"
            }))
            
    async def handle_disconnect(self, websocket):
        """Handle player disconnection"""
        player = self.websocket_to_player.get(websocket)
        if not player:
            return
            
        print(f"Player {player.name} disconnected")
        
        # Mark as disconnected but don't remove immediately
        player.connected = False
        
        # Notify room of disconnection
        if player.room_code and player.room_code in self.rooms:
            room = self.rooms[player.room_code]
            await self.broadcast_to_room(player.room_code, {
                "type": "player_disconnected", 
                "players": room.get_player_list()
            })
        
        # Remove from websocket mapping
        if websocket in self.websocket_to_player:
            del self.websocket_to_player[websocket]
            
        # Schedule cleanup after 30 seconds if not reconnected
        asyncio.create_task(self.cleanup_disconnected_player(player.player_id, 30))
        
    async def cleanup_disconnected_player(self, player_id: str, delay: int):
        """Remove player after delay if they haven't reconnected"""
        await asyncio.sleep(delay)
        
        if player_id in self.players:
            player = self.players[player_id]
            if not player.connected:  # Still disconnected after delay
                print(f"🗑️ Cleaning up disconnected player: {player.name}")
                
                if player.room_code:
                    self.leave_room(player)
                    
                if player_id in self.players:
                    del self.players[player_id]

def get_local_ip():
    """Get the local IP address of this machine"""
    # Prefer netifaces when available (faster/more accurate). Otherwise fall back to socket trick.
    if 'NETIFACES_AVAILABLE' in globals() and NETIFACES_AVAILABLE:
        try:
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr.get('addr')
                        # Skip localhost and link-local addresses
                        if ip and ip != '127.0.0.1' and not ip.startswith('169.254'):
                            return ip
        except Exception:
            # If anything goes wrong with netifaces, fall back below
            pass

    # Fallback: create a UDP socket to a public DNS to read the outbound IP
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # doesn't actually send packets
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if ip:
                return ip
    except Exception:
        pass

    # Last resort
    return "127.0.0.1"

class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
        
    def end_headers(self):
        try:
            # Enable CORS and prevent caching
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()
        except (ConnectionResetError, BrokenPipeError):
            # Client disconnected, ignore the error
            pass
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs to reduce noise
        pass
    
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except (ConnectionResetError, BrokenPipeError):
            # Client disconnected, ignore the error
            pass
    
    def do_GET(self):
        try:
            super().do_GET()
        except (ConnectionResetError, BrokenPipeError):
            # Client disconnected, ignore the error
            pass

def run_http_server(port=8080):
    """Run HTTP server for serving the game HTML"""
    try:
        server = HTTPServer(('0.0.0.0', port), HTTPRequestHandler)
        print(f"HTTP Server running on port {port}")
        server.serve_forever()
    except Exception as e:
        print(f"HTTP Server error: {e}")

# Global game server instance
game_server = None

async def websocket_handler(websocket):
    """Handle WebSocket connections"""
    global game_server
    
    try:
        print(f"🔌 New WebSocket connection from {websocket.remote_address}")
        
        # Register the connection
        game_server.clients.add(websocket)
        
        # Send initial connection message
        await websocket.send(json.dumps({
            'type': 'connected',
            'room_code': game_server.room_code,
            'message': 'Connected to game server'
        }))
        
        async for message in websocket:
            try:
                data = json.loads(message)
                await game_server.handle_message(websocket, data)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid message format"
                }))
    except websockets.exceptions.ConnectionClosed:
        print(f"🔌 WebSocket connection closed")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
    finally:
        await game_server.handle_disconnect(websocket)

def find_free_port(start_port, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def main():
    """Main server function"""
    # Get local IP
    local_ip = get_local_ip()
    
    # Find free ports
    http_port = find_free_port(8080)
    ws_port = find_free_port(8765)
    
    if not http_port or not ws_port:
        print("❌ Could not find available ports!")
        return
    
    print("🎮 Impostor Word Game Server Starting...")
    print("="*50)
    print(f"Local IP: {local_ip}")
    print(f"HTTP Server: http://{local_ip}:{http_port}")
    print(f"WebSocket Server: ws://{local_ip}:{ws_port}")
    print("="*50)
    print("\n📱 For phones to connect:")
    print(f"1. Make sure devices are on the same WiFi network")
    print(f"2. Open browser and go to: http://{local_ip}:{http_port}/Web.html")
    print(f"3. Or scan QR code if you generate one for: http://{local_ip}:{http_port}/Web.html")
    print("\n⚡ Server is ready for connections!")
    
    # Create game server instance
    global game_server
    game_server = GameServer()
    
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server, args=(http_port,), daemon=True)
    http_thread.start()
    
    # Start WebSocket server with proper asyncio setup
    async def start_servers():
        try:
            start_server = await websockets.serve(websocket_handler, "0.0.0.0", ws_port)
            print(f"✅ WebSocket server started on port {ws_port}")
            await start_server.wait_closed()
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"❌ Port {ws_port} is already in use. Please wait a moment and try again.")
            else:
                print(f"❌ Failed to start WebSocket server: {e}")
            return
    
    # Run the WebSocket server
    try:
        asyncio.run(start_servers())
    except KeyboardInterrupt:
        print("\n👋 Server shutting down...")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()
