import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth, db } from '../config/firebase';
import { doc, setDoc, getDoc } from 'firebase/firestore';

export default function Login() {
  const handleGoogleLogin = async () => {
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);
      const user = result.user;

      const userRef = doc(db, 'users', user.uid);
      const userDoc = await getDoc(userRef);

      if (!userDoc.exists()) {
        await setDoc(userRef, {
          name: user.displayName,
          email: user.email,
          photoURL: user.photoURL,
          coins: 1000,
          gamesPlayed: 0,
          gamesWon: 0,
          createdAt: new Date(),
        });
      }
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-slate-900 to-blue-900 flex items-center justify-center p-4">
      <div className="text-center">
        <h1 className="text-6xl font-bold mb-4 text-white drop-shadow-lg">🎴 Rummy</h1>
        <p className="text-xl text-gray-300 mb-8">Play with friends. Earn coins. Have fun!</p>
        
        <button
          onClick={handleGoogleLogin}
          className="btn btn-primary text-lg px-8 py-4 shadow-2xl hover:shadow-xl transform hover:scale-105 transition-all"
        >
          🔐 Sign in with Google
        </button>

        <p className="text-gray-400 mt-12 text-sm">
          You'll receive 1000 free coins on first login
        </p>
      </div>
    </div>
  );
}
