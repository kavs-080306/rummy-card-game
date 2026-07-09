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
        .login-card {
            background: white;
            border: 4px solid #ff6b35;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 90%;
        }
        .title {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.5rem;
            color: #0a4f0a;
        }
        .subtitle {
            font-size: 1.2rem;
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        .demo-note {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 12px;
            border-radius: 4px;
            font-size: 13px;
            color: #664d03;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="title">🎴 RUMMY</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Play with Friends. Win Coins!</div>', unsafe_allow_html=True)
        
        st.write("")
        
        email = st.text_input("📧 Email Address", placeholder="your@email.com", key="email_input")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter password", key="pass_input")
        
        st.write("")
        
        col_login, col_signup = st.columns(2)
        
        with col_login:
            if st.button("🔐 Sign In", use_container_width=True, key="signin_btn"):
                if email and password:
                    st.session_state.user = {
                        "uid": email.split("@")[0],
                        "email": email,
                        "name": email.split("@")[0].capitalize(),
                        "coins": 1000
                    }
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Please enter both email and password")
        
        with col_signup:
            if st.button("📝 Sign Up", use_container_width=True, key="signup_btn"):
                if email and password:
                    st.session_state.user = {
                        "uid": email.split("@")[0],
                        "email": email,
                        "name": email.split("@")[0].capitalize(),
                        "coins": 1000
                    }
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Please enter both email and password")
        
        st.markdown('<div class="demo-note">💡 Demo Mode: Use any email and password to login. Start with 1000 coins!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    st.markdown("# 🎴 Rummy Card Game - Dashboard")
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown(f"**Welcome, {st.session_state.user.get('name', 'Player')}!**")
    with col2:
        st.metric("💰 Your Coins", st.session_state.user.get("coins", 1000))
    with col3:
        pass
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()
    
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["🎮 GAME LOBBY", "📊 STATISTICS", "⚙️ SETTINGS"])
    
    with tab1:
        game_lobby_page()
    
    with tab2:
        st.subheader("📈 Your Game Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Games Played", "5")
        with col2:
            st.metric("Games Won", "2")
        with col3:
            st.metric("Win Rate", "40%")
        with col4:
            st.metric("Total Winnings", "250 coins")
    
    with tab3:
        st.write("⚙️ Settings coming soon...")
        st.write("- Sound preferences")
        st.write("- Difficulty levels")
        st.write("- Display options")

def game_lobby_page():
    st.markdown("### 🎮 Find or Create a Game")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write("")
    with col2:
        if st.button("➕ CREATE NEW GAME", use_container_width=True, key="create_game_btn"):
            create_new_game()
    with col3:
        if st.button("🔄 REFRESH", use_container_width=True):
            st.rerun()
    
    st.write("")
    
    # Display available games
    if st.session_state.games:
        games_waiting = [g for g in st.session_state.games.values() if g['status'] == 'waiting']
        
        if games_waiting:
            st.markdown("**💡 Available Games:**")
            st.write("")
            for idx, game in enumerate(games_waiting):
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                
                with col1:
                    st.markdown(f"### 🎴 Game #{game['game_id'][-4:]}")
                with col2:
                    st.markdown(f"### 👥 {len(game['players'])}/6 Players")
                with col3:
                    st.markdown(f"### 💰 {game['entry_fee']} coins")
                with col4:
                    created_time = game['created_at']
                    st.markdown(f"### ⏱️ New")
                with col5:
                    if st.button("📍 JOIN", key=f"join_{game['game_id']}", use_container_width=True):
                        join_game(game['game_id'])
                
                st.divider()
        else:
            st.markdown('<div class="game-card" style="text-align: center; padding: 40px;"><p style="font-size: 18px; color: #666;">No games waiting. Be the first to create one! 🎯</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="game-card" style="text-align: center; padding: 40px;"><p style="font-size: 18px; color: #666;">No games available yet. Click <strong>CREATE NEW GAME</strong> to start! 🎯</p></div>', unsafe_allow_html=True)

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
        st.markdown(f"### 🎴 Rummy Game #{game['game_id'][-4:]}")
    with col2:
        if st.button("🚪 Exit Game", use_container_width=True):
            st.session_state.page = "dashboard"
            st.session_state.current_game_id = None
            st.rerun()
    
    st.write("")
    
    # Game board area - GREEN FELT TABLE
    st.markdown('<div class="game-board">', unsafe_allow_html=True)
    
    current_player = game['players'][game['current_player_index']]
    st.markdown(f'<div class="board-title">🎯 {current_player["name"]} Playing</div>', unsafe_allow_html=True)
    
    board_col1, board_col2 = st.columns(2)
    
    with board_col1:
        st.markdown('<div class="pile-container">', unsafe_allow_html=True)
        st.markdown('<div class="pile-label">📦 DRAW PILE</div>', unsafe_allow_html=True)
        display_card_back(len(game['deck']))
        st.markdown(f'<p style="color: #fff; text-align: center; margin-top: 10px; font-weight: bold;">{len(game["deck"])} cards</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if current_player['uid'] == st.session_state.user['uid']:
            st.write("")
            if st.button("🎴 DRAW CARD", use_container_width=True, key="draw_btn"):
                draw_card(game)
                st.rerun()
        else:
            st.write("")
            st.info("⏳ Waiting for current player to draw...")
    
    with board_col2:
        st.markdown('<div class="pile-container">', unsafe_allow_html=True)
        st.markdown('<div class="pile-label">💨 DISCARD PILE</div>', unsafe_allow_html=True)
        if game['discard_pile']:
            last_card = game['discard_pile'][-1]
            display_playing_card(last_card, selected=False)
        else:
            st.markdown('<p style="color: #aaa; text-align: center; font-size: 18px; margin-top: 30px;">Empty</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    
    # Players info
    st.markdown('### 👥 Players in Game')
    cols = st.columns(len(game['players']))
    for idx, (col, player) in enumerate(zip(cols, game['players'])):
        with col:
            is_current = idx == game['current_player_index']
            display_player_info(player, is_current)
    
    st.write("")
    
    # Your hand
    st.markdown('### 🃏 Your Hand')
    my_hand = game['players'][0].get('hand', []) if game['players'] else []
    
    if my_hand:
        st.markdown('<div class="hand-container">', unsafe_allow_html=True)
        st.markdown('<div class="hand-title">Select cards to play</div>', unsafe_allow_html=True)
        
        # Display cards in rows
        cards_per_row = 7
        for i in range(0, len(my_hand), cards_per_row):
            row_cards = my_hand[i:i + cards_per_row]
            cols = st.columns(len(row_cards))
            for col, card in zip(cols, row_cards):
                with col:
                    display_playing_card(card, selected=False)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if current_player['uid'] == st.session_state.user['uid']:
            st.write("")
            st.write("**Your turn! Choose an action:**")
            action_col1, action_col2 = st.columns(2)
            with action_col1:
                if st.button("✅ PLAY SETS", use_container_width=True, key="play_btn"):
                    st.info("🎯 Click cards to select them, then confirm")
            with action_col2:
                if st.button("💨 DISCARD CARD", use_container_width=True, key="discard_btn"):
                    st.info("📌 Select 1 card to discard and end your turn")
    else:
        st.markdown('<div class="hand-container"><p style="color: #ffeb3b; text-align: center; font-size: 16px;">No cards yet. Draw a card to start playing!</p></div>', unsafe_allow_html=True)

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
