import { useState, useEffect } from 'react';
import axios from 'axios';
import PlayingCard from './PlayingCard';

export default function GameRoom({ gameId, userId, onExit }) {
  const [gameState, setGameState] = useState(null);
  const [selectedCards, setSelectedCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  useEffect(() => {
    fetchGameState();
    const interval = setInterval(fetchGameState, 1000);
    return () => clearInterval(interval);
  }, [gameId]);

  const fetchGameState = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/game/${gameId}`);
      setGameState(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch game state:', error);
    }
  };

  const selectCard = (index) => {
    if (selectedCards.includes(index)) {
      setSelectedCards(selectedCards.filter(i => i !== index));
    } else {
      setSelectedCards([...selectedCards, index]);
    }
  };

  const playCards = async () => {
    if (selectedCards.length === 0) return;

    try {
      await axios.post(`${backendUrl}/api/game/${gameId}/play`, {
        playerId: userId,
        cardIndices: selectedCards,
      });
      setSelectedCards([]);
      fetchGameState();
    } catch (error) {
      console.error('Failed to play cards:', error);
    }
  };

  const drawCard = async () => {
    try {
      await axios.post(`${backendUrl}/api/game/${gameId}/draw`, {
        playerId: userId,
      });
      fetchGameState();
    } catch (error) {
      console.error('Failed to draw card:', error);
    }
  };

  const discardCard = async (cardIndex) => {
    try {
      await axios.post(`${backendUrl}/api/game/${gameId}/discard`, {
        playerId: userId,
        cardIndex,
      });
      setSelectedCards([]);
      fetchGameState();
    } catch (error) {
      console.error('Failed to discard card:', error);
    }
  };

  if (loading) {
    return <div className="text-center text-white">Loading game...</div>;
  }

  if (!gameState) {
    return <div className="text-center text-white">Game not found</div>;
  }

  const currentPlayer = gameState.players?.[gameState.currentPlayerIndex];
  const isYourTurn = currentPlayer?.id === userId;
  const myHand = gameState.players?.find(p => p.id === userId)?.hand || [];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Game #{gameId.slice(0, 8)}</h2>
        <button
          onClick={onExit}
          className="btn btn-danger"
        >
          Exit Game
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-green-900 rounded-lg p-8 min-h-96 border-4 border-green-700 flex flex-col items-center justify-center">
            <div className="space-y-4 text-center">
              <h3 className="text-2xl font-bold">
                {isYourTurn ? "🎯 Your Turn!" : `⏳ ${currentPlayer?.name}'s Turn`}
              </h3>
              
              <div className="flex justify-center gap-4">
                <div className="space-y-2">
                  <p className="text-sm text-gray-300">Draw Pile</p>
                  <button
                    onClick={drawCard}
                    disabled={!isYourTurn}
                    className={`w-24 h-32 border-2 border-dashed rounded-lg font-bold ${
                      isYourTurn ? 'bg-white text-black cursor-pointer hover:bg-gray-200' : 'bg-gray-400 opacity-50'
                    }`}
                  >
                    📦 {gameState.deckRemaining || 0}
                  </button>
                </div>

                <div className="space-y-2">
                  <p className="text-sm text-gray-300">Discard Pile</p>
                  {gameState.discardPile?.length > 0 ? (
                    <div className="w-24">
                      <PlayingCard
                        rank={gameState.discardPile[gameState.discardPile.length - 1].rank}
                        suit={gameState.discardPile[gameState.discardPile.length - 1].suit}
                        width={96}
                      />
                    </div>
                  ) : (
                    <div className="w-24 h-32 border-2 border-dashed rounded-lg bg-gray-700 flex items-center justify-center">
                      Empty
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-xl font-bold">Your Hand ({myHand.length} cards)</h3>
            <div className="flex flex-wrap gap-3 justify-center p-4 bg-slate-800 rounded-lg min-h-40">
              {myHand.map((card, index) => (
                <div
                  key={index}
                  onClick={() => selectCard(index)}
                  className={`cursor-pointer transition transform hover:scale-110 ${
                    selectedCards.includes(index) ? 'ring-4 ring-yellow-400 -translate-y-4' : ''
                  }`}
                >
                  <PlayingCard rank={card.rank} suit={card.suit} width={64} />
                </div>
              ))}
            </div>
          </div>

          {selectedCards.length > 0 && (
            <div className="flex gap-4">
              <button
                onClick={playCards}
                disabled={!isYourTurn}
                className="btn btn-success flex-1 disabled:opacity-50"
              >
                ✅ Play {selectedCards.length} card(s)
              </button>
              <button
                onClick={() => discardCard(selectedCards[0])}
                disabled={!isYourTurn || selectedCards.length !== 1}
                className="btn btn-primary flex-1 disabled:opacity-50"
              >
                💨 Discard
              </button>
            </div>
          )}
        </div>

        <div className="space-y-4">
          <h3 className="text-xl font-bold">Players ({gameState.players?.length || 0})</h3>
          <div className="space-y-3">
            {gameState.players?.map((player, index) => (
              <div
                key={player.id}
                className={`p-4 rounded-lg border-2 ${
                  index === gameState.currentPlayerIndex
                    ? 'bg-purple-900 border-purple-500'
                    : 'bg-slate-800 border-slate-700'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-semibold">{player.name}</span>
                  <span className="text-sm text-gray-300">{player.hand?.length || 0} cards</span>
                </div>
                <p className="text-sm text-yellow-400 mt-1">💰 {player.coins}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
