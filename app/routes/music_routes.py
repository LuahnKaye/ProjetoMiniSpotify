from flask import Blueprint, request, jsonify
from app.services.cosmos_service import playlists_container
from app.models import Music

music_bp = Blueprint("musics", __name__)

@music_bp.route("/", methods=["POST"])
def create_music():
    data = request.json
    if not data.get("name") or not data.get("artist"):
        return jsonify({"error": "Missing fields"}), 400

    music = Music(data["name"], data["artist"])

    # Adicionar música diretamente ao container se necessário
    # playlists_container.upsert_item(music.to_dict())

    return jsonify({"message": "Music created", "music": music.to_dict()}), 201
