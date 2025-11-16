# 📸 - Argus - Système de Capture par lien 🎯

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Made with ❤️](https://img.shields.io/badge/made%20with-❤️-red.svg)]()

Argus est un outil puissant et discret conçu pour capturer des photos à distance via une simple interface web. Il génère des liens uniques qui, lorsqu'ils sont ouverts, permettent de capturer une image depuis la caméra de la cible et de l'envoyer instantanément sur un chat **Telegram** ou un canal **Discord**.

> **Idéal pour la sécurité, le monitoring d'appareils personnels ou des tests de pénétration autorisés.**

---

## ⚡ Fonctionnalités

-   🌐 **Tunnel Public Automatique** : Intégration de `cloudflared` pour exposer votre serveur local sur internet en un clic, sans configuration de réseau complexe.
-   ⚡ **Capture Ultra-Rapide et Discrète** : Page de vérification optimisée pour être rapide (< 1 seconde) et passer inaperçue.
-   📸 **Envoi Multi-plateformes** : Les photos capturées sont envoyées instantanément et de manière sécurisée, au choix via **Telegram** ou **Discord**.
-   🎨 **Interface Web Moderne** : Panneau de contrôle élégant et sombre avec des onglets dédiés pour choisir facilement votre plateforme de livraison.
-   🤖 **Personnalisation Automatique (Discord)** : Le bot Discord apparaît automatiquement avec le nom "Argus Bot" et un avatar personnalisé pour une reconnaissance instantanée.
-   🔧 **Facile à Déployer** : Installation des dépendances automatique et démarrage simple.

---

## ⚠️ Avertissement Important : Responsabilité et Usage Légal

Cet outil est conçu à des fins éducatives, de sécurité personnelle et de tests d'intrusion **légaux et autorisés**.

L'utilisation de Argus à des fins malveillantes, pour espionner des individus sans leur consentement éclairé, ou pour toute activité illégale est **strictement interdite** et peut constituer une violation des lois sur la vie privée et la cybersécurité.

**Vous êtes le seul responsable de l'usage que vous faites de ce logiciel.** Les développeurs déclinent toute responsabilité pour les dommages ou les problèmes légaux résultant d'une mauvaise utilisation. **Utilisez cet outil de manière éthique et responsable.**

---

## 📋 Prérequis

-   **Python 3.7 ou supérieur**
-   **Un Bot Telegram** (créez-le via [@BotFather](https://t.me/BotFather) sur Telegram) - *Requis pour l'envoi via Telegram*
-   **Un Webhook Discord** (créez-le dans les paramètres de votre serveur Discord) - *Requis pour l'envoi via Discord*
-   **pip** (gestionnaire de paquets Python)

---

## 🚀 Installation

1.  **Cloner ce dépôt :**
    ```bash
    git clone https://github.com/LTX128/Argus.git
    cd Argus
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Démarrer Argus :**
    ```bash
    Executer : Argus.exe ou Argus.py
    ```

Au premier lancement, le script vérifiera si `cloudflared` est installé. Si ce n'est pas le cas, il l'installera automatiquement pour vous.

---

## ⚙️ Configuration

La configuration dépend de la plateforme que vous souhaitez utiliser. Le panneau de contrôle vous permet de choisir entre Telegram et Discord.

### Pour Telegram

1.  **Récupérez votre Token de Bot Telegram :**
    *   Parlez à [@BotFather](https://t.me/BotFather) sur Telegram.
    *   Utilisez la commande `/newbot` pour créer un bot.
    *   Copiez le token que BotFather vous donne (il ressemble à `1234567890:ABCDEF...`).

2.  **Récupérez votre Chat ID :**
    *   Parlez à votre nouveau bot.
    *   Envoyez-lui un message.
    *   Allez sur `https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates` dans votre navigateur.
    *   Cherchez `"chat":{"id":123456789` dans la réponse JSON. Le nombre est votre Chat ID.

### Pour Discord

1.  **Créez un Webhook Discord :**
    *   Allez dans les paramètres de votre serveur Discord.
    *   Naviguez vers **"Intégrations"** -> **"Webhooks"**.
    *   Cliquez sur **"Créer un Webhook"**.
    *   Donnez-lui un nom (par ex. "Argus Captures") et sélectionnez le canal où les messages seront envoyés.
    *   Copiez l'**URL du Webhook**. Elle ressemble à `https://discord.com/api/webhooks/...`. C'est cette URL que vous utiliserez dans Argus.
    *   *Note : Le nom et l'avatar du bot seront automatiquement définis par Argus ("Argus Bot"), vous n'avez pas besoin de les configurer ici.*

### Configuration dans Argus

1.  Une fois le script démarré, ouvrez votre navigateur et allez à l'adresse locale indiquée (généralement `http://localhost:5000`).
2.  Choisissez l'onglet de votre plateforme (Telegram ou Discord).
3.  Remplissez le formulaire avec les informations récupérées (Token Bot + Chat ID pour Telegram, ou URL Webhook pour Discord) et l'URL de redirection souhaitée.

---

## 📖 Utilisation

1.  Sur le panneau de contrôle, choisissez votre plateforme (Telegram ou Discord) et cliquez sur **"Générer le Lien de Capture"**.
2.  Un lien unique sera généré. Copiez-le.
3.  Envoyez ce lien à la personne que vous souhaitez capturer (ou testez-le vous-même).
4.  Lorsque la personne cliquera sur le lien, une page de "Vérification de sécurité" s'affichera brièvement.
5.  La photo sera capturée et vous la recevrez directement dans votre chat Telegram ou sur votre canal Discord !

---

# 📸 - Argus - Made By LTX - 🛜

---
