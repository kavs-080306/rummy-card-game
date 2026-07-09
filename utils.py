import streamlit as st
from datetime import datetime

# Custom CSS for better styling
def apply_custom_css():
    st.markdown("""
    <style>
        /* Main background */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0a4f0a !important;
        }
        
        .main {
            background-color: #0a4f0a !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1e293b;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 0.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            background-color: #ff6b35 !important;
            color: white !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(255, 107, 53, 0.4);
            background-color: #ff5722 !important;
        }
        
        /* Game cards */
        .game-card {
            background-color: rgba(255, 255, 255, 0.95);
            border: 2px solid #fff;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        .game-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
        }
        
        /* REALISTIC PLAYING CARDS */
        .playing-card {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            width: 110px;
            height: 160px;
            background-color: white;
            border: 3px solid #333;
            border-radius: 12px;
            padding: 10px;
            margin: 8px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            font-weight: bold;
            position: relative;
            font-family: 'Arial Black', sans-serif;
            text-align: center;
            user-select: none;
            vertical-align: top;
        }
        
        .playing-card:hover {
            transform: translateY(-25px) scale(1.1);
            box-shadow: 0 16px 32px rgba(0, 0, 0, 0.6);
        }
        
        .playing-card.selected {
            transform: translateY(-30px) scale(1.15);
            border-color: #FFD700;
            box-shadow: 0 0 0 5px rgba(255, 215, 0, 0.7), 0 16px 32px rgba(0, 0, 0, 0.6);
            background: linear-gradient(135deg, #fffacd 0%, #ffffe0 100%);
        }
        
        .card-corner {
            position: absolute;
            font-size: 16px;
            font-weight: bold;
            line-height: 1;
            width: 100%;
        }
        
        .card-top-left {
            top: 6px;
            left: 6px;
            text-align: left;
        }
        
        .card-bottom-right {
            bottom: 6px;
            right: 6px;
            text-align: right;
            transform: rotate(180deg);
        }
        
        .card-center {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .card-rank {
            font-size: 32px;
            font-weight: 900;
            line-height: 1;
        }
        
        .card-suit {
            font-size: 40px;
            line-height: 0.8;
        }
        
        /* Red cards */
        .card-red {
            color: #CC0000;
        }
        
        /* Black cards */
        .card-black {
            color: #000000;
        }
        
        .card-back {
            display: inline-flex;
            width: 110px;
            height: 160px;
            background: linear-gradient(45deg, #0c3d7d 0%, #1a5a96 50%, #0c3d7d 100%);
            border: 3px solid #051f3d;
            border-radius: 12px;
            margin: 8px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            align-items: center;
            justify-content: center;
            font-size: 40px;
            cursor: pointer;
            transition: all 0.3s ease;
            user-select: none;
            position: relative;
        }
        
        .card-back::before {
            content: '';
            position: absolute;
            width: 90%;
            height: 85%;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            pointer-events: none;
        }
        
        .card-back:hover {
            transform: translateY(-12px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.6);
        }
        
        /* GREEN FELT GAME BOARD */
        .game-board {
            background: linear-gradient(135deg, #0d5a0d 0%, #0a3f0a 50%, #064d06 100%);
            border: 5px solid #2d5a2d;
            border-radius: 16px;
            padding: 40px;
            margin: 20px 0;
            box-shadow: 
                inset 0 2px 8px rgba(0, 0, 0, 0.6),
                inset 0 -2px 8px rgba(255, 255, 255, 0.1),
                0 8px 16px rgba(0, 0, 0, 0.5);
            min-height: 500px;
            position: relative;
        }
        
        .game-board::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                repeating-linear-gradient(
                    90deg,
                    rgba(255,255,255,.02) 0px,
                    rgba(255,255,255,.02) 1px,
                    transparent 1px,
                    transparent 2px
                ),
                repeating-linear-gradient(
                    0deg,
                    rgba(255,255,255,.02) 0px,
                    rgba(255,255,255,.02) 1px,
                    transparent 1px,
                    transparent 2px
                );
            pointer-events: none;
        }
        
        .board-title {
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        
        .pile-container {
            background-color: rgba(0, 0, 0, 0.2);
            border: 3px dashed rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            min-height: 220px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            backdrop-filter: blur(5px);
        }
        
        .pile-label {
            color: #ffeb3b;
            font-weight: bold;
            margin-bottom: 15px;
            font-size: 16px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        
        /* Metrics */
        [data-testid="metric-container"] {
            background-color: rgba(255, 255, 255, 0.95);
            border: 2px solid #ffeb3b;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 0.5rem;
            background-color: rgba(255, 255, 255, 0.95) !important;
        }
        
        /* Hand area */
        .hand-container {
            background: linear-gradient(135deg, rgba(13, 90, 13, 0.8) 0%, rgba(10, 63, 10, 0.8) 100%);
            border: 3px solid #ffeb3b;
            border-radius: 16px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            min-height: 200px;
        }
        
        .hand-title {
            color: #ffeb3b;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }
        
        /* Player info cards */
        .player-info-card {
            background-color: rgba(255, 255, 255, 0.95);
            border: 3px solid #ffeb3b;
            border-radius: 12px;
            padding: 15px;
            margin: 8px 0;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .player-info-card.current-turn {
            background: linear-gradient(135deg, #fffacd 0%, #ffffe0 100%);
            border-color: #ff6b35;
            box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.3), 0 8px 16px rgba(0, 0, 0, 0.3);
        }
        
        .player-info-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)

def display_playing_card(card, selected=False, key=None):
    """Display a realistic playing card"""
    is_red = card.suit in ["♥", "♦"]
    suit_color = "card-red" if is_red else "card-black"
    
    st.markdown(f"""
    <div style="display: inline-block; vertical-align: top;">
        <div class="playing-card {suit_color} {'selected' if selected else ''}">
            <div class="card-corner card-top-left">{card.rank}<br>{card.suit}</div>
            <div class="card-center">
                <div class="card-rank">{card.rank}</div>
                <div class="card-suit">{card.suit}</div>
            </div>
            <div class="card-corner card-bottom-right">{card.rank}<br>{card.suit}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_card_back(deck_count=0):
    """Display card back"""
    st.markdown(f"""
    <div style="display: inline-block; text-align: center; vertical-align: top;">
        <div class="card-back">🎴</div>
        <p style="text-align: center; margin-top: 8px; font-size: 14px; color: #ffeb3b; font-weight: bold;">{deck_count} cards</p>
    </div>
    """, unsafe_allow_html=True)

def display_player_info(player, is_current=False):
    """Display player information card"""
    status = "🎯 Your Turn" if is_current else "⏳ Waiting"
    status_icon = "▶️" if is_current else "⏱️"
    
    st.markdown(f"""
    <div class="player-info-card {'current-turn' if is_current else ''}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: {'#ff6b35' if is_current else '#333'};"><strong>{status_icon} {player.name}</strong></h4>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">{status}</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; font-size: 18px; color: #ff6b35;"><strong>💰 {player.coins}</strong></p>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">🃏 {player.card_count()} cards</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_game_board():
    """Display game board"""
    st.markdown('<div class="game-board">', unsafe_allow_html=True)

def close_game_board():
    """Close game board"""
    st.markdown('</div>', unsafe_allow_html=True)

def display_pile_area(title="", count=0):
    """Display pile area for draw/discard"""
    st.markdown(f"""
    <div class="pile-container">
        <div class="pile-label">{title}</div>
    """, unsafe_allow_html=True)

def close_pile_area():
    """Close pile area"""
    st.markdown('</div>', unsafe_allow_html=True)

def format_game_time(created_at):
    """Format game creation time"""
    if isinstance(created_at, str):
        return created_at
    delta = datetime.now() - created_at
    if delta.seconds < 60:
        return f"{delta.seconds}s ago"
    elif delta.seconds < 3600:
        return f"{delta.seconds // 60}m ago"
    else:
        return f"{delta.seconds // 3600}h ago"

# Apply custom CSS globally
apply_custom_css()
