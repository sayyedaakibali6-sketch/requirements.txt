import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId

akki = Flask(__name__)
CORS(akki)

# Database Setup
client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

# --- Tumhari API Key yahan set kar di hai ---
YT_API_KEY = "AIzaSyBVerjaQcUumGBOSO--M1B4bOFUgXjc8eM"

@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        url = data.get("video_url")
        
        # Shorts aur Normal Video dono ke liye ID nikalna
        if "shorts/" in url:
            v_id = url.split("shorts/")[1].split("?")[0]
        elif "v=" in url:
            v_id = url.split("v=")[1].split("&")[0]
        else:
            v_id = url.split("/")[-1].split("?")[0]

        # YouTube API se Real-time data fetch karna
        api_url = f"https://www.googleapis.com/youtube/v3/videos?id={v_id}&key={YT_API_KEY}&part=statistics,snippet"
        res = requests.get(api_url).json()
        
        if not res.get('items'):
            return jsonify({"error": "Video not found"}), 404
            
        video_data = res['items'][0]
        stats = video_data['statistics']
        snippet = video_data['snippet']

        # Database mein save karna
        reels_col.insert_one({
            "video_id": v_id,
            "video_url": f"https://www.youtube.com/embed/{v_id}?autoplay=1&modestbranding=1&rel=0&iv_load_policy=3&enablejsapi=1&playsinline=1",
            "caption": snippet['title'],
            "likes": stats.get('likeCount', '0'),
            "channel_name": snippet['channelTitle'],
            "views": stats.get('viewCount', '0'),
            "comments": stats.get('commentCount', '0')
        })
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: r['_id'] = str(r['_id'])
    return jsonify(reels)

if __name__ == "__main__":
    akki.run(host='0.0.0.0', port=10000)
    
