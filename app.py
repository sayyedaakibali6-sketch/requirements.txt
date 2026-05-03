import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
import os

akki = Flask(__name__)
CORS(akki)

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels
live_col = db.live_status

# --- ADVANCED WORLD + YOUTUBE SEARCH ---
@akki.route('/api/search-all', methods=['GET'])
def search_all():
    query = request.args.get('q', '')
    if not query: return jsonify({"error": "Blank query"})
    try:
        # Web suggestions
        web_res = requests.get(f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}").json()
        # YouTube list logic
        yt_link = f"https://www.youtube.com/embed?listType=search&list={query}"
        return jsonify({"web": web_res[1][:5], "yt_link": yt_link})
    except:
        return jsonify({"error": "Server Busy"})

# --- REELS & LIVE APIs ---
@akki.route('/api/reels', methods=['GET'])
def get_reels():
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: r['_id'] = str(r['_id'])
    return jsonify(reels)

# --- RENDER PORT FIX ---
if __name__ == "__main__":
    # Render automatically sets a PORT, we must use it
    port = int(os.environ.get("PORT", 10000))
    akki.run(host='0.0.0.0', port=port)
    
