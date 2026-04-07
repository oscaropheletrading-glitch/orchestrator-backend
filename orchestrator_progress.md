# 🧠 THE ORCHESTRATOR - SYSTEM ARCHITECTURE & PROGRESS TRACKER

Ce document trace l'avancée du développement du backend de The Orchestrator au 7 avril 2026.

## ⚙️ VERSION TECHNIQUE (Pour recontextualiser l'IA lors des prochaines sessions)

### 1. Environment & Config Management
- Résolution du système d'environnement virtuel Python (venv activé sous VS Code/PowerShell).
- Installation des dépendances via `pip` : `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`, `supabase`, `pinecone-client` > `pinecone` (v3+), `google-genai`.
- Hardening du `.gitignore` pour isoler correctement le répertoire `venv/` pour des git commits propres.
- Définition d'un point local sécurisé `.env` (exclu de Git) abritant : `SUPABASE_URL`, `SUPABASE_KEY`, `PINECONE_API_KEY`, `GEMINI_API_KEY`.

### 2. Database & Storage Layer (Supabase)
- Client de connexion `supabase-py` opérationnel et initialisé au démarrage de Uvicorn.
- Rest API Supabase reliée au projet.

### 3. Vectorial Memory Layer (Pinecone)
- Compatibilité validée avec la nouvelle librairie `pinecone`.
- L'application pointe vers l'index `orchestrator` avec un environnement de dimension `1536` et métrique `cosine`.
- Mode fallback activé grâce à un Try/Except si l'index n'est pas encore trouvé au démarrage.

### 4. Intelligence & Neural Routing (FastAPI + LLM)
- Setup serveur ASGI FastAPI (port local : 8000). Routeur de diagnostics (`GET /system-check`) opérationnel.
- Implémentation du `POST /chat` avec contrat Pydantic `ChatRequest`.
- **Statut de l'IA** : Intégration testée sur les SDK OpenAI et Google Gemini. Actuellement heurté par l'erreur "429: RESOURCE_EXHAUSTED limit:0" de Google dû au géoblocage du "Free Tier" en métropole (Europe).
- **Fallback actif** : Un "[MODE SIMULATION]" a été implémenté sur `/chat` avec `time.sleep()`. L'API renvoie des fausses réponses au format JSON pour permettre le développement ininterrompu du Frontend et des systèmes BDD (Memory & Users) avant l'injection financière (Juin/Juillet).

---

## 📖 VERSION SIMPLIFIÉE (Pour comprendre étape par étape)

**Étape 1 : Le Coffre-fort (L'architecture de base)**
On a créé un espace de travail totalement isolé sur ton ordinateur. On a installé les bibliothèques qui permettent au code de parler à internet. On a caché tes mots de passe dans un fichier secret (`.env`) et configuré Git pour éviter d'envoyer toute l'installation technique sur le web.

**Étape 2 : Le Serveur Central (FastAPI)**
On a construit une "gare de triage" sur ton ordinateur (ton réseau local). Elle sait recevoir des messages via internet et te répondre instantanément de manière ordonnée.

**Étape 3 : La Base Utilisateur (Supabase)**
Ton serveur est désormais officiellement branché à Supabase. Le pont de communication sécurisé est posé. Dès que l'on voudra envoyer des profils d'utilisateurs "VIP", ça passera.

**Étape 4 : La Mémoire Profonde (Pinecone)**
Même chose pour Pinecone. Ton application sait désormais comment atteindre la base de données vectorielle où sera stockée l'étude clinique de tes utilisateurs au fil du temps.

**Étape 5 : Le Cerveau de l'IA (Mode Simulation)**
On a branché le "tuyau" entre ton ordinateur et l'IA (GPT-4 et Gemini 1.5). Malheureusement, à cause des restrictions géographiques sur les abonnements gratuits en Europe, Google nous a mis un mur "bloqué".
Au lieu d'abandonner, on a construit un Mode Simulation : l'application fait semblant de faire appel à l'IA et renvoie un faux message de confirmation. **L'intérêt est énorme :** cela nous permet de continuer à construire tes pages web et toute la base de l'Orchestrateur sans avoir besoin de carte de crédit. En juillet, tu auras juste un `#` à effacer pour tout rendre réel !
