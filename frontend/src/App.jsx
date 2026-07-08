import { useState, useEffect } from 'react';
import { auth } from './config/firebase';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-slate-900">
        <div className="text-2xl text-white">Loading...</div>
      </div>
    );
  }

  return user ? <Dashboard /> : <Login />;
}
