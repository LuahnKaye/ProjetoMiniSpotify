from flask import Flask
from flask_cors import CORS
from app.services.cosmos_service import init_cosmos

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Inicializar CosmosDB
    init_cosmos()

    # Registrar rotas
    from app.routes.user_routes import user_bp
    from app.routes.playlist_routes import playlist_bp
    from app.routes.music_routes import music_bp

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(playlist_bp, url_prefix="/playlists")
    app.register_blueprint(music_bp, url_prefix="/musics")

    return app
