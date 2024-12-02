from azure.cosmos import CosmosClient
from app.config import COSMOS_DB_URI, COSMOS_DB_KEY, COSMOS_DB_NAME

client = None
database = None
users_container = None
playlists_container = None

def init_cosmos():
    global client, database, users_container, playlists_container
    client = CosmosClient(COSMOS_DB_URI, COSMOS_DB_KEY)
    database = client.create_database_if_not_exists(COSMOS_DB_NAME)
    users_container = database.create_container_if_not_exists(
        id="Users",
        partition_key={"path": "/email"},
        offer_throughput=400
    )
    playlists_container = database.create_container_if_not_exists(
        id="Playlists",
        partition_key={"path": "/user_id"},
        offer_throughput=400
    )
