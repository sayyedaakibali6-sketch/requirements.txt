import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import os

akki = Flask(__name__)
CORS(akki)

client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

@akki.route('/api/search-all', methods=['GET'])
def search_all():
    query = request.args.get('q', '')
    if not query: return jsonify({"error": "Empty"})
    try:
        # Chrome suggestion logic
        web_res = requests.get(f"https://suggestqueries.google.com/complete/search?client=firefox&q={query}").json()
        # YouTube Search Redirect logic
        yt_search = f"https://www.youtube.com/embed?listType=search&list={query}"
        return jsonify({"web": web_res[1][:5], "yt_link": yt_search})
    except:
        return jsonify({"error": "Server Down"})

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: 
        r['_id'] = str(r['_id'])
        # Link ko embed format mein convert karna zaroori hai
        if 'youtube.com/shorts/' in r['video_url']:
            r['video_url'] = r['video_url'].replace('shorts/', 'embed/')
        elif 'watch?v=' in r['video_url']:
            r['video_url'] = r['video_url'].replace('watch?v=', 'embed/')
    return jsonify(reels)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    akki.run(host='0.0.0.0', port=port)
    
