import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
import os

akki = Flask(__name__)
CORS(akki)

# MongoDB Setup
client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

# --- ALL-IN-ONE SEARCH ENGINE ---
@akki.route('/api/search-all', methods=['GET'])
def search_all():
    query = request.args.get('q', '')
    if not query: return jsonify({"error": "Empty"})
    try:
        # Chrome suggestions
        web_res = requests.get(f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}").json()
        # YouTube dynamic search embed
        yt_search = f"https://www.youtube.com/embed?listType=search&list={query}"
        return jsonify({"web": web_res[1][:5], "yt_link": yt_search})
    except:
        return jsonify({"error": "Server Busy"})

# --- REELS FETCH LOGIC (With Link Fixer) ---
@akki.route('/api/reels', methods=['GET'])
def get_reels():
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: 
        r['_id'] = str(r['_id'])
        # Automatic Link Conversion (Shorts/Watch -> Embed)
        url = r.get('video_url', '')
        if 'shorts/' in url: r['video_url'] = url.replace('shorts/', 'embed/')
        elif 'watch?v=' in url: r['video_url'] = url.replace('watch?v=', 'embed/')
    return jsonify(reels)

# --- UPLOAD API ---
@akki.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    if data.get('video_url'):
        reels_col.insert_one(data)
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

# --- RENDER PORT FIX ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    akki.run(host='0.0.0.0', port=port)
    
