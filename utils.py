import streamlit as st
from datetime import datetime

# Custom CSS for better styling
def apply_custom_css():
    st.markdown("""
    <style>
        /* Main background */
        .main {
            background-color: #0f172a;
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
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Cards */
        .game-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
        }
        
        .game-card:hover {
            border-color: #6366f1;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
        }
        
        /* Playing cards - REALISTIC STYLE */
        .playing-card {
            display: inline-block;
            width: 100px;
            height: 140px;
            background-color: white;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 8px;
            margin: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            font-weight: bold;
            position: relative;
            font-family: 'Arial Black', sans-serif;
            text-align: center;
            user-select: none;
        }
        
        .playing-card:hover {
            transform: translateY(-15px) scale(1.05);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        }
        
        .playing-card.selected {
            transform: translateY(-20px) scale(1.08);
            border-color: #fbbf24;
            box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.6), 0 12px 24px rgba(0, 0, 0, 0.4);
            background: linear-gradient(135deg, #fffacd 0%, white 100%);
        }
        
        .card-top {
            position: absolute;
            top: 4px;
            left: 4px;
            font-size: 14px;
            line-height: 1;
        }
        
        .card-rank {
            font-size: 24px;
            margin: 20px 0 5px 0;
        }
        
        .card-suit {
            font-size: 28px;
            margin: 5px 0;
        }
        
        .card-bottom {
            position: absolute;
            bottom: 4px;
            right: 4px;
            font-size: 14px;
            transform: rotate(180deg);
            line-height: 1;
        }
        
        /* Red cards */
        .card-red {
            color: #e63946;
        }
        
        /* Black cards */
        .card-black {
            color: #1a1a1a;
        }
        
        .card-back {
            display: inline-flex;
            width: 100px;
            height: 140px;
            background: linear-gradient(45deg, #1e3a8a 0%, #1e40af 50%, #1e3a8a 100%);
            border: 2px solid #0c1442;
            border-radius: 8px;
            margin: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            align-items: center;
            justify-content: center;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            user-select: none;
        }
        
        .card-back:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        }
        
        /* Game board */
        .game-board {
            background: linear-gradient(135deg, #1a472a 0%, #0f2818 100%);
            border: 3px solid #4a5d23;
            border-radius: 12px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5), 0 4px 8px rgba(0, 0, 0, 0.3);
            min-height: 400px;
        }
        
        .card-area {
            background-color: rgba(0, 0, 0, 0.2);
            border: 2px dashed #4a5d23;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            min-height: 180px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        /* Metrics */
        [data-testid="metric-container"] {
            background-color: #1e293b;
            border: 2px solid #6366f1;
            border-radius: 0.5rem;
            padding: 1.5rem;
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 0.5rem;
        }
        
        /* Hand area */
        .hand-container {
            background-color: rgba(30, 41, 59, 0.8);
            border: 2px solid #4f46e5;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)

def display_playing_card(card, selected=False, key=None):
    """Display a realistic playing card"""
    is_red = card.suit in ["♥", "♦"]
    suit_color = "card-red" if is_red else "card-black"
    
    st.markdown(f"""
    <div style="display: inline-block;">
        <div class="playing-card {suit_color} {'selected' if selected else ''}">
            <div class="card-top">{card.rank}<br>{card.suit}</div>
            <div class="card-rank">{card.rank}</div>
            <div class="card-suit">{card.suit}</div>
            <div class="card-bottom">{card.rank}<br>{card.suit}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_card_back(deck_count=0):
    """Display card back"""
    st.markdown(f"""
    <div style="display: inline-block; text-align: center;">
        <div class="card-back">🎴</div>
        <p style="text-align: center; margin-top: 5px; font-size: 12px; color: #9ca3af;">{deck_count}</p>
    </div>
    """, unsafe_allow_html=True)

def display_player_info(player, is_current=False):
    """Display player information card"""
    status = "🎯 Current Turn" if is_current else "⏳ Waiting"
    bg_color = "rgba(99, 102, 241, 0.15)" if is_current else "rgba(51, 65, 85, 0.5)"
    border_color = "#6366f1" if is_current else "#475569"
    
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        border: 2px solid {border_color};
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        transition: all 0.3s ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #fff;">{player.name}</h4>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #9ca3af;">{status}</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; font-size: 16px; color: #fbbf24;">💰 {player.coins}</p>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #9ca3af;">🃏 {player.card_count()} cards</p>
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

def display_card_area(title=""):
    """Display card area"""
    st.markdown(f'<div class="card-area">', unsafe_allow_html=True)

def close_card_area():
    """Close card area"""
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
