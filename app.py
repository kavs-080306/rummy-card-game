import streamlit as st
import random
from datetime import datetime
import threading

# --- GLOBAL TRACKER FOR MULTI-USER SYNC ---
# This dictionary lives at the application server level, meaning ALL users share it.
if "_GLOBAL_ROOMS" not in globals():
    globals()["_GLOBAL_ROOMS"] = {}
    globals()["_ROOM_LOCK"] = threading.Lock()

GLOBAL_ROOMS = globals()["_GLOBAL_ROOMS"]
ROOM_LOCK = globals()["_ROOM_LOCK"]

# Initialize local player session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'current_game_id' not in st.session_state:
    st.session_state.current_game_id = None
if 'selected_card_idx' not in st.session_state:
    st.session_state.selected_card_idx = None

st.set_page_config(
    page_title="👑 Elite Multiplayer Rummy",
    page_icon="🎴",
    layout="wide"
)

# --- THEME & CASINO CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0d1b1e; color: #ffffff; }
    .game-board {
        background: radial-gradient(circle, #0d5c3a 0%, #052416 100%);
        border: 10px solid #4a2e1b;
        border-radius: 20px;
        padding: 25px;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.7), 0 10px 20px rgba(0,0,0,0.5);
    }
    .playing-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 8px;
        width: 85px;
        height: 125px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.3);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s;
        margin: auto;
    }
    .playing-card.selected {
        border: 3px solid #ffcc00 !important;
        transform: translateY(-10px);
    }
    .card-red { color: #d63031; }
    .card-black { color: #2d3436; }
    .card-back {
        background: repeating-linear-gradient(45deg, #b33939, #b33939 8px, #8c2a2a 8px, #8c2a2a 16px);
        border: 3px solid #fff;
        border-radius: 8px;
        width: 85px;
        height: 125px;
        margin: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER UI RENDERERS ---
def render_card(card, selected=False):
    suit, rank = card['suit'], card['rank']
    color = "card-red" if suit in ["♥", "♦"] else "card-black"
    sel_class = "selected" if selected else ""
    st.markdown(f"""
    <div class="playing-card {color} {sel_class}">
        <div style="font-weight:bold; font-size:1.1rem; line-height:1;">{rank}<br><span style="font-size:0.8rem;">{suit}</span></div>
        <div style="font-size:2rem; text-align:center;">{suit}</div>
        <div style="font-weight:bold; font-size:1.1rem; text-align:right; line-height:1; transform:rotate(180deg);">{rank}<br><span style="font-size:0.8rem;">{suit}</span></div>
    </div>
    """, unsafe_allow_html=True)

def render_card_back():
    st.markdown('<div class="card-back"></div>', unsafe_allow_html=True)

def generate_deck():
    suits, ranks = ["♠", "♥", "♦", "♣"], ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck = [{"suit": s, "rank": r} for s in suits for r in ranks]
    random.shuffle(deck)
    return deck

# --- APP FLOW PAGES ---
def login_page():
    st.title("🎴 Global Rummy Lounge")
    st.subheader("Play with your friends across different screens")
    
    with st.form("login_form"):
        username = st.text_input("Choose a display name:", placeholder="Player 1")
        # Fixed the structural bug here
        submit = st.form_submit_button("Enter Casino Lobby")
        if submit and username:
            st.session_state.user = {
                "uid": f"usr_{random.randint(1000,9999)}",
                "name": username.strip()
            }
            st.session_state.page = "lobby"
            st.rerun()

def lobby_page():
    st.markdown(f"### 🏟️ Welcome, **{st.session_state.user['name']}**")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Available Multi-Friend Tables")
    with col2:
        if st.button("➕ CREATE NEW ROOM", use_container_width=True):
            with ROOM_LOCK:
                room_code = f"ROOM_{random.randint(1000, 9999)}"
                GLOBAL_ROOMS[room_code] = {
                    "id": room_code,
                    "players": [],  # List of player dicts
                    "deck": generate_deck(),
                    "discard_pile": [],
                    "turn_idx": 0,
                    "status": "waiting"
                }
            st.session_state.current_game_id = room_code
            st.session_state.page = "game"
            st.rerun()

    st.write("---")
    
    # Read currently open cross-session rooms safely
    with ROOM_LOCK:
        active_rooms = list(GLOBAL_ROOMS.items())

    if active_rooms:
        for r_code, r_data in active_rooms:
            c_info, c_pl, c_join = st.columns([2, 1, 1])
            c_info.markdown(f"#### 🎰 Table Code: `{r_code}`")
            c_pl.write(f"👥 Seats Filled: {len(r_data['players'])}/4")
            with c_join:
                if r_data["status"] == "waiting" and len(r_data["players"]) < 4:
                    if st.button("Join Seat", key=f"join_{r_code}", use_container_width=True):
                        st.session_state.current_game_id = r_code
                        st.session_state.page = "game"
                        st.rerun()
                else:
                    st.write("🔒 *In progress / Full*")
            st.write("---")
    else:
        st.info("No active rooms right now. Create one and tell your friend the room code!")

# --- MULTIPLAYER REAL-TIME FRAGMENT ---
@st.fragment(run_every=2.5)  # Auto-refreshes game table state every 2.5 seconds dynamically!
def live_game_board(room_code):
    with ROOM_LOCK:
        if room_code not in GLOBAL_ROOMS:
            st.error("Room dissolved!")
            return
        game = GLOBAL_ROOMS[room_code]

    # Handle Joining Setup
    my_uid = st.session_state.user["uid"]
    player_ids = [p["uid"] for p in game["players"]]
    
    if my_uid not in player_ids:
        if game["status"] == "waiting" and len(game["players"]) < 4:
            with ROOM_LOCK:
                # Deal initial 13 cards out of shared multi-client deck
                initial_hand = [game["deck"].pop() for _ in range(13)] if len(game["deck"]) >= 13 else []
                game["players"].append({
                    "uid": my_uid,
                    "name": st.session_state.user["name"],
                    "hand": initial_hand
                })
                if len(game["discard_pile"]) == 0 and game["deck"]:
                    game["discard_pile"].append(game["deck"].pop())
            st.rerun()
        else:
            st.warning("This table is locked.")
            return

    # Grab fresh copies of our synced context
    players = game["players"]
    current_turn_player = players[game["turn_idx"]] if players else None
    my_data = next(p for p in players if p["uid"] == my_uid)

    # UI Table Header
    st.write(f"🏷️ **Your Room Invite Code:** `{room_code}` (Share this with friends)")
    
    # Roster display
    st.write("👥 **Players at Table:** " + " ➜ ".join([f"**{p['name']}** ({len(p['hand'])} cards)" for p in players]))
    
    # 1. THE FELT BOARD DISPLAY
    st.markdown('<div class="game-board">', unsafe_allow_html=True)
    if current_turn_player:
        st.markdown(f"<h3 style='text-align:center; color:#ffcc00;'>👉 Turn Owner: {current_turn_player['name']}</h3>", unsafe_allow_html=True)
    
    bc1, bc2 = st.columns(2)
    with bc1:
        st.markdown("<p style='text-align:center; margin:0;'>📦 DECK PILE</p>", unsafe_allow_html=True)
        render_card_back()
        st.markdown(f"<p style='text-align:center;'>{len(game['deck'])} left</p>", unsafe_allow_html=True)
        
        if current_turn_player and current_turn_player["uid"] == my_uid:
            if st.button("📥 Draw from Deck", use_container_width=True, key="draw_main"):
                with ROOM_LOCK:
                    if game["deck"]:
                        my_data["hand"].append(game["deck"].pop())
                st.rerun()

    with bc2:
        st.markdown("<p style='text-align:center; margin:0;'>🗑️ DISCARD PILE</p>", unsafe_allow_html=True)
        if game["discard_pile"]:
            render_card(game["discard_pile"][-1])
        else:
            st.write("Empty")
            
        if current_turn_player and current_turn_player["uid"] == my_uid:
            if st.button("♻️ Draw from Discard", use_container_width=True, key="draw_disc"):
                with ROOM_LOCK:
                    if game["discard_pile"]:
                        my_data["hand"].append(game["discard_pile"].pop())
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. LOCAL USER'S CARD SELECTION
    st.write("---")
    st.subheader("🃏 Your Dealt Hand")
    
    if my_data["hand"]:
        hand_cols = st.columns(len(my_data["hand"]))
        for idx, card in enumerate(my_data["hand"]):
            with hand_cols[idx]:
                is_selected = (st.session_state.selected_card_idx == idx)
                render_card(card, selected=is_selected)
                if st.button("📍 Select", key=f"sel_{idx}"):
                    st.session_state.selected_card_idx = idx
                    st.rerun()

    # Turn Execution Commands
    if current_turn_player and current_turn_player["uid"] == my_uid:
        st.info("⚡ It is your turn! Select a card from your hand and hit Discard below.")
        if st.button("🔥 Confirm Discard Action", use_container_width=True, type="primary"):
            if st.session_state.selected_card_idx is not None and st.session_state.selected_card_idx < len(my_data["hand"]):
                with ROOM_LOCK:
                    discarded_card = my_data["hand"].pop(st.session_state.selected_card_idx)
                    game["discard_pile"].append(discarded_card)
                    # Pass the turn index rotation across active users loop
                    game["turn_idx"] = (game["turn_idx"] + 1) % len(game["players"])
                    game["status"] = "playing" # Lock room layout
                st.session_state.selected_card_idx = None
                st.rerun()
            else:
                st.error("Please pick/click a card from your hand first above!")

def game_page():
    r_code = st.session_state.current_game_id
    
    col_header, col_exit = st.columns([3, 1])
    col_header.title("🎰 Elite Club Card Room")
    with col_exit:
        if st.button("🚪 Leave Table Room"):
            st.session_state.page = "lobby"
            st.session_state.current_game_id = None
            st.rerun()
            
    live_game_board(r_code)

# --- GLOBAL ROUTER NAVIGATION ---
def main():
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "lobby":
        lobby_page()
    elif st.session_state.page == "game":
        game_page()

if __name__ == "__main__":
    main()
