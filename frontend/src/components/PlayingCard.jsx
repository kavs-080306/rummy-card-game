export default function PlayingCard({ rank, suit, width = 80 }) {
  const isRed = suit === '♥' || suit === '♦';
  const color = isRed ? 'text-red-600' : 'text-black';

  return (
    <div
      className={`card ${isRed ? 'red' : 'black'}`}
      style={{ width: `${width}px` }}
    >
      <div className="text-center">
        <div className={`text-lg font-bold ${color}`}>{rank}</div>
        <div className={`text-2xl ${color}`}>{suit}</div>
      </div>
    </div>
  );
}
