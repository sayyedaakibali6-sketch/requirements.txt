import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId

akki = Flask(__name__)
CORS(akki)

client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

YT_API_KEY = "AIzaSyBVerjaQcUumGBOSO--M1B4bOFUgXjc8eM"

@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        url = data.get("video_url")
        # Video ID nikalne ka sabse fast tareeka
        v_id = url.split("shorts/")[1].split("?")[0] if "shorts/" in url else url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]

        # YouTube Data Fetch
        api_url = f"https://www.googleapis.com/youtube/v3/videos?id={v_id}&key={YT_API_KEY}&part=statistics,snippet"
        res = requests.get(api_url).json()
        
        # Agar API response na de, toh default data bhar do (Crash nahi hoga)
        if 'items' in res and len(res['items']) > 0:
            item = res['items'][0]
            title = item['snippet']['title']
            likes = item['statistics'].get('likeCount', '0')
            channel = item['snippet']['channelTitle']
        else:
            title, likes, channel = "YouTube Video", "M", "Vanced User"

        reels_col.insert_one({
            "video_id": v_id,
            "video_url": f"https://www.youtube.com/embed/{v_id}?autoplay=1&modestbranding=1&rel=0&iv_load_policy=3&enablejsapi=1&playsinline=1",
            "caption": title,
            "likes": likes,
            "channel_name": channel
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
    
