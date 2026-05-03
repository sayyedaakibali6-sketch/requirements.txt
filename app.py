import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
import os

akki = Flask(__name__)
CORS(akki)

client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

@akki.route('/api/search-all', methods=['GET'])
def search_all():
    query = request.args.get('q', '')
    if not query: return jsonify({"error": "Empty query"})
    try:
        web_res = requests.get(f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}").json()
        # FIXED: Direct YouTube Search Video Link
        yt_search_url = f"https://www.youtube.com/embed?listType=search&list={query}"
        return jsonify({
            "web": web_res[1][:5], 
            "yt_link": yt_search_url,
            "status": "Secure"
        })
    except:
        return jsonify({"error": "Busy"})

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    # Scrolling wapas lane ke liye fetch logic
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: r['_id'] = str(r['_id'])
    return jsonify(reels)

# Admin Upload Fix
@akki.route('/api/add-reel', methods=['POST'])
def add_reel():
    data = request.json
    if 'video_url' in data:
        reels_col.insert_one(data)
        return jsonify({"message": "Success"})
    return jsonify({"error": "Failed"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    akki.run(host='0.0.0.0', port=port)
    
