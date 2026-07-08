# 🎴 Card UI Reference Guide

## Quick Visual Guide - What You Get

### 1. Playing Card Example

```html
┌────────────────────────┐
│ A   ♥                  │  ← Rank & Suit (Top Left)
│                        │
│                        │
│        A               │  ← Large Rank (Center)
│        ♥               │  ← Large Suit (Center)
│                        │
│                        │
│                   A  ♥ │  ← Rank & Suit (Bottom Right - Flipped)
└────────────────────────┘

Colors:
- Hearts ♥ & Diamonds ♦ = Red (#e63946)
- Spades ♠ & Clubs ♣ = Black (#1a1a1a)

Size: 100px wide × 140px tall
Corners: Rounded (8px)
Shadow: 3D effect
```

### 2. Card Interactions

#### Hover Effect:
```
Resting:
[A ♥]

Hover (mouse over):
    [A ♥]   ← Card lifts up 15px
    
Shadow intensifies
Card slightly enlarges (1.05x)
```

#### Selection Effect:
```
Not Selected:        Selected:
[A ♥]               ╔═══════════╗
                    ║  [A ♥]   ║ ← Golden glow
                    ║ Highlighted║
                    ╚═══════════╝
                    Moves up 20px
                    Scales 1.08x
```

### 3. Card Back (Deck)

```
┌────────────────────┐
│                    │
│        🎴          │  ← Blue gradient pattern
│        48          │  ← Number of cards
│                    │
└────────────────────┘

Color: Blue gradient (#1e3a8a → #1e40af)
Border: Dark blue
Used for: Draw pile
```

### 4. Game Board

```
┌─ GREEN FELT TABLE ─────────────────────┐
│                                        │
│  📦 DRAW PILE        💨 DISCARD PILE  │
│  [DECK BACK]         [A ♥]            │
│  48 cards            Last Card         │
│                                        │
└────────────────────────────────────────┘

Background: Green felt (#1a472a)
Border: Wood color (#4a5d23)
```

### 5. Player Hand

```
┌─── YOUR HAND ─────────────────────────────────┐
│                                               │
│  [A♥] [K♠] [Q♦] [J♣] [10♥] [9♠] [8♦]       │
│  [7♣] [6♥] [5♠] [4♦] [3♣] [2♥]             │
│                                               │
└─── Blue border container ────────────────────┘

Layout: Scrollable row
Cards wrap automatically
Interactive: Click to select
```

### 6. Players Display

```
Current Player:
┌──────────────────────────┐
│ Alice 🎯 Current Turn   │ ← Blue border
│ 💰 850 coins            │ ← Yellow coin amount
│ 🃏 12 cards            │ ← Gray card count
└──────────────────────────┘

Waiting Player:
┌──────────────────────────┐
│ Bob ⏳ Waiting          │ ← Gray border
│ 💰 950 coins            │
│ 🃏 13 cards            │
└──────────────────────────┘
```

---

## CSS Classes Reference

### Card Styling

```css
/* Base card styling */
.playing-card {
    width: 100px;
    height: 140px;
    background-color: white;
    border: 2px solid #333;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

/* Red cards (♥♦) */
.card-red {
    color: #e63946;
}

/* Black cards (♠♣) */
.card-black {
    color: #1a1a1a;
}

/* Selected state */
.playing-card.selected {
    border-color: #fbbf24;
    box-shadow: 0 0 0 4px rgba(251,191,36,0.6);
    transform: translateY(-20px) scale(1.08);
}
```

### Board Styling

```css
/* Game board container */
.game-board {
    background: linear-gradient(135deg, #1a472a 0%, #0f2818 100%);
    border: 3px solid #4a5d23;
    border-radius: 12px;
}

/* Card area containers */
.card-area {
    background-color: rgba(0,0,0,0.2);
    border: 2px dashed #4a5d23;
    border-radius: 8px;
}

/* Hand container */
.hand-container {
    background-color: rgba(30,41,59,0.8);
    border: 2px solid #4f46e5;
    border-radius: 12px;
}
```

---

## Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| **Red** | #e63946 | Hearts ♥, Diamonds ♦ |
| **Black** | #1a1a1a | Spades ♠, Clubs ♣ |
| **White** | #ffffff | Card face |
| **Green** | #1a472a | Game board bg |
| **Gold** | #fbbf24 | Selection highlight |
| **Blue** | #6366f1 | Current player |
| **Dark** | #0f172a | Main background |
| **Secondary** | #1e293b | UI backgrounds |

---

## Animation Timings

| Animation | Duration | Effect |
|-----------|----------|--------|
| Hover lift | 300ms | Card moves up |
| Scale | 300ms | Card enlarges |
| Shadow | 300ms | Intensifies |
| Selection | 300ms | Glow appears |

---

## Responsive Breakpoints

### Desktop (1920x1080+)
- Cards: Full size
- Layout: 7 columns
- Spacing: Generous

### Tablet (768x1024)
- Cards: Full size
- Layout: 4 columns
- Spacing: Normal

### Mobile (375x812)
- Cards: Full size
- Layout: 3 columns
- Spacing: Compact

---

## Card Structure (HTML)

```html
<div class="playing-card card-red">
    <div class="card-top">
        A<br>♥
    </div>
    <div class="card-rank">A</div>
    <div class="card-suit">♥</div>
    <div class="card-bottom">
        A<br>♥
    </div>
</div>
```

---

## Usage Examples

### Display a Card:
```python
from utils import display_playing_card
from game_logic import Card

card = Card("♥", "A")
display_playing_card(card, selected=False)
```

### Display Deck Back:
```python
from utils import display_card_back

display_card_back(48)  # Shows back with 48 cards remaining
```

### Display Player Info:
```python
from utils import display_player_info

display_player_info(player, is_current=True)
```

---

## Customization Tips

### Change Card Size:
In `utils.py`, modify:
```css
.playing-card {
    width: 120px;    /* ← Change from 100px */
    height: 168px;   /* ← Change from 140px */
}
```

### Change Colors:
```css
/* For red cards */
.card-red { color: #ff0000; }

/* For game board */
.game-board { background: linear-gradient(...); }

/* For selection */
.playing-card.selected { border-color: #00ff00; }
```

### Change Animations:
```css
.playing-card {
    transition: all 0.5s ease;  /* ← Slower animation */
}

.playing-card:hover {
    transform: translateY(-25px);  /* ← More lift */
}
```

---

## Browser Compatibility

| Browser | Support |
|---------|---------|
| Chrome | ✅ Full |
| Firefox | ✅ Full |
| Safari | ✅ Full |
| Edge | ✅ Full |
| Mobile | ✅ Full |

---

## Performance Notes

- ✅ Pure CSS (no JavaScript)
- ✅ Uses GPU acceleration
- ✅ 60fps animations
- ✅ No image loading
- ✅ Lightweight HTML

---

## Testing the UI

### Local Testing:
```bash
streamlit run app.py
```

### Test Actions:
1. **Hover cards** - See lift effect
2. **Click card** - See selection glow
3. **Resize window** - Check responsiveness
4. **Try on mobile** - Test touch interactions

---

**Version**: 1.0  
**Last Updated**: 2026-07-08  
**Status**: Production Ready ✅
