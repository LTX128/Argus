# Argus - Système de Capture Distante 🎯

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Made with ❤️](https://img.shields.io/badge/made%20with-❤️-red.svg)]()

Argus est un outil puissant et discret conçu pour capturer des photos à distance via une simple interface web. Il génère des liens uniques qui, lorsqu'ils sont ouverts, permettent de capturer une image depuis la caméra de la cible et de l'envoyer instantanément sur un chat Telegram.

> **Idéal pour la sécurité, le monitoring d'appareils personnels ou des tests de pénétration autorisés.**

---

## ⚡ Fonctionnalités

-   🌐 **Tunnel Public Automatique** : Intégration de `cloudflared` pour exposer votre serveur local sur internet en un clic, sans configuration de réseau complexe.
-   ⚡ **Capture Ultra-Rapide et Discrète** : Page de vérification optimisée pour être rapide (< 1 seconde) et passer inaperçue.
-   📸 **Envoi Direct via Telegram** : Les photos capturées sont envoyées instantanément et de manière sécurisée à votre bot Telegram.
-   🎨 **Interface Web Moderne** : Panneau de contrôle élégant et sombre pour créer et gérer facilement vos liens de capture.
-   🔧 **Facile à Déployer** : Installation des dépendances automatique et démarrage simple.

---

## ⚠️ Avertissement Important : Responsabilité et Usage Légal

Cet outil est conçu à des fins éducatives, de sécurité personnelle et de tests d'intrusion **légaux et autorisés**.

L'utilisation de Argus à des fins malveillantes, pour espionner des individus sans leur consentement éclairé, ou pour toute activité illégale est **strictement interdite** et peut constituer une violation des lois sur la vie privée et la cybersécurité.

**Vous êtes le seul responsable de l'usage que vous faites de ce logiciel.** Les développeurs déclinent toute responsabilité pour les dommages ou les problèmes légaux résultant d'une mauvaise utilisation. **Utilisez cet outil de manière éthique et responsable.**

---

## 📋 Prérequis

-   **Python 3.7 ou supérieur**
-   **Un Bot Telegram** (créez-le via [@BotFather](https://t.me/BotFather) sur Telegram)
-   **pip** (gestionnaire de paquets Python)

---

## 🚀 Installation

1.  **Cloner ce dépôt :**
    ```bash
    git clone https://github.com/VOTRE_NOM_D_UTILISATEUR/Argus.git
    cd Argus
    ```

2.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```
    *(Si le fichier `requirements.txt` n'existe pas, créez-le et ajoutez les lignes ci-dessous)*

    **Contenu de `requirements.txt` :**
    ```
    Flask
    requests
    ```

3.  **Démarrer Argus :**
    ```bash
    python Argus.py
    ```

Au premier lancement, le script vérifiera si `cloudflared` est installé. Si ce n'est pas le cas, il l'installera automatiquement pour vous.

---

## ⚙️ Configuration

1.  Une fois le script démarré, ouvrez votre navigateur et allez à l'adresse locale indiquée (généralement `http://localhost:5000`).

2.  **Récupérez votre Token de Bot Telegram :**
    *   Parlez à [@BotFather](https://t.me/BotFather) sur Telegram.
    *   Utilisez la commande `/newbot` pour créer un bot.
    *   Copiez le token que BotFather vous donne (il ressemble à `1234567890:ABCDEF...`).

3.  **Récupérez votre Chat ID :**
    *   Parlez à votre nouveau bot.
    *   Envoyez-lui un message.
    *   Allez sur `https://api.telegram.org/bot<VOTRE_TOKEN>/getUpdates` dans votre navigateur.
    *   Cherchez `"chat":{"id":123456789` dans la réponse JSON. Le nombre est votre Chat ID.

4.  **Remplissez le formulaire de configuration sur la page d'accueil d'Argus avec votre Chat ID, votre Token Bot et l'URL de redirection souhaitée.**

---

## 📖 Utilisation

1.  Sur le panneau de contrôle, cliquez sur **"Générer le Lien de Capture"**.
2.  Un lien unique sera généré. Copiez-le.
3.  Envoyez ce lien à la personne que vous souhaitez capturer (ou testez-le vous-même).
4.  Lorsque la personne cliquera sur le lien, une page de "Vérification de sécurité" s'affichera brièvement.
5.  La photo sera capturée et vous la recevrez directement dans votre chat Telegram !

---

## 📸 Démonstration

### Panneau de Contrôle
*(Ici, vous pourriez ajouter une capture d'écran de l'interface web)*
`![Panneau de Contrôle](screenshots/dashboard.png)`

### Page de Vérification Discrète
*(Ici, vous pourriez ajouter une capture d'écran de la page de vérification)*
`![Page de Vérification](screenshots/verification.png)`

---

## 📁 Structure du Projet
