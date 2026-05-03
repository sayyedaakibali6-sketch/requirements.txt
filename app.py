from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId

# App ka naam akki set kar diya jaisa tumne kaha tha
akki = Flask(__name__)
CORS(akki)

# Database Connection (Sari Keys Included)
MONGO_URI = "mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client.fitnessDB
reels_col = db.reels

@akki.route('/')
def home():
    return "Akki YouTube Shorts Engine Live! 🚀"

@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        raw_url = data.get("video_url")
        
        # YouTube Shorts link ko embed HD mein badalne ka logic
        if "shorts/" in raw_url:
            v_id = raw_url.split("shorts/")[1].split("?")[0]
            # Full screen aur auto-play ke liye playsinline=1 aur baaki params add kiye hain
            final_url = f"https://www.youtube.com/embed/{v_id}?autoplay=1&controls=0&rel=0&modestbranding=1&playsinline=1&iv_load_policy=3&enablejsapi=1"
        elif "instagram.com/reels/" in raw_url or "instagram.com/p/" in raw_url:
            final_url = raw_url.split("?")[0] + "embed/captioned"
        else:
            final_url = raw_url # Direct MP4 ya TikTok ke liye

        reels_col.insert_one({
            "video_url": final_url, 
            "caption": data.get("caption", "No Caption"), 
            "type": "embed"
        })
        return jsonify({"success": True}), 200
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

@akki.route('/api/delete/<id>', methods=['DELETE'])
def delete_reel(id):
    try:
        reels_col.delete_one({"_id": ObjectId(id)})
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    akki.run(host='0.0.0.0', port=10000)
    
