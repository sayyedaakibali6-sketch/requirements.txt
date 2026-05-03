import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader

akki = Flask(__name__)
CORS(akki)

# MongoDB Setup
client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

# Cloudinary Setup (Fixed Credentials)
cloudinary.config( 
  cloud_name = "ds0psevfl", 
  api_key = "796123982348574", 
  api_secret = "AGeK2CnY01xh_AlOM7GhJyPKD6Y" 
)

YT_API_KEY = "AIzaSyBVerjaQcUumGBOSO--M1B4bOFUgXjc8eM"

# YouTube Upload
@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        url = data.get("video_url")
        v_id = url.split("shorts/")[1].split("?")[0] if "shorts/" in url else url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1].split("?")[0]
        api_url = f"https://www.googleapis.com/youtube/v3/videos?id={v_id}&key={YT_API_KEY}&part=statistics,snippet"
        res = requests.get(api_url).json()
        reels_col.insert_one({
            "video_url": f"https://www.youtube.com/embed/{v_id}?enablejsapi=1&autoplay=0&controls=0",
            "caption": res['items'][0]['snippet']['title'] if 'items' in res else "YouTube Video",
            "channel_name": res['items'][0]['snippet']['channelTitle'] if 'items' in res else "Vanced Pro",
            "type": "youtube"
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Gallery Upload (Using your 'vanced_upload' preset)
@akki.route('/api/upload-gallery', methods=['POST'])
def upload_gallery():
    try:
        if 'video' not in request.files:
            return jsonify({"error": "No video file found"}), 400
            
        file = request.files['video']
        # Force using the 'vanced_upload' unsigned preset you created
        res = cloudinary.uploader.upload(
            file, 
            resource_type="video", 
            upload_preset="vanced_upload"
        )
        
        reels_col.insert_one({
            "video_url": res['secure_url'],
            "caption": request.form.get("caption", "Gallery Video"),
            "channel_name": "My Gallery",
            "type": "local"
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

if __name__ == "__main__":
    akki.run(host='0.0.0.0', port=10000)
  
