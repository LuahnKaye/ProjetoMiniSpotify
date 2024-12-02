from flask import Blueprint, request, jsonify
from app.services.cosmos_service import users_container
from app.models import User
import uuid  # Para gerar IDs únicos

user_bp = Blueprint("users", __name__)

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    if not data.get("email") or not data.get("name") or not data.get("password"):
        return jsonify({"error": "Missing fields"}), 400

    # Verificar se o usuário já existe
    query = f"SELECT * FROM c WHERE c.email = '{data['email']}'"
    existing_users = list(users_container.query_items(query=query, enable_cross_partition_query=True))
    if existing_users:
        return jsonify({"error": "User with this email already exists"}), 409

    # Criar o usuário com ID único
    user = User(str(uuid.uuid4()), data["email"], data["name"], data["password"])
    try:
        users_container.upsert_item(user.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User created", "user": user.to_dict()}), 201

@user_bp.route("/", methods=["GET"])
def get_users():
    try:
        users = list(users_container.read_all_items())
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve users: {str(e)}"}), 500
