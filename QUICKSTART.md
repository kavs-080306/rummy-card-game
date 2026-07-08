# 🚀 Quick Start Guide - Rummy Card Game

## 5-Minute Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/kavs-080306/rummy-card-game.git
cd rummy-card-game
```

### 2. Create Python Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Firebase (Optional for now)
```bash
cp .env.example .env
# Edit .env with your Firebase credentials later
```

### 5. Run the App
```bash
streamlit run app.py
```

**Visit:** http://localhost:8501

---

## 🎮 Demo Credentials

**Email:** demo@example.com  
**Password:** anything  

(Demo login works without Firebase)

---

## ✨ Features Ready to Use

✅ **Login/Signup** - Demo auth  
✅ **Create Game** - Start multiplayer sessions  
✅ **Join Game** - Find and join games  
✅ **Play Cards** - Draw, discard, play actions  
✅ **Game Board** - Beautiful card display  
✅ **Player Stats** - Track performance  

---

## 🎯 Next: Firebase Integration

When ready to use real authentication:

1. Create Firebase project: https://console.firebase.google.com
2. Copy credentials to `.env`
3. Import Firebase admin SDK (already in requirements.txt)
4. Update login logic in `app.py`

---

## 📦 Deploy to Streamlit Cloud (Free!)

1. Push to GitHub
2. Go to https://share.streamlit.io
3. Select your repo and `app.py`
4. Add `.env` variables in "Advanced settings"
5. Click "Deploy"

**Done!** Your game is live! 🎉

---

## 📁 Project Files

```
rummy-card-game/
├── app.py              # Main Streamlit app (1000 lines)
├── game_logic.py       # Game classes (Card, Deck, Player, Game)
├── utils.py            # UI utilities & styling
├── requirements.txt    # Python packages
├── .streamlit/
│   └── config.toml     # Streamlit theme config
├── Dockerfile          # For containerized deployment
├── docker-compose.yml  # Docker setup
├── Procfile            # For Heroku deployment
├── DEPLOYMENT.md       # Full deployment guide
└── README.md           # Documentation
```

---

## 🐛 Troubleshooting

**Port 8501 in use?**
```bash
streamlit run app.py --server.port=8502
```

**Module not found error?**
```bash
pip install --upgrade -r requirements.txt
```

**Games not appearing?**
```bash
# Check browser cache
# Clear streamlit cache with Ctrl+R
# Restart app
```

---

## 💡 Current Features

| Feature | Status |
|---------|--------|
| Login/Signup | ✅ |
| Create Game | ✅ |
| Join Game | ✅ |
| Draw Card | ✅ |
| Discard Card | ✅ |
| Play Cards | 🔜 |
| Win Detection | 🔜 |
| Firebase Auth | 🔜 |
| Coin System | 🔜 |
| Leaderboard | 🔜 |

---

## 🎉 Ready to Play!

Let's build the future of card games! 

**Questions?** Check DEPLOYMENT.md for advanced setup.
