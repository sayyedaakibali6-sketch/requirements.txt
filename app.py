from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo

app = Flask(__createdgdonakki__)
CORS(app)

# Connection string ekdum sahi format mein
MONGO_URL = "mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URL)
db = client.fitnessDB
reels_col = db.reels 

@app.route('/')
def home():
    return "Instagram Engine is Running! 🚀"

@app.route('/api/upload', methods=['POST'])
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

@app.route('/api/reels', methods=['GET'])
def get_reels():
    try:
        reels = list(reels_col.find().sort('_id', -1))
        for r in reels:
            r['_id'] = str(r['_id'])
        return jsonify(reels), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
    
