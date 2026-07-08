import { useState, useEffect } from 'react';
import { auth, db } from '../config/firebase';
import { doc, onSnapshot } from 'firebase/firestore';
import GameLobby from './GameLobby';

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [coins, setCoins] = useState(0);
  const [activeTab, setActiveTab] = useState('lobby');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((currentUser) => {
      if (currentUser) {
        setUser(currentUser);

        const userRef = doc(db, 'users', currentUser.uid);
        onSnapshot(userRef, (doc) => {
          if (doc.exists()) {
            setCoins(doc.data()?.coins || 0);
          }
          setLoading(false);
        });
      }
    });

    return unsubscribe;
  }, []);

  const handleLogout = () => {
    auth.signOut();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-2xl text-white">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <nav className="bg-slate-800 border-b border-slate-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold">🎴 Rummy</h1>
          
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-2 bg-slate-700 px-4 py-2 rounded-lg">
              <span className="text-yellow-400 text-xl">💰</span>
              <span className="text-2xl font-bold">{coins}</span>
            </div>

            <div className="flex items-center gap-3">
              <img 
                src={user?.photoURL} 
                alt={user?.displayName}
                className="w-10 h-10 rounded-full"
              />
              <span className="text-gray-300">{user?.displayName}</span>
            </div>

            <button
              onClick={handleLogout}
              className="btn btn-danger"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setActiveTab('lobby')}
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              activeTab === 'lobby'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-700 text-gray-300 hover:bg-slate-600'
            }`}
          >
            🎮 Game Lobby
          </button>
          <button
            onClick={() => setActiveTab('stats')}
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              activeTab === 'stats'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-700 text-gray-300 hover:bg-slate-600'
            }`}
          >
            📊 Statistics
          </button>
        </div>

        {activeTab === 'lobby' && <GameLobby userId={user?.uid} coins={coins} />}
        {activeTab === 'stats' && <Statistics user={user} />}
      </div>
    </div>
  );
}

function Statistics({ user }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
        <p className="text-gray-400">Games Played</p>
        <p className="text-4xl font-bold text-purple-400">0</p>
      </div>
      <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
        <p className="text-gray-400">Games Won</p>
        <p className="text-4xl font-bold text-green-400">0</p>
      </div>
      <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
        <p className="text-gray-400">Win Rate</p>
        <p className="text-4xl font-bold text-blue-400">0%</p>
      </div>
    </div>
  );
}
