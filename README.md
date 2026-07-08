# Rummy Card Game

A multiplayer rummy card game with Google authentication and coin-based payment system.

## Features
- 🎴 Real-time multiplayer rummy gameplay
- 🔐 Google Sign-in authentication
- 💰 Coin-based payment and rewards system
- 🎯 Game leaderboard and player statistics
- ⚡ Real-time game updates using Firestore

## Tech Stack
- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** Python Flask + Flask-CORS
- **Database:** Firebase (Firestore)
- **Authentication:** Google OAuth
- **Hosting:** Vercel (Frontend) + Railway/Render (Backend)

## Project Structure
```
rummy-card-game/
├── frontend/          # React app
├── backend/           # Python Flask API
└── README.md
```

## Setup Instructions

### 1. Firebase Setup
- Create a Firebase project at https://console.firebase.google.com
- Enable Google Authentication
- Create a Firestore database
- Get your Firebase config credentials

### 2. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Add your Firebase credentials to .env.local
npm run dev
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

## Game Rules
- Standard Indian Rummy rules
- 2-6 players per game
- Players pay coins to join
- Winners get coins as rewards
- Minimum 13 cards to win

## Contributing
Feel free to fork and submit PRs!

## License
MIT
