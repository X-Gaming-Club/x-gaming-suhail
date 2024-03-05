from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import json
from xgamingai import get_next_action

app = Flask(__name__)

CORS(app)


"""
    Data : {
        "enemy": {
            "_id" : {
                "damage" : _int,
                "health" : _int,
                "distance" : _int,
            }
        },
        "player": {
            "_health" : _int,
            "id" : _int
        }
        "npc": {
            "_health" : _int,
            "id" : _int
        }
    }

    Response : {
        _entity_id : _spell_id
    }
"""
@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    targets = get_next_action(data)
    print(targets)
    return jsonify(targets)