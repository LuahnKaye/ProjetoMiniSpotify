from flask import Blueprint, request, jsonify
from app.services.cosmos_service import playlists_container
from app.models import Playlist
import uuid

playlist_bp = Blueprint("playlists", __name__)

@playlist_bp.route("/", methods=["POST"])
def create_playlist():
    data = request.json
    if not data.get("user_id") or not data.get("name"):
        return jsonify({"error": "Missing fields"}), 400

    playlist_id = str(uuid.uuid4())  # Gera um ID único
    playlist = Playlist(data["user_id"], data["name"])
    playlist_dict = playlist.to_dict()
    playlist_dict["id"] = playlist_id

    try:
        playlists_container.upsert_item(playlist_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Playlist created", "playlist": playlist_dict}), 201

@playlist_bp.route("/<playlist_id>/add-music", methods=["POST"])
def add_music(playlist_id):
    data = request.json
    if not data.get("user_id") or not data.get("music_name") or not data.get("artist"):
        return jsonify({"error": "Missing fields"}), 400

    try:
        playlist = playlists_container.read_item(playlist_id, partition_key=data["user_id"])
    except Exception as e:
        return jsonify({"error": "Playlist not found"}), 404

    music = {"name": data["music_name"], "artist": data["artist"]}
    playlist["musics"].append(music)

    try:
        playlists_container.upsert_item(playlist)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Music added", "playlist": playlist}), 200

@playlist_bp.route("/", methods=["GET"])
def get_playlists():
    try:
        playlists = list(playlists_container.read_all_items())
        return jsonify({"playlists": playlists}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve playlists: {str(e)}"}), 500
