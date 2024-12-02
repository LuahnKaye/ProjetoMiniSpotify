from flask import Blueprint, request, jsonify
from app.models import Music
from app.services.cosmos_service import songs_container  # Importar o container Songs
import uuid

music_bp = Blueprint("musics", __name__)

@music_bp.route("/", methods=["POST"])
def create_music():
    data = request.json
    if not data.get("name") or not data.get("artist"):
        return jsonify({"error": "Missing fields"}), 400

    music_id = str(uuid.uuid4())
    music = Music(data["name"], data["artist"])
    music_dict = music.to_dict()
    music_dict["id"] = music_id

    # Adicionar a música ao CosmosDB
    try:
        songs_container.upsert_item(music_dict)
    except Exception as e:
        return jsonify({"error": f"Failed to save music: {str(e)}"}), 500

    return jsonify({"message": "Music created", "music": music_dict}), 201

@music_bp.route("/", methods=["GET"])
def get_musics():
    try:
        musics = list(songs_container.read_all_items())
        return jsonify({"musics": musics}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve musics: {str(e)}"}), 500
