import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.getenv("FRONTEND_URL", "http://localhost:5173")}})

from app.routes import game_routes, user_routes

app.register_blueprint(game_routes.bp)
app.register_blueprint(user_routes.bp)

@app.route('/api/health', methods=['GET'])
def health():
    return {"status": "Backend is running!", "version": "1.0.0"}, 200

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False), port=5000, host='0.0.0.0')
