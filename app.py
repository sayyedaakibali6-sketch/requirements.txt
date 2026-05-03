from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo

# App ka naam akki set kar diya
akki = Flask(__name__)
CORS(akki)

# Database Connection
MONGO_URI = "mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.fitnessDB
reels_col = db.reels

@akki.route('/')
def home():
    return "Akki Instagram Engine is Running! 🚀"

@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        reels_col.insert_one({
            "video_url": data.get("video_url"),
            "caption": data.get("caption", ""),
            "likes": 0
        })
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    try:
        reels = list(reels_col.find().sort('_id', -1))
        for r in reels:
            r['_id'] = str(r['_id'])
        return jsonify(reels), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    akki.run(host='0.0.0.0', port=10000)
    
