# 🕵️ Impostor Word Game - Multiplayer Edition

A fun multiplayer guessing game where players try to find the impostor who doesn't know the secret word!

## 🎮 How to Play

1. **One player hosts** the game on their computer
2. **Other players join** using their phones/devices on the same WiFi network
3. **Each player gets a role** - either they see the secret word or they're the impostor
4. **Players reveal their roles** by clicking "I've Seen My Role"
5. **Start discussing** - give hints about the word without saying it directly
6. **Find the impostor** - who's trying to blend in without knowing the word!

## 🚀 Setup Instructions

### 1. Install Dependencies
Run the setup script to install required packages:
```bash
./setup.sh
```

Or manually install:
```bash
pip3 install -r requirements.txt
```

### 2. Start the Server
```bash
python3 server.py
```

The server will show you:
- Your local IP address
- The URL for players to connect to

### 3. Connect Players
- **Host computer**: Open `http://localhost:8080/Web.html`
- **Other devices**: Open `http://[SERVER_IP]:8080/Web.html` (replace [SERVER_IP] with the IP shown by the server)

### 4. Create or Join Game
- **Host**: Click "Host Game", enter your name, and create a room
- **Players**: Click "Join Game", enter your name and the room code

## 📱 Mobile Connection

Players can connect using any device with a web browser:
- Phones, tablets, laptops - anything with WiFi!
- Make sure all devices are on the same WiFi network
- The game automatically detects and connects to the server

## 🎯 Game Features

- **Real-time multiplayer** - up to 8 players
- **Automatic role assignment** - random impostor selection
- **Role revelation system** - players must confirm they've seen their role
- **Multiple rounds** - play again with the same group
- **Responsive design** - works great on mobile devices
- **Network discovery** - automatic server detection on local network

## 🔧 Technical Details

### Architecture
- **Backend**: Python WebSocket server with room management
- **Frontend**: HTML5 with WebSocket client
- **Networking**: Local WiFi network communication
- **Real-time**: Instant updates for all players

### Ports Used
- **8080**: HTTP server (serves the game webpage)
- **8765**: WebSocket server (handles game communication)

### Requirements
- Python 3.6+
- WiFi network (all devices must be connected to the same network)
- Modern web browser on each device

## 🎪 Game Rules

1. **3-8 players required** to start a game
2. **One random player** becomes the impostor
3. **Everyone else** sees the secret word
4. **Discuss and give hints** without saying the word directly
5. **Impostor** tries to blend in and figure out the word
6. **Vote or discuss** to find the impostor!

## 🛠️ Troubleshooting

### Can't Connect to Server
- Make sure all devices are on the same WiFi network
- Check that the server is running (`python3 server.py`)
- Try the IP address shown by the server
- Disable VPN if you're using one

### Game Not Working
- Refresh the webpage
- Check browser console for errors
- Restart the server if needed

### Firewall Issues
- The server needs ports 8080 and 8765 open
- On macOS, you may need to allow Python through the firewall

## 🎨 Customization

You can easily customize the game by editing:
- **Word list**: Modify the `concepts` array in `server.py`
- **Styling**: Edit the CSS in `Web.html`
- **Game rules**: Adjust player limits, timing, etc. in `server.py`

## 📝 License

This is a fun open-source project! Feel free to modify and share.

---

**Have fun playing! 🎉**
