import streamlit as st
import random
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Streamlit session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'games' not in st.session_state:
    st.session_state.games = {}
if 'current_game_id' not in st.session_state:
    st.session_state.current_game_id = None

# Initialize Firebase
try:
    firebase_admin.get_app()
except ValueError:
    firebase_config = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID")
    }
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": firebase_config["projectId"],
    })
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Page styling
st.set_page_config(
    page_title="🎴 Rummy Card Game",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def login_page():
    st.markdown("""
    <style>
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .title {
            font-size: 4rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1rem;
        }
        .subtitle {
            font-size: 1.5rem;
            text-align: center;
            color: #9ca3af;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="title">🎴 Rummy</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Play with Friends. Earn Coins. Have Fun!</div>', unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        
        email = st.text_input("📧 Email", placeholder="your@email.com")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter password")
        
        col_login, col_signup = st.columns(2)
        
        with col_login:
            if st.button("🔐 Sign In", use_container_width=True):
                if email and password:
                    # Demo login (in production, use actual Firebase auth)
                    st.session_state.user = {
                        "uid": email.split("@")[0],
                        "email": email,
                        "name": email.split("@")[0],
                        "coins": 1000
                    }
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Please enter email and password")
        
        with col_signup:
            if st.button("📝 Sign Up", use_container_width=True):
                if email and password:
                    st.session_state.user = {
                        "uid": email.split("@")[0],
                        "email": email,
                        "name": email.split("@")[0],
                        "coins": 1000
                    }
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Please enter email and password")
        
        st.info("💡 Demo: Use any email and password to continue")

def dashboard_page():
    st.markdown("# 🎴 Rummy Card Game")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        pass
    with col2:
        st.metric("💰 Coins", st.session_state.user.get("coins", 1000))
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["🎮 Game Lobby", "📊 Statistics", "⚙️ Settings"])
    
    with tab1:
        game_lobby_page()
    
    with tab2:
        st.subheader("Your Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Games Played", 5)
        with col2:
            st.metric("Games Won", 2)
        with col3:
            st.metric("Win Rate", "40%")
    
    with tab3:
        st.write("Settings coming soon...")

def game_lobby_page():
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("Available Games")
    with col2:
        if st.button("➕ Create Game", use_container_width=True):
            create_new_game()
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.write("")
    
    # Display available games
    if st.session_state.games:
        for game_id, game in st.session_state.games.items():
            if game['status'] == 'waiting':
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.write(f"**Game #{game_id[:8]}**")
                with col2:
                    st.write(f"Players: {len(game['players'])}/6")
                with col3:
                    st.write(f"Entry: {game['entry_fee']} coins")
                with col4:
                    if st.button("Join", key=f"join_{game_id}"):
                        join_game(game_id)
                st.divider()
    else:
        st.info("No games available. Create one to get started!")

def create_new_game():
    game_id = f"game_{random.randint(10000, 99999)}"
    st.session_state.games[game_id] = {
        "game_id": game_id,
        "creator_id": st.session_state.user["uid"],
        "players": [st.session_state.user],
        "entry_fee": 10,
        "status": "waiting",
        "created_at": datetime.now(),
        "deck": generate_deck(),
        "discard_pile": [],
        "current_player_index": 0,
    }
    st.session_state.current_game_id = game_id
    st.session_state.page = "game"
    st.success(f"✅ Game {game_id[:8]} created!")
    st.rerun()

def join_game(game_id):
    if st.session_state.games[game_id]['entry_fee'] > st.session_state.user['coins']:
        st.error("Not enough coins to join!")
        return
    
    st.session_state.games[game_id]['players'].append(st.session_state.user)
    st.session_state.current_game_id = game_id
    st.session_state.page = "game"
    st.success("✅ Joined game!")
    st.rerun()

def game_page():
    if not st.session_state.current_game_id or st.session_state.current_game_id not in st.session_state.games:
        st.error("Game not found!")
        if st.button("Back to Lobby"):
            st.session_state.page = "dashboard"
            st.rerun()
        return
    
    game = st.session_state.games[st.session_state.current_game_id]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## Game #{game['game_id'][:8]}")
    with col2:
        if st.button("🚪 Exit Game"):
            st.session_state.page = "dashboard"
            st.session_state.current_game_id = None
            st.rerun()
    
    st.write("")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("🎯 Game Board")
        
        current_player = game['players'][game['current_player_index']]
        st.info(f"📍 Current Turn: **{current_player['name']}**")
        
        board_col1, board_col2 = st.columns([1, 1])
        
        with board_col1:
            st.markdown("### 📦 Draw Pile")
            st.write(f"Cards remaining: {len(game['deck'])}")
            if st.button("Draw Card"):
                if current_player['uid'] == st.session_state.user['uid']:
                    draw_card(game)
                else:
                    st.warning("Not your turn!")
        
        with board_col2:
            st.markdown("### 💨 Discard Pile")
            if game['discard_pile']:
                last_card = game['discard_pile'][-1]
                st.write(f"Last card: {last_card}")
            else:
                st.write("Empty")
    
    with col2:
        st.subheader("👥 Players")
        for idx, player in enumerate(game['players']):
            is_current = idx == game['current_player_index']
            status = "🎯 Current" if is_current else "⏳ Waiting"
            st.write(f"**{player['name']}** {status}")
            st.write(f"💰 {player['coins']} coins | 🃏 {len(player.get('hand', []))} cards")
    
    with col3:
        st.subheader("⚙️ Actions")
        if current_player['uid'] == st.session_state.user['uid']:
            if st.button("Play Cards"):
                st.info("Card selection coming soon...")
            if st.button("Discard"):
                st.info("Discard selection coming soon...")
        else:
            st.write("Waiting for your turn...")

def generate_deck():
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [{"suit": suit, "rank": rank} for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def draw_card(game):
    if game['deck']:
        card = game['deck'].pop()
        current_player = game['players'][game['current_player_index']]
        if 'hand' not in current_player:
            current_player['hand'] = []
        current_player['hand'].append(card)
        
        # Move to next player
        game['current_player_index'] = (game['current_player_index'] + 1) % len(game['players'])
        st.success("✅ Card drawn!")
        st.rerun()

# Main navigation
def main():
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()
    elif st.session_state.page == "game":
        game_page()

if __name__ == "__main__":
    main()
