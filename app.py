import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId

akki = Flask(__name__)
CORS(akki)

# MongoDB Setup
client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels
live_col = db.live_status # For Live TV/News links

# Smart Link Parser (YouTube vs Direct Video)
def parse_video_url(url):
    if "youtube.com" in url or "youtu.be" in url:
        v_id = url.split("shorts/")[1].split("?")[0] if "shorts/" in url else url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1].split("?")[0]
        return f"https://www.youtube.com/embed/{v_id}?enablejsapi=1&autoplay=1&mute=0&controls=0", "youtube"
    # For Instagram, TikTok, Facebook direct MP4 links
    return url, "direct"

# --- REELS API ---
@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        final_url, v_type = parse_video_url(data.get("video_url"))
        reels_col.insert_one({
            "video_url": final_url,
            "caption": data.get("caption", "New Reel"),
            "type": v_type,
            "channel_name": data.get("channel", "VancedPro")
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: r['_id'] = str(r['_id'])
    return jsonify(reels)

@akki.route('/api/delete/<id>', methods=['DELETE'])
def delete_video(id):
    reels_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"success": True})

# --- LIVE TV/NEWS API ---
@akki.route('/api/set-live', methods=['POST'])
def set_live():
    data = request.json # {channel_name: str, stream_url: str, is_active: bool}
    live_col.update_one({"channel_name": data['channel_name']}, {"$set": data}, upsert=True)
    return jsonify({"success": True})

@akki.route('/api/get-live', methods=['GET'])
def get_live():
    streams = list(live_col.find({"is_active": True}, {'_id': 0}))
    return jsonify(streams)

# --- SMART WORLD SEARCH API (Real-time Wikipedia Hack) ---
@akki.route('/api/search-world', methods=['GET'])
def search_world():
    query = request.args.get('q', '')
    if not query: return jsonify({"error": "No query"})
    
    # Simple hack using Wikipedia API for real-time info
    wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    try:
        res = requests.get(wiki_url).json()
        if "title" in res:
            return jsonify({
                "title": res['title'],
                "description": res.get('extract', 'No info found'),
                "image": res.get('thumbnail', {}).get('source', '')
            })
        return jsonify({"error": "Not found"})
    except:
        return jsonify({"error": "Search failed"})

if __name__ == "__main__":
    akki.run(host='0.0.0.0', port=10000)
