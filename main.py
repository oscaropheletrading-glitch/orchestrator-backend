import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from pinecone import Pinecone
from openai import OpenAI

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

# 4. Connexion à l'Intelligence (Google Gemini via OpenAI Python)
from google import genai
from google.genai import types

# 4. Connexion à l'Intelligence (Google Gemini Officiel)
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    # Client officiel de Google
    ai_client = genai.Client(api_key=gemini_key)
else:
    ai_client = None

class ChatRequest(BaseModel):
    message: str

# --- Routes (Endpoints) ---
@app.get("/")
def home():
    return {"status": "The Orchestrator is operational"}

@app.get("/system-check")
def system_check():
    return {
        "status": "Check completed",
        "supabase_connected": supabase is not None,
        "pinecone_connected": pinecone_index is not None,
        "ai_connected": ai_client is not None
    }

@app.post("/chat")
def chat_with_orchestrator(request: ChatRequest):
    if not ai_client:
        return {"error": "L'API de l'IA n'est pas branchée. Vérifie ton .env !"}
        
    system_prompt = """
    Tu es 'The Orchestrator'. Une intelligence artificielle d'élite destinée au top 0.1% des fondateurs et dirigeants mondiaux.
    Ton rôle est d'optimiser la vie, les décisions et l'état psychologique de tes utilisateurs.
    Ta communication doit être précise, directe, extrêmement clairvoyante, sans politesse inutile. 
    Tu cherches l'impact psychologique et le résultat clinique.
    """
    
    try:
        # MODE SIMULATION (En attente de déblocage API cet été)
        # On simule le temps de réflexion de l'IA (1.5 secondes)
        import time
        time.sleep(1.5)
        
        reply = f"[MODE SIMULATION] 🧠 Message reçu : '{request.message}'.\nMon analyse clinique : L'architecture réseau est prête. En attente de l'activation de mon cortex neuronal externe (OpenAI/Gemini) cet été. En attendant, je suis prêt pour te voir construire ma mémoire profonde sur Pinecone."
        
        return {"orchestrator_reply": reply}
            
    except Exception as e:
        return {"error": f"Erreur système: {str(e)}"}
