import os
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
from pinecone import Pinecone

# 1. Charger les clés secrètes depuis le fichier .env
load_dotenv()

app = FastAPI()

# 2. Récupération & Connexion à Supabase
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")

if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
else:
    supabase = None
    print("⚠️ Attention: Clés Supabase manquantes.")

# 3. Récupération & Connexion à Pinecone
pinecone_key: str = os.getenv("PINECONE_API_KEY")

if pinecone_key:
    pc = Pinecone(api_key=pinecone_key)
    try:
        # Remplace "index-quickstart" par le nom de ton index si différent
        pinecone_index = pc.Index("orchestrator")
    except Exception as e:
        pinecone_index = None
        print(f"⚠️ Erreur avec l'Index Pinecone: {e}")
else:
    pc = None
    pinecone_index = None
    print("⚠️ Attention: Clé Pinecone manquante.")

@app.get("/")
def home():
    return {"status": "The Orchestrator is operational"}

@app.get("/system-check")
def system_check():
    """
    Cette route permet de vérifier que tes bases de données sont bien connectées !
    """
    return {
        "status": "Check completed",
        "supabase_connected": supabase is not None,
        "pinecone_connected": pc is not None
    }
