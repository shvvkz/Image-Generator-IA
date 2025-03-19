# Image Generator IA
par Viggo Casciano

# Le sujet
Voici le sujet:
- Créer un code python qui prend en entrée un prompt d'un **utilisateur**.
- Ce prompt doit être _renforcé_ par le LLM Deepseek.
- Ensuite le prompt renforcé doit être envoyer à une IA générative d'image appelé Black Forest pour générer une image.

## 1. Mise en place du projet:

### 1.1 Récupération du projet:
Veuillez avant toutes choses,  récupérer le projet via ce lien github avec la commande :

```sh
git clone https://github.com/shvvkz/Image-Generator-IA.git
cd Image-Generator-Ia
```

### 1.2 Mise en place de l'environnement virtuelle:
Pour créer un environnement virtuelle veuillez éxécuter cette commande:
```sh
python -m venv venv
```

Ensuite nous allons nous placer dans cette environnement virtuelle avec cette commande :

**Pour Linux:**
```sh
source venv/bin/activate
```

**Pour Windows:**
```sh
venv\Scripts\activate
```

### 1.3 Récupération des clefs d'API

Avant tout il vous faut faire une copy du fichier .env.example et de renommer cette copie en **.env**, celui ci devrait ressembler à ça:
```txt
NOVITA_API_KEY=
NEBIUS_API_KEY=
```
Pour ce projet vous avez besoin de générer deux clefs d'API:
- Une clef de **Novita**, qui va nous permettre de générer un prompt améliorer.
- Une clef de **Nebius**, qui va nous permettre de générer l'image.

Pour ce faire rendez vous sur ces deux liens:
- Novita : [Création d'API pour Novita](https://novita.ai/settings/key-management?utm_source=getstarted)
- Nebius : [Création d'API pour Nebius](https://nebius.com/settings/api-keys)

Vous allez devoir vous créer un compte sur chacun des deux sites pour pouvoir vous générer une image.
#### 1.3.1 Générer une clef d'API sur Novita
Rendez vous sur le lien ci dessus après avoir créer votre compte et vous allez devoir:
- Cliquez sur **Add New Key**
- Rentrez un nom pour votre clef d'API (exemple: Novita)
- Appuyez sur **Copy**
- Coller le contenu dans le fichier **.env** à droite de _NOVITA_API_KEY=_

Le contenu de votre fichier **.env** devrait être:
```txt
NOVITA_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NEBIUS_API_KEY=
```

#### 1.3.2 Générer une clef d'API sur Novita 
Rendez vous sur le lien ci dessus après avoir créer votre compte et vous allez devoir:
- Cliquez sur **Create API Key**
- Rentrez un nom pour votre clef d'API (exemple: Nebius)
- Appuyez sur **Copy**
- Coller le contenu dans le fichier **.env** à droite de _NEBIUS_API_KEY=_

Le contenu de votre fichier **.env** devrait être:
```txt
NOVITA_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NEBIUS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

```
### 1.4 Installation des dépendances:
Pour installer les dépendances du projet il va falloir éxécuter cette commande:
```sh
pip install -r requirements.txt
```
Celui ci va nous installer 3 packages:
- huggingface-hub: package qui va nous rendre les intéractions avec les API des IA plus simple
- dotenv: package qui va nous permettre de gérer nous variables d'environnements
- pillow: package qui va nous permettre d'écrire une image à partir d'une BitMap

## 2. Génération du prompt intermédiaire:

Une fois que vous avez configuré votre environnement et installé les dépendances, vous pouvez exécuter le script pour générer un prompt amélioré grâce à l'IA.

### 2.1 Exécution du script:
Pour exécuter le script, utilisez la commande suivante :
```sh
python main.py
```

Lorsque vous exécutez le script, celui-ci vous demandera d'entrer un prompt. Ce prompt sera amélioré par l'IA Novita pour le rendre plus descriptif et adapté à la génération d'images.

Exemple :
```
Please enter a prompt to generate an image:
> Un chat assis sous un arbre
```

L'IA Novita va alors améliorer ce prompt pour le rendre plus riche en détails. Par exemple :
```
{"enhanced_prompts": [
    "Un chat majestueux avec un pelage doré est assis sous un vieux chêne, baigné par la lumière dorée du coucher de soleil.",
    "Un chat noir aux yeux émeraude se repose paisiblement sous un arbre en fleurs, alors que des pétales roses tombent doucement autour de lui.",
    "Un chat roux joueur bondit entre les racines noueuses d'un arbre gigantesque dans une forêt mystérieuse, illuminée par une lueur féerique.",
    "Un petit chat tigré s'assoit sous un pommier, contemplant les pommes rouges qui pendent au-dessus de lui, tandis qu'une brise légère fait danser les feuilles.",
    "Un chat siamois au regard perçant est blotti sous un cerisier en fleurs, dans un jardin japonais paisible avec une rivière sinueuse." 
]}
```

## 3. Génération d'images:

Une fois le prompt amélioré, l'IA Nebius utilisera chacun des cinq prompts enrichis pour générer une image.

### 3.1 Processus de génération d'image:
Le programme enverra chaque prompt amélioré à l'IA Nebius pour créer une image. Chaque image sera ensuite enregistrée dans le dossier où se trouve le script sous la forme `output_X.png`.

Exemple de sortie :
```
[GENERATING IMAGE 1/5]
[GENERATING IMAGE 2/5]
[GENERATING IMAGE 3/5]
[GENERATING IMAGE 4/5]
[GENERATING IMAGE 5/5]
```
Les fichiers images seront alors disponibles sous les noms `output_0.png`, `output_1.png`, etc.

### 3.2 Accéder aux images générées:
Après l'exécution du script, vous pourrez voir les images générées dans le dossier du projet. Vous pouvez les ouvrir avec n'importe quel visualiseur d'images pour voir le résultat.

## 4. Problèmes et solutions:

Si vous rencontrez des erreurs lors de l'exécution du script, voici quelques solutions possibles :

### 4.1 Clés d'API non reconnues:
Si vous voyez un message d'erreur indiquant que les clés d'API sont invalides ou absentes, assurez-vous que votre fichier `.env` est bien configuré et contient les clés correctes.
```sh
NOVITA_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NEBIUS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4.2 Problèmes avec l'installation des dépendances:
Si une erreur indique qu'un module est manquant, vérifiez que toutes les dépendances sont bien installées avec :
```sh
pip install -r requirements.txt
```

### 4.3 Erreur JSON:
Si l'IA ne renvoie pas un JSON valide, le programme affichera une erreur. Dans ce cas, vérifiez que votre connexion Internet est stable et que l'API Novita fonctionne correctement.

## 5. Améliorations possibles:

Voici quelques pistes d'amélioration pour le projet :
- Ajouter une interface graphique pour faciliter l'utilisation.
- Permettre à l'utilisateur de choisir parmi plusieurs modèles d'IA pour la génération.
- Sauvegarder un historique des prompts et images générées.
- Ajouter des filtres artistiques aux images générées.
