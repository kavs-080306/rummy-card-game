# 🎴 Rummy Card Game - Streamlit Edition

A fun multiplayer rummy card game built with **Streamlit** and **Firebase**.

## 🚀 Quick Start

### 1. **Clone & Setup**
```bash
git clone https://github.com/kavs-080306/rummy-card-game.git
cd rummy-card-game
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure Firebase**
- Create a Firebase project at https://console.firebase.google.com
- Get your credentials and create `.env`:
```bash
cp .env.example .env
# Edit .env with your Firebase credentials
```

### 4. **Run Locally**
```bash
streamlit run app.py
```
Visit: **http://localhost:8501**

---

## 📦 Features

✅ **Google Login** with Firebase Authentication  
✅ **Coin System** - Start with 1000 coins  
✅ **Game Lobby** - Create or join games  
✅ **Real-time Gameplay** - Draw, discard, play cards  
✅ **Multiplayer Support** - 2-6 players per game  
✅ **Game Statistics** - Track wins and coins  
✅ **Beautiful UI** - Dark themed Streamlit design  

---

## 🎮 How to Play

1. **Sign In** with email/password
2. **Create or Join** a game (10 coins entry fee)
3. **Play** - Draw cards, make sets/sequences, discard
4. **Win** - Be first to form valid rummy and discard all cards
5. **Earn** - Winners get coins!

---

## 🎯 Game Rules (Indian Rummy)

- **Players**: 2-6 players
- **Cards**: Standard deck (52 cards)
- **Hand Size**: 13 cards
- **Objective**: Form valid sets/sequences and discard all cards
- **Sets**: 3+ cards of same rank (different suits)
- **Sequences**: 3+ cards in order of same suit
- **Win**: First to form valid rummy + declare

---

## 🌐 Deployment

### Deploy to Streamlit Cloud (Free!)

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect GitHub repo
4. Select `app.py` as main file
5. Add environment variables from `.env`
6. Deploy! 🚀

**Your app is now live!**

---

## 📁 Project Structure

```
rummy-card-game/
├── app.py                 # Main Streamlit app
├── game_logic.py          # Card/Game/Player classes
├── utils.py               # UI utilities & styling
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.28+ |
| **Backend** | Streamlit (Built-in) |
| **Database** | Firebase Firestore |
| **Auth** | Firebase Authentication |
| **Hosting** | Streamlit Cloud |

---

## 📝 Session State Management

Uses Streamlit `session_state` for:
- ✅ Player authentication
- ✅ Game instances
- ✅ Player hands
- ✅ Game history
- ✅ Coin tracking

---

## 🔐 Security Notes

- Never commit `.env` file
- Use Firebase security rules in production
- Validate all player actions on backend
- Implement server-side coin verification

---

## 🐛 Known Limitations

- Real-time multiplayer uses polling (not true WebSocket)
- No chat/messaging yet
- Mobile UI needs optimization
- Game history not persisted to Firestore (yet)

---

## 📚 Future Improvements

- [ ] Firestore integration for persistent games
- [ ] Real-time updates with Firestore listeners
- [ ] Google Sign-In button
- [ ] Mobile app (React Native)
- [ ] Game chat and emojis
- [ ] Leaderboard
- [ ] Elo rating system
- [ ] Tournament mode
- [ ] Replay history

---

## 💬 Contributing

Found a bug? Want to add a feature? Feel free to fork and submit a PR!

---

## 📄 License

MIT License - Feel free to use this project!

---

## 🎉 Have Fun Playing!

Built with ❤️ using Streamlit

**GitHub**: https://github.com/kavs-080306/rummy-card-game
