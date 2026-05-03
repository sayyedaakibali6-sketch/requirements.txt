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

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    try:
        reels = list(reels_col.find().sort('_id', -1))
        for r in reels: 
            r['_id'] = str(r['_id'])
            url = r.get('video_url', '')
            if 'shorts/' in url: 
                r['video_url'] = url.replace('shorts/', 'embed/').split('?')[0]
            elif 'watch?v=' in url: 
                r['video_url'] = url.replace('watch?v=', 'embed/').split('&')[0]
        return jsonify(reels)
    except Exception as e:
        return jsonify({"error": str(e)})

@akki.route('/api/upload', methods=['POST'])
def upload():
    try:
        data = request.json
        if data.get('video_url'):
            reels_col.insert_one(data)
            return jsonify({"success": True})
        return jsonify({"success": False}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@akki.route('/api/delete/<id>', methods=['DELETE'])
def delete_reel(id):
    try:
        reels_col.delete_one({"_id": ObjectId(id)})
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    akki.run(host='0.0.0.0', port=port)
    
