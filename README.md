# Auto Build Deploy

Ce projet simplifie l'automatisation du déploiement d'une application via un webhook.

## Fonctionnalités

- Déclenchement automatisé des déploiements via webhook
- Mise à jour automatique du dépôt
- Construction d'images Docker à la demande
- Redéploiement sans interruption (presque instantané)

## Prérequis

- Docker
- Docker Compose

## Installation & Configuration

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/c4software/Auto-Build-Deploy.git
   ```
2. Configurez les variables d'environnement dans `docker-compose.yml` :
   - Modifiez `REPO_URL` pour pointer vers votre dépôt.
   - Définissez `RANDOM_PATH_FOR_WEBHOOK` pour personnaliser le chemin du webhook.
3. Démarrez le service :
   ```bash
   docker-compose up -d
   ```

## Utilisation

Le serveur écoute sur le port 8888.  
Pour déclencher le déploiement, effectuez une requête POST vers :
```
http://localhost:8888/<RANDOM_PATH_FOR_WEBHOOK>
```
(Remplacez `<RANDOM_PATH_FOR_WEBHOOK>` par la valeur configurée.)

## Logs & Déploiement

Les logs s'affichent en temps réel dans la console du conteneur, permettant un suivi précis des déploiements.

## Contribuer

Les contributions sont les bienvenues !  

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.