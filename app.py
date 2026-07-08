import streamlit as st
import random
from datetime import datetime
from game_logic import Deck, Player, RummyGame
from utils import display_playing_card, display_card_back, display_player_info, apply_custom_css
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

# Initialize Firebase (optional for demo mode)
FIREBASE_ENABLED = False
db = None
try:
    import firebase_admin
    from firebase_admin import credentials, auth, firestore
    firebase_admin.get_app()
    db = firestore.client()
    FIREBASE_ENABLED = True
except:
    pass

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
    st.markdown("### 🎮 Game Lobby")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write("")
    with col2:
        if st.button("➕ Create Game", use_container_width=True):
            create_new_game()
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.write("")
    
    # Display available games
    if st.session_state.games:
        games_waiting = [g for g in st.session_state.games.values() if g['status'] == 'waiting']
        
        if games_waiting:
            cols = st.columns(1)
            for game in games_waiting:
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**🎴 Game #{game['game_id'][:8]}**")
                    with col2:
                        st.markdown(f"👥 {len(game['players'])}/6")
                    with col3:
                        st.markdown(f"💰 {game['entry_fee']} coins")
                    with col4:
                        st.markdown(f"⏱️ {game['created_at']}")
                    with col5:
                        if st.button("📍 Join", key=f"join_{game['game_id']}", use_container_width=True):
                            join_game(game['game_id'])
                    
                    st.divider()
        else:
            st.info("No games waiting for players. Create one to get started!")
    else:
        st.info("🎴 No games available yet. Create one to get started!")

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
        st.markdown(f"## 🎴 Game #{game['game_id'][:8]}")
    with col2:
        if st.button("🚪 Exit Game", use_container_width=True):
            st.session_state.page = "dashboard"
            st.session_state.current_game_id = None
            st.rerun()
    
    st.write("")
    
    # Game board area
    st.markdown('<div class="game-board">', unsafe_allow_html=True)
    
    current_player = game['players'][game['current_player_index']]
    st.markdown(f"### 📍 **{current_player['name']}'s Turn**")
    st.write("")
    
    board_col1, board_col2 = st.columns(2)
    
    with board_col1:
        st.markdown("#### 📦 Draw Pile")
        st.write("")
        # Display deck back
        display_card_back(len(game['deck']))
        st.write(f"**{len(game['deck'])} cards remaining**")
        
        if current_player['uid'] == st.session_state.user['uid']:
            if st.button("🎴 Draw Card", use_container_width=True, key="draw_btn"):
                draw_card(game)
                st.rerun()
        else:
            st.info("⏳ Waiting for current player...")
    
    with board_col2:
        st.markdown("#### 💨 Discard Pile")
        st.write("")
        if game['discard_pile']:
            last_card = game['discard_pile'][-1]
            display_playing_card(last_card, selected=False)
            st.write(f"**{last_card.rank}{last_card.suit}**")
        else:
            st.markdown('<div style="height: 140px; display: flex; align-items: center; justify-content: center; background-color: rgba(0,0,0,0.2); border-radius: 8px; border: 2px dashed #999;"><span style="color: #999; font-size: 18px;">Empty</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    
    # Players info
    st.markdown("### 👥 Players")
    cols = st.columns(len(game['players']))
    for idx, (col, player) in enumerate(zip(cols, game['players'])):
        with col:
            is_current = idx == game['current_player_index']
            display_player_info(player, is_current)
    
    st.write("")
    
    # Your hand
    st.markdown("### 🃏 Your Hand")
    my_hand = game['players'][0].get('hand', []) if game['players'] else []
    
    if my_hand:
        st.markdown('<div class="hand-container">', unsafe_allow_html=True)
        cols = st.columns(len(my_hand) if len(my_hand) <= 7 else 7)
        for idx, (col, card) in enumerate(zip(cols, my_hand)):
            with col:
                display_playing_card(card, selected=False)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if current_player['uid'] == st.session_state.user['uid']:
            st.write("")
            action_col1, action_col2 = st.columns(2)
            with action_col1:
                if st.button("✅ Play Cards", use_container_width=True):
                    st.info("Select cards by clicking them")
            with action_col2:
                if st.button("💨 Discard Card", use_container_width=True):
                    st.info("Select 1 card to discard")
    else:
        st.info("No cards in hand yet. Draw a card to start!")

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
