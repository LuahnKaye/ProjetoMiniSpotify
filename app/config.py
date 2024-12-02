import os

COSMOS_DB_URI = os.getenv("COSMOS_DB_URI", "https://minispotifydb.documents.azure.com:443/")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY", "hfmSHl3at6ToN0IBnCXuh5sHitFnqCFm8XRWe67CgWGfEsSD5Ctn81ndJnRnubwgK8oayoFWPFPOACDbhudQdg==")
COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME", "MiniSpotifyDB")
