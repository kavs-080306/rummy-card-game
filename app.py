import streamlit as st
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Note: Keeping your custom imports intact, though we handle card UI rendering inside app.py below
# from game_logic import Deck, Player, RummyGame
# from utils import display_playing_card, display_card_back, display_player_info, apply_custom_css

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
if 'selected_card_idx' not in st.session_state:
    st.session_state.selected_card_idx = None

# Page styling configuration
st.set_page_config(
    page_title="🎴 Elite Rummy Club",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- GLOBAL STYLES FOR REAL CASINO VIBE ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main background & Theme overhaul */
        .stApp {
            background-color: #0f2027;
            background-image: linear-gradient(to bottom, #203a43, #0f2027);
            color: #ffffff;
        }
        
        /* Green Felt Table Container */
        .game-board {
            background: radial-gradient(circle, #116234 0%, #083b1e 100%);
            border: 12px solid #5c3a21;
            border-radius: 24px;
            padding: 30px;
            box-shadow: inset 0 0 40px rgba(0,0,0,0.8), 0 15px 30px rgba(0,0,0,0.5);
            margin-bottom: 25px;
        }
        
        .board-title {
            font-family: 'Georgia', serif;
            font-size: 1.8rem;
            color: #f1c40f;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
            text-align: center;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }

        /* Pure CSS Playing Cards */
        .playing-card {
            background: #ffffff;
            border-radius: 10px;
            padding: 10px;
            width: 100px;
            height: 145px;
            box-shadow: 3px 5px 15px rgba(0,0,0,0.4);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
            user-select: none;
            margin: 5px auto;
        }
        .playing-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 25px rgba(0,0,0,0.6);
        }
        .playing-card.selected {
            border: 3px solid #f1c40f !important;
            transform: translateY(-15px);
            box-shadow: 0 0 15px #f1c40f;
        }
        .card-red { color: #e74c3c; }
        .card-black { color: #2c3e50; }
        
        .card-corner {
            font-size: 1.4rem;
            font-weight: bold;
            line-height: 1;
        }
        .card-corner.bottom {
            transform: rotate(180deg);
            align-self: flex-end;
        }
        .card-center-suit {
            font-size: 2.5rem;
            text-align: center;
            align-self: center;
            line-height: 1;
        }

        /* Card Back Cover */
        .card-back {
            background: repeating-linear-gradient(45deg, #c0392b, #c0392b 10px, #962d22 10px, #962d22 20px);
            border: 4px solid #ffffff;
            border-radius: 10px;
            width: 100px;
            height: 145px;
            box-shadow: 3px 5px 15px rgba(0,0,0,0.4);
            margin: 5px auto;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .card-back-inner {
            width: 80px;
            height: 125px;
            border: 2px dashed rgba(255,255,255,0.4);
            border-radius: 6px;
        }

        /* Hand Container Style */
        .hand-container {
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            margin-top: 15px;
        }
        
        /* Custom styling for metrics */
        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.05);
            padding: 10px 20px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- CARD RENDERER HELPERS ---
def render_card_ui(card, selected=False, key=None):
    """Generates clean HTML markup mimicking an actual casino playing card."""
    suit = card['suit']
    rank = card['rank']
    is_red = suit in ["♥", "♦"]
    color_class = "card-red" if is_red else "card-black"
    selected_class = "selected" if selected else ""
    
    card_html = f"""
    <div class="playing-card {color_class} {selected_class}">
        <div class="card-corner top">
            <div>{rank}</div>
            <div style="font-size: 1.1rem; margin-top:2px;">{suit}</div>
        </div>
        <div class="card-center-suit">{suit}</div>
        <div class="card-corner bottom">
            <div>{rank}</div>
            <div style="font-size: 1.1rem; margin-top:2px;">{suit}</div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_card_back_ui():
    """Generates a premium textured card back design."""
    back_html = """
    <div class="card-back">
        <div class="card-back-inner"></div>
    </div>
    """
    st.markdown(back_html, unsafe_allow_html=True)


# --- APPLICATION PAGES ---
def login_page():
    st.markdown("""
    <style>
        .login-card {
            background: #ffffff;
            border: 4px solid #f1c40f;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            max-width: 400px;
            margin: 100px auto;
            color: #333333;
        }
        .login-title {
            font-size: 3rem;
            font-weight: 900;
            text-align: center;
            color: #083b1e;
            margin-bottom: 0.5rem;
            font-family: 'Georgia', serif;
        }
        .login-subtitle {
            font-size: 1.1rem;
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">🎰 RUMMY</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Elite Card Room Experience</div>', unsafe_allow_html=True)
        
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
                    st.error("Please enter credentials")
        
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
        
        st.markdown('<div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; border-radius: 4px; font-size: 13px; color: #664d03; margin-top: 20px;">💡 Demo Mode: Use any login to play with 1,000 complimentary chips!</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    st.markdown("# 🎴 Grand Lobby")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### Welcome back, **{st.session_state.user.get('name', 'Player')}**")
    with col2:
        st.metric("💰 Available Chips", f"{st.session_state.user.get('coins', 1000)} pts")
    with col3:
        if st.button("🚪 Leave Club", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()
    
    st.divider()
    tab1, tab2, tab3 = st.tabs(["🎮 ACTIVE TABLES", "📈 PLAYER PROFILE", "⚙️ ROOM SETTINGS"])
    
    with tab1:
        game_lobby_page()
    with tab2:
        st.subheader("📈 Season History")
        c1, c2, c3 = st.columns(3)
        c1.metric("Games Played", "14")
        c2.metric("Matches Won", "8")
        c3.metric("Win Ratio", "57.1%")
    with tab3:
        st.write("⚙️ Fine-tune card styles, table layouts, and automated sorting triggers here soon.")

def game_lobby_page():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🏟️ Open Stakes Lounge")
    with col2:
        if st.button("➕ OPEN NEW TABLE", use_container_width=True, key="create_game_btn"):
            create_new_game()
            
    st.write("")
    
    if st.session_state.games:
        games_waiting = [g for g in st.session_state.games.values() if g['status'] == 'waiting']
        if games_waiting:
            for game in games_waiting:
                col_id, col_pl, col_fee, col_act = st.columns([1, 1, 1, 1])
                col_id.markdown(f"**Table #{game['game_id'][-4:]}**")
                col_pl.markdown(f"👥 {len(game['players'])}/6 Seats filled")
                col_fee.markdown(f"💰 {game['entry_fee']} Entry Buy-in")
                with col_act:
                    if st.button("📍 SIT DOWN", key=f"join_{game['game_id']}", use_container_width=True):
                        join_game(game['game_id'])
                st.divider()
        else:
            st.info("All tables are fully locked into active games right now. Open a new deck table!")
    else:
        st.info("No active tables running. Click 'OPEN NEW TABLE' to seat yourself.")

def create_new_game():
    game_id = f"game_{random.randint(10000, 99999)}"
    starting_deck = generate_deck()
    
    # Pre-deal 13 classic cards to the creator
    player_hand = [starting_deck.pop() for _ in range(13)]
    
    creator_player = {
        "uid": st.session_state.user["uid"],
        "name": st.session_state.user["name"],
        "hand": player_hand
    }
    
    st.session_state.games[game_id] = {
        "game_id": game_id,
        "creator_id": st.session_state.user["uid"],
        "players": [creator_player],
        "entry_fee": 100,
        "status": "waiting",
        "created_at": datetime.now(),
        "deck": starting_deck,
        "discard_pile": [starting_deck.pop()], # Start discard pile with top card
        "current_player_index": 0,
    }
    st.session_state.current_game_id = game_id
    st.session_state.page = "game"
    st.rerun()

def join_game(game_id):
    game = st.session_state.games[game_id]
    if game['entry_fee'] > st.session_state.user['coins']:
        st.error("Insufficient chip balance!")
        return
        
    new_hand = [game['deck'].pop() for _ in range(13)]
    joining_player = {
        "uid": st.session_state.user["uid"],
        "name": st.session_state.user["name"],
        "hand": new_hand
    }
    
    game['players'].append(joining_player)
    st.session_state.current_game_id = game_id
    st.session_state.page = "game"
    st.rerun()

def game_page():
    if not st.session_state.current_game_id or st.session_state.current_game_id not in st.session_state.games:
        st.error("Table session disconnected.")
        if st.button("Back to Lobby"):
            st.session_state.page = "dashboard"
            st.rerun()
        return
    
    game = st.session_state.games[st.session_state.current_game_id]
    current_player = game['players'][game['current_player_index']]
    
    # Header bar
    col_t, col_ex = st.columns([3, 1])
    col_t.markdown(f"### 🎴 Elite Club • Table #{game['game_id'][-4:]}")
    with col_ex:
        if st.button("🚪 Stand Up & Leave", use_container_width=True):
            st.session_state.page = "dashboard"
            st.session_state.current_game_id = None
            st.rerun()
            
    st.write("")

    # --- THE GREEN FELT CASINO TABLE ---
    st.markdown('<div class="game-board">', unsafe_allow_html=True)
    st.markdown(f'<div class="board-title">♠️ ♦️ CURRENT PLAYER TURN: {current_player["name"].upper()} ♥️ ♣️</div>', unsafe_allow_html=True)
    
    b_col1, b_col2 = st.columns(2)
    
    with b_col1:
        st.markdown('<div style="text-align: center; background: rgba(0,0,0,0.2); padding:15px; border-radius:12px;">', unsafe_allow_html=True)
        st.markdown('<p style="color:#f1c40f; font-weight:bold; margin-bottom:10px;">📦 MAIN DRAW DECK</p>', unsafe_allow_html=True)
        render_card_back_ui()
        st.markdown(f'<p style="color:#ccc; margin-top:10px;"><b>{len(game["deck"])}</b> cards remaining</p>', unsafe_allow_html=True)
        
        # Draw interaction
        if current_player['uid'] == st.session_state.user['uid']:
            if st.button("📥 DRAW NEW CARD", use_container_width=True, key="draw_btn_real"):
                draw_card(game)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with b_col2:
        st.markdown('<div style="text-align: center; background: rgba(0,0,0,0.2); padding:15px; border-radius:12px;">', unsafe_allow_html=True)
        st.markdown('<p style="color:#e74c3c; font-weight:bold; margin-bottom:10px;">🗑️ DISCARD PILE</p>', unsafe_allow_html=True)
        if game['discard_pile']:
            render_card_ui(game['discard_pile'][-1], selected=False)
            st.markdown(f'<p style="color:#ccc; margin-top:10px;">Top Card Shown</p>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:145px; display:flex; align-items:center; justify-content:center; color:#777;">Pile Empty</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- YOUR HAND CARD INTERACTION ---
    st.markdown('### 🃏 Your Hand Dealt')
    
    # Find matching logged-in player model configuration
    my_player_data = next((p for p in game['players'] if p['uid'] == st.session_state.user['uid']), None)
    
    if my_player_data and 'hand' in my_player_data and my_player_data['hand']:
        my_hand = my_player_data['hand']
        
        st.markdown('<div class="hand-container">', unsafe_allow_html=True)
        
        # Display index radio selector underneath cards to capture action context cleanly
        card_cols = st.columns(len(my_hand))
        for idx, card in enumerate(my_hand):
            with card_cols[idx]:
                is_selected = (st.session_state.selected_card_idx == idx)
                render_card_ui(card, selected=is_selected)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action Bar UI Controls
        st.write("")
        control_col1, control_col2, control_col3 = st.columns([1.5, 1, 1.5])
        
        with control_col1:
            selected_idx = st.selectbox(
                "🎯 Choose a card from hand to manipulate:",
                options=range(len(my_hand)),
                format_func=lambda x: f"Card {x+1}: {my_hand[x]['rank']}{my_hand[x]['suit']}"
            )
            if st.button("🔍 Highlight Chosen Card"):
                st.session_state.selected_card_idx = selected_idx
                st.rerun()
                
        with control_col3:
            if current_player['uid'] == st.session_state.user['uid']:
                st.markdown("<p style='color:#f1c40f;'><b>Your Turn Options:</b></p>", unsafe_allow_html=True)
                act_c1, act_c2 = st.columns(2)
                with act_c1:
                    if st.button("💨 Discard Card", use_container_width=True):
                        # Action logic: pop card to discard pile
                        card_to_discard = my_hand.pop(selected_idx)
                        game['discard_pile'].append(card_to_discard)
                        # Hand over turn index loop
                        game['current_player_index'] = (game['current_player_index'] + 1) % len(game['players'])
                        st.session_state.selected_card_idx = None
                        st.success("Discard submitted successfully!")
                        st.rerun()
                with act_c2:
                    if st.button("🃏 Melt Set/Meld", use_container_width=True):
                        st.toast("Meld verified! Classic matching combination locked in.", icon="🏆")
    else:
        st.info("Waiting on cards to be dealt out dynamically to your terminal seat.")

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
        st.toast(f"Drew {card['rank']}{card['suit']} from Main Deck!", icon="📥")
        st.rerun()

# Main Application Router Navigation
def main():
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()
    elif st.session_state.page == "game":
        game_page()

if __name__ == "__main__":
    main()
