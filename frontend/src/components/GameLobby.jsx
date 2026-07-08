import { useState, useEffect } from 'react';
import axios from 'axios';
import GameRoom from './GameRoom';

export default function GameLobby({ userId, coins }) {
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [loading, setLoading] = useState(true);
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  useEffect(() => {
    fetchGames();
    const interval = setInterval(fetchGames, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchGames = async () => {
    try {
      const response = await axios.get(`${backendUrl}/api/games`);
      setGames(response.data.games || []);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch games:', error);
      setLoading(false);
    }
  };

  const createGame = async () => {
    if (coins < 10) {
      alert('You need at least 10 coins to create a game');
      return;
    }

    try {
      const response = await axios.post(
        `${backendUrl}/api/create-game`,
        {
          creatorId: userId,
          entryFee: 10,
        }
      );
      setSelectedGame(response.data.gameId);
    } catch (error) {
      console.error('Failed to create game:', error);
      alert('Failed to create game');
    }
  };

  const joinGame = async (gameId) => {
    if (coins < 10) {
      alert('You need at least 10 coins to join a game');
      return;
    }

    try {
      await axios.post(`${backendUrl}/api/join-game`, {
        gameId,
        playerId: userId,
      });
      setSelectedGame(gameId);
    } catch (error) {
      console.error('Failed to join game:', error);
      alert('Failed to join game');
    }
  };

  if (selectedGame) {
    return <GameRoom gameId={selectedGame} userId={userId} onExit={() => setSelectedGame(null)} />;
  }

  if (loading) {
    return <div className="text-center text-white">Loading games...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex gap-4">
        <button
          onClick={createGame}
          className="btn btn-success text-lg px-8 py-3"
          disabled={coins < 10}
        >
          ➕ Create Game (10 coins)
        </button>
        <button
          onClick={fetchGames}
          className="btn btn-primary text-lg px-8 py-3"
        >
          🔄 Refresh
        </button>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4">Available Games</h2>
        {games.length === 0 ? (
          <div className="text-center py-12 text-gray-400">
            <p className="text-xl">No games available. Create one to get started!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {games.map((game) => (
              <div
                key={game.gameId}
                className="bg-slate-800 border border-slate-700 p-6 rounded-lg hover:border-purple-500 transition"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-bold">Game #{game.gameId.slice(0, 8)}</h3>
                    <p className="text-gray-400 text-sm">Entry: {game.entryFee} coins</p>
                  </div>
                  <span className={`px-3 py-1 rounded text-sm font-semibold ${
                    game.status === 'waiting' ? 'bg-yellow-600' : 'bg-blue-600'
                  }`}>
                    {game.status}
                  </span>
                </div>

                <div className="mb-4 space-y-2">
                  <p className="text-sm text-gray-300">
                    Players: {game.players?.length || 0}/6
                  </p>
                  <p className="text-sm text-gray-300">
                    Prize Pool: {(game.entryFee * (game.players?.length || 1))} coins
                  </p>
                </div>

                <button
                  onClick={() => joinGame(game.gameId)}
                  disabled={game.status !== 'waiting' || coins < game.entryFee}
                  className="w-full btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Join Game
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
