import streamlit as st
import random
from datetime import datetime
import threading

# --- GLOBAL STORAGE FOR MULTI-USER SYNC (PERSISTENT CROSS-SESSION) ---
if "_GLOBAL_ROOMS" not in globals():
    globals()["_GLOBAL_ROOMS"] = {}
if "_GLOBAL_USERS" not in globals():
    # In-memory dictionary holding unique user accounts: {username: {"password": pwd, "coins": 5000}}
    globals()["_GLOBAL_USERS"] = {}
if "_ROOM_LOCK" not in globals():
    globals()["_ROOM_LOCK"] = threading.Lock()

GLOBAL_ROOMS = globals()["_GLOBAL_ROOMS"]
GLOBAL_USERS = globals()["_GLOBAL_USERS"]
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
    st.title("🎴 Global Rummy Lounge Login")
    st.subheader("Register or login to track your chip stack across tables!")
    
    tab_in, tab_up = st.tabs(["🔐 SIGN IN", "📝 CREATE ACCOUNT"])
    
    with tab_in:
        with st.form("signin_form"):
            username = st.text_input("Username", key="login_user", placeholder="Enter username").strip()
            password = st.text_input("Password", type="password", key="login_pass")
            submit_in = st.form_submit_button("Sign In")
            
            if submit_in:
                if not username or not password:
                    st.error("Please fill in all credential fields.")
                else:
                    with ROOM_LOCK:
                        if username in GLOBAL_USERS and GLOBAL_USERS[username]["password"] == password:
                            st.session_state.user = {
                                "uid": username,
                                "name": username,
                                "coins": GLOBAL_USERS[username]["coins"]
                            }
                            st.session_state.page = "lobby"
                            st.rerun()
                        else:
                            st.error("Invalid username or password match configuration.")
                            
    with tab_up:
        st.info("🎁 Sign up today to receive a dynamic credit of 5,000 free starting chips!")
        with st.form("signup_form"):
            new_username = st.text_input("Choose Username", key="reg_user", placeholder="Must be unique").strip()
            new_password = st.text_input("Choose Password", type="password", key="reg_pass")
            submit_up = st.form_submit_button("Create Account & Claim Welcome Bonus")
            
            if submit_up:
                if not new_username or not new_password:
                    st.error("Fields cannot be left empty.")
                else:
                    with ROOM_LOCK:
                        if new_username in GLOBAL_USERS:
                            st.error("⚠️ Username already taken! Please pick another configuration.")
                        else:
                            # FIXED: Save to the global registry FIRST so lobby_page can read it safely
                            GLOBAL_USERS[new_username] = {
                                "password": new_password,
                                "coins": 5000
                            }
                            st.session_state.user = {
                                "uid": new_username,
                                "name": new_username,
                                "coins": 5000
                            }
                            st.session_state.page = "lobby"
                            st.success("Account created successfully!")
                            st.rerun()
def lobby_page():
    # Sync visual metrics from the global multi-session cache layer
    with ROOM_LOCK:
        st.session_state.user["coins"] = GLOBAL_USERS[st.session_state.user["uid"]]["coins"]
        
    c_head, c_bal, c_out = st.columns([2, 1, 1])
    c_head.markdown(f"### 🏟️ Welcome back, **{st.session_state.user['name']}**")
    c_bal.metric("💰 Chip Balance", f"{st.session_state.user['coins']} coins")
    with c_out:
        if st.button("🚪 Logout Account", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()
            
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Available Multi-Friend Tables")
    with col2:
        if st.button("➕ CREATE TABLE (Cost: 100)", use_container_width=True):
            if st.session_state.user["coins"] < 100:
                st.error("Insufficient coins to start a table!")
            else:
                with ROOM_LOCK:
                    room_code = f"ROOM_{random.randint(1000, 9999)}"
                    # Deduct cost from global account stack
                    GLOBAL_USERS[st.session_state.user["uid"]]["coins"] -= 100
                    GLOBAL_ROOMS[room_code] = {
                        "id": room_code,
                        "players": [],  
                        "deck": generate_deck(),
                        "discard_pile": [],
                        "turn_idx": 0,
                        "status": "waiting"
                    }
                st.session_state.current_game_id = room_code
                st.session_state.page = "game"
                st.rerun()

    st.write("---")
    
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
        st.info("No active tables right now. Create one and tell your friend the code!")

@st.fragment(run_every=2.5)
def live_game_board(room_code):
    with ROOM_LOCK:
        if room_code not in GLOBAL_ROOMS:
            st.error("Room dissolved!")
            return
        game = GLOBAL_ROOMS[room_code]

    my_uid = st.session_state.user["uid"]
    player_ids = [p["uid"] for p in game["players"]]
    
    if my_uid not in player_ids:
        if game["status"] == "waiting" and len(game["players"]) < 4:
            with ROOM_LOCK:
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

    players = game["players"]
    current_turn_player = players[game["turn_idx"]] if players else None
    my_data = next(p for p in players if p["uid"] == my_uid)

    st.write(f"🏷️ **Your Room Invite Code:** `{room_code}` (Share this with friends)")
    st.write("👥 **Players at Table:** " + " ➜ ".join([f"**{p['name']}** ({len(p['hand'])} cards)" for p in players]))
    
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

    if current_turn_player and current_turn_player["uid"] == my_uid:
        st.info("⚡ It is your turn! Select a card from your hand and hit Discard below.")
        if st.button("🔥 Confirm Discard Action", use_container_width=True, type="primary"):
            if st.session_state.selected_card_idx is not None and st.session_state.selected_card_idx < len(my_data["hand"]):
                with ROOM_LOCK:
                    discarded_card = my_data["hand"].pop(st.session_state.selected_card_idx)
                    game["discard_pile"].append(discarded_card)
                    game["turn_idx"] = (game["turn_idx"] + 1) % len(game["players"])
                    game["status"] = "playing"
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
