import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId

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
    
    results = {"web": [], "videos": []}
    
    try:
        # 1. Web Search (Direct Google Scraper Logic)
        web_res = requests.get(f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}").json()
        results["web"] = web_res[1][:5] # Top 5 suggestions/topics
        
        # 2. YouTube Search Logic (CID, Crime Patrol etc)
        # Hum YouTube ke search page ko parse karke embed links nikalenge
        yt_url = f"https://www.youtube.com/results?search_query={query}"
        # Note: Professional setup ke liye YouTube Data API v3 use karna best hai
        results["yt_link"] = f"https://www.youtube.com/embed?listType=search&list={query}"
        
        return jsonify(results)
    except:
        return jsonify({"error": "Server Busy"})

# --- REELS & LIVE APIs (Rest same as before) ---
@akki.route('/api/reels', methods=['GET'])
def get_reels():
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: r['_id'] = str(r['_id'])
    return jsonify(reels)

if __name__ == "__main__":
    akki.run(host='0.0.0.0', port=10000)
    
