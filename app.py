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
    url = data.get("video_url")
    # YouTube Shorts link ko embed link mein convert karna
    if "shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]
        url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=0&controls=0&loop=1&modestbranding=1&showinfo=0&rel=0"
    
    reels_col.insert_one({"video_url": url, "caption": data.get("caption", ""), "likes": "0"})
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
    
