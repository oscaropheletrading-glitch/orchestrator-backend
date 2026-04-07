// Eléments du DOM
const loginScreen = document.getElementById('login-screen');
const appScreen = document.getElementById('app-screen');
const authBtn = document.getElementById('auth-btn');
const emailInput = document.getElementById('email-input');
const nameInput = document.getElementById('name-input');
const authStatus = document.getElementById('auth-status');
const displayName = document.getElementById('display-name');

const chatBox = document.getElementById('chat-box');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

// --- ECRAN DE CONNEXION ---
authBtn.addEventListener('click', async () => {
    const email = emailInput.value.trim();
    const name = nameInput.value.trim();

    if (!email || !name) {
        authStatus.textContent = "Erreur: Identification incomplète.";
        return;
    }

    authBtn.textContent = "CONNEXION...";
    authStatus.textContent = "";

    try {
        // Envoi des données à notre API FastAPI
        const response = await fetch('/add-member', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                full_name: name,
                status: "VIP"
            })
        });

        const data = await response.json();

        if (data.error) {
            // Si l'utilisateur existe déjà, la base de données renvoie une erreur (email unique). 
            // On peut considérer ça comme un login normal pour The Orchestrator dans un premier temps.
            if (data.error.includes("duplicate key")) {
                enterApp(name);
            } else {
                authStatus.textContent = data.error;
                authBtn.textContent = "INITIALISER LA CONNEXION";
            }
        } else {
            // Nouvel utilisateur créé !
            enterApp(name);
        }
    } catch (error) {
        authStatus.textContent = "Erreur système. Serveur injoignable.";
        authBtn.textContent = "INITIALISER LA CONNEXION";
    }
});

function enterApp(name) {
    loginScreen.classList.remove('active');
    appScreen.classList.add('active');
    displayName.textContent = name;
}

// --- ECRAN DE CHAT ---

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // 1. Ajouter le message de l'utilisateur à l'interface
    addMessage(text, 'user-msg');
    chatInput.value = '';

    // 2. Faire une requête à l'API /chat de The Orchestrator
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text }) // Même format que FastAPI
        });
        
        const data = await response.json();
        
        if (data.error) {
            addMessage("SYSTÈME ERROR: " + data.error, 'orchestrator-msg');
        } else {
            addMessage(data.orchestrator_reply, 'orchestrator-msg');
        }
        
    } catch(err) {
        addMessage("SYSTÈME ERROR: Connexion perdue avec le Cortex.", 'orchestrator-msg');
    }
}

function addMessage(text, className) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${className}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'msg-content';
    contentDiv.innerText = text;
    
    msgDiv.appendChild(contentDiv);
    chatBox.appendChild(msgDiv);
    
    // Scroller vers le bas automatiquement
    chatBox.scrollTop = chatBox.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
