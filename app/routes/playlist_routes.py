from flask import Blueprint, request, jsonify
from app.services.cosmos_service import playlists_container
from app.models import Playlist

playlist_bp = Blueprint("playlists", __name__)

@playlist_bp.route("/", methods=["POST"])
def create_playlist():
    data = request.json
    if not data.get("user_id") or not data.get("name"):
        return jsonify({"error": "Missing fields"}), 400

    playlist = Playlist(data["user_id"], data["name"])
    try:
        playlists_container.upsert_item(playlist.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Playlist created", "playlist": playlist.to_dict()}), 201

@playlist_bp.route("/<playlist_id>/add-music", methods=["POST"])
def add_music(playlist_id):
    data = request.json
    if not data.get("music_name") or not data.get("artist"):
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
