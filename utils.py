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
        
        /* Playing cards */
        .playing-card {
            display: inline-block;
            width: 80px;
            height: 120px;
            background-color: white;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin: 0.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .playing-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        .playing-card.selected {
            border-color: #fbbf24;
            box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.5);
            transform: translateY(-12px);
        }
        
        /* Metrics */
        [data-testid="metric-container"] {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 0.5rem;
            padding: 1.5rem;
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

def display_playing_card(card, selected=False, key=None):
    """Display a playing card"""
    suit_color = "red" if card.suit in ["♥", "♦"] else "black"
    
    st.markdown(f"""
    <div style="display: inline-block; margin: 5px;">
        <div style="
            width: 80px;
            height: 120px;
            background-color: white;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: {suit_color};
            {'border-color: #fbbf24; box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.5);' if selected else ''}
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        ">
            <div>
                <div style="font-size: 1.2rem;">{card.rank}</div>
                <div style="font-size: 1.5rem;">{card.suit}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_player_info(player, is_current=False):
    """Display player information card"""
    status = "🎯 Current Turn" if is_current else "⏳ Waiting"
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**{player.name}** {status}")
    with col2:
        st.write(f"💰 {player.coins}")
    with col3:
        st.write(f"🃏 {player.card_count()}")

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
apply_custom_CSS()
