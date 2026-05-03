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

# Live Status Setup
live_col = db.live_status

@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        url = data.get("video_url")
        caption = data.get("caption", "New Reel")
        
        # Simple Logic: Agar YouTube hai toh embed link banao, baaki ke liye direct URL use karo
        if "youtube.com" in url or "youtu.be" in url:
            v_id = url.split("shorts/")[1].split("?")[0] if "shorts/" in url else url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1].split("?")[0]
            final_url = f"https://www.youtube.com/embed/{v_id}?enablejsapi=1&autoplay=1&controls=0"
            v_type = "youtube"
        else:
            # TikTok, FB, Insta ke liye direct video links
            final_url = url
            v_type = "external"

        reels_col.insert_one({
            "video_url": final_url,
            "caption": caption,
            "type": v_type,
            "channel_name": "Vanced Pro"
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# LIVE SYSTEM: Admin se status update karne ke liye
@akki.route('/api/go-live', methods=['POST'])
def go_live():
    data = request.json
    # is_live: true/false, stream_url: hls or embed link
    live_col.update_one({}, {"$set": data}, upsert=True)
    return jsonify({"success": True})

@akki.route('/api/live-status', methods=['GET'])
def get_live():
    status = live_col.find_one({}, {'_id': 0})
    return jsonify(status or {"is_live": False})

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    search = request.args.get('search', '')
    query = {"caption": {"$regex": search, "$options": "i"}} if search else {}
    reels = list(reels_col.find(query).sort('_id', -1))
    for r in reels: r['_id'] = str(r['_id'])
    return jsonify(reels)

@akki.route('/api/delete/<id>', methods=['DELETE'])
def delete_video(id):
    reels_col.delete_one({"_id": ObjectId(id)})
    return jsonify({"success": True})

if __name__ == "__main__":
    akki.run(host='0.0.0.0', port=10000)
  
