from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId

akki = Flask(__name__)
CORS(akki)

client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

@akki.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    raw_url = data.get("video_url")
    
    # Smart Link Converter
    if "shorts/" in raw_url:
        v_id = raw_url.split("shorts/")[1].split("?")[0]
        final_url = f"https://www.youtube.com/embed/{v_id}?autoplay=1&controls=0&rel=0&modestbranding=1"
    elif "instagram.com/reels/" in raw_url or "instagram.com/p/" in raw_url:
        final_url = raw_url.split("?")[0] + "embed/captioned"
    elif "tiktok.com" in raw_url:
        # TikTok ke liye direct embed logic
        final_url = raw_url # TikTok links usually need their specific embed script, but iframe works for some
    else:
        final_url = raw_url # MP4 link direct

    reels_col.insert_one({"video_url": final_url, "caption": data.get("caption", ""), "type": "embed"})
    return jsonify({"success": True})

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: r['_id'] = str(r['_id'])
    return jsonify(reels)

@akki.route('/api/delete/<id>', methods=['DELETE'])
def delete(id):
    reels_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"success": True})

if __name__ == "__main__":
    akki.run(host='0.0.0.0', port=10000)
    
