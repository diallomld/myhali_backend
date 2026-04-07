## I- Description

Back-end du projet portant sur le système d'adressage automatique et basé sur du Django et avec PostgreSQL comme SGBD.
Assurez-vous que python et pip sont installés sur votre machine.
Pour démarrer le projet :

### Installation

Assurez-vous que python et pip sont installés sur votre machine
Cloner le projet

```sh
 git clone https://github.com/cbsBiram/adressage-backend.git
 cd adressage-backend
```

## II- Virtualenv

Chaque environnement virtuel a son propre binaire Python (qui correspond à la version du binaire qui a été utilisée pour créer cet environnement) et peut avoir sa propre liste de paquets Python installés dans ses propres dossiers site. Nous allons utiliser pipenv

#### 1. Install pipenv

```sh
 pip install pipenv
```

### Dépendances

"Pipfile" liste toutes les dépendances nécessaires au projet et qui doivent être installés par un collaborateur.

#### 2. Install the dependancies

```sh
 pipenv install --ignore-pipfile
```

#### 3. Check the virtualenv.

```sh
 pipenv --venv
```

#### 4. Launch the virtualenv (each time)

```sh
 pipenv shell
```

#### 5. List of all the installed dependancies

```sh
 pipenv graph
```

#### 6. To exit

```sh
 exit
```

#### 7. Change the python version in the virtual environment.

```sh
 pipenv --python <version>
```

## IV- Configuration de la base de donnée

Ceci constitue un prérequis au projet.

### 1- Installer PostgreSQL

Aller à la page de téléchargement de PostgreSQL ([ici](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)).
L'installation est assez intuitive mais voici certaines étapes importantes:

<a href="#composantes"><img src="https://miro.medium.com/max/666/1*TtC8dYviJRVivCZ8dkPZLw.png"></a>

Dans l'assistant d'installation de PostgreSQL, dans la page de sélection des composants, décochez les composants que vous ne voulez pas installer, ou laissez-les tels quels (vérifier que _PgAdmin_ est bien coché). Si vous décochez quelque chose, ne vous inquiétez pas, lancez simplement le programme d'installation plus tard et sélectionnez le composant dont vous avez besoin, et PostgreSQL sera mis à jour en conséquence.

<a href="#password"><img src="https://miro.medium.com/max/703/1*f20FS0ubJXLC90DIp5J-Vg.png"></a>

À la page Password, entrez le mot de passe (Entrer root pour le projet) du super-utilisateur de la base de données (postgres). Ce compte sera utilisé pour accéder à votre SQL Shell (pqsl) par la suite.

<a href="#port"><img src="https://miro.medium.com/max/716/1*sDVW-_sk3H91BTfd_zZCJg.png"></a>

Poursuivez avec le reste de l'installation. Pour vérifier l'installation, trouvez le programme SQL Shell (pqsl) et cliquez dessus pour le lancer. La ligne de commande pqsl apparaîtra.

### 2- Tester PostgreSQL

Ouvrez la ligne de commande. Acceptez la valeur par défaut pour les champs Server, Database, Port et Username en appuyant sur Entrée. Toutefois, dans le champ Password, vous devez entrer le mot de passe que vous avez choisi dans l'assistant d'installation.

### 3- Ouvrir PgAdmin et créer une nouvelle base de données du nom de "adressage"

```sh
CREATE DATABASE adressage OWNER postgres;
```

## V- Migrations et démarrage de l'application

### 4- Lancer la migration

```sh
 python manage.py makemigrations
 python manage.py migrate
```

### 5- Lancer l'application

```sh
 python manage.py runserver 0.0.0.0:8000
```

## VI- Branche et versioning du code

### 1- Nouvelle branche

```sh
git branch <Branch_Name>
git branch
git checkout <Branch_Name>
```

### 2- Pour récupérer les changements effectués sur la branche Master

```sh
git pull origin master
```

### 3- Pour pusher les modifications locales

```sh
git add .
git commit -m "<Message>"
git push
```

## VI- Déploiement

### 1- Connexion à Heroku

```sh
heroku login
```

### Staging area

```sh
git add .
git commit -m "<message>"
```

### Déployer le code sur Heroku

```sh
git push heroku master
```

---
