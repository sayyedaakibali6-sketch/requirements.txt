from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo

app = Flask(__Create AkkiDGDon__)
CORS(app)

# MongoDB Connection - Aapka wahi purana database
client = pymongo.MongoClient("mongodb+srv://abudhabisyed80_db_user:Akki12345@cluster0.cdettyo.mongodb.net/fitnessDB?retryWrites=true&w=majority")
db = client.fitnessDB
reels_col = db.reels 

@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    reels_col.insert_one({
        "video_url": data.get("video_url"), # Direct .mp4 link yahan jayega
        "caption": data.get("caption", ""),
        "likes": 0
    })
    return jsonify({"status": "success"})

@app.route('/api/reels', methods=['GET'])
def get_reels():
    reels = list(reels_col.find().sort('_id', -1))
    for r in reels: r['_id'] = str(r['_id'])
    return jsonify(reels)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
  
