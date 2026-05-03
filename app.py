import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
import os

akki = Flask(__name__)
CORS(akki)

# --- MONGODB CONNECTION ---
# Tumhara connection string ekdum sahi hai
client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

# --- 1. GET ALL REELS (With Auto-Play Link Fixer) ---
@akki.route('/api/reels', methods=['GET'])
def get_reels():
    try:
        reels = list(reels_col.find().sort('_id', -1))
        for r in reels: 
            r['_id'] = str(r['_id'])
            # YouTube Link Fixer: Shorts/Watch ko Embed mein badalna zaroori hai
            url = r.get('video_url', '')
            if 'shorts/' in url: 
                r['video_url'] = url.replace('shorts/', 'embed/')
            elif 'watch?v=' in url: 
                r['video_url'] = url.replace('watch?v=', 'embed/')
        return jsonify(reels)
    except Exception as e:
        return jsonify({"error": str(e)})

# --- 2. UPLOAD NEW REEL ---
@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        if not data.get('video_url'):
            return jsonify({"success": False, "message": "Link missing"}), 400
        
        reels_col.insert_one(data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# --- 3. DELETE REEL (The missing part) ---
@akki.route('/api/delete/<id>', methods=['DELETE'])
def delete_reel(id):
    try:
        # ObjectId use karna zaroori hai MongoDB ke liye
        result = reels_col.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# --- 4. RENDER PORT FIX (Status 127 Fix) ---
if __name__ == "__main__":
    # Render automatically sets a PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    akki.run(host='0.0.0.0', port=port)
    
