from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import os

akki = Flask(__name__)
CORS(akki)

# MongoDB Setup
client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels

@akki.route('/api/reels', methods=['GET'])
def get_reels():
    try:
        reels = list(reels_col.find().sort('_id', -1))
        for r in reels: 
            r['_id'] = str(r['_id'])
            # Link Fixer for YouTube
            url = r.get('video_url', '')
            if 'shorts/' in url: r['video_url'] = url.replace('shorts/', 'embed/')
            elif 'watch?v=' in url: r['video_url'] = url.replace('watch?v=', 'embed/')
        return jsonify(reels)
    except:
        return jsonify([])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    akki.run(host='0.0.0.0', port=port)
    
