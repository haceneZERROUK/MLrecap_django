#!/bin/bash
set -e

# Récupération des variables d'environnement
set -a
source .env
set +a

# Variables
RESOURCE_GROUP=$RESOURCE_GROUP              # Nom du groupe de ressources
APP_CONTAINER_NAME="groupe2-django-app"          # Nom du conteneur
ACR_NAME=$ACR_NAME              # Nom de ton Azure Container Registry
ACR_IMAGE="django-app:latest"              # Nom de l'image dans le ACR
ACR_URL="$ACR_NAME.azurecr.io"             # URL du registre
CPU="1"                                    # Nombre de CPUs
MEMORY="2"                                 # Mémoire (RAM)
PORT="8800"                                # Port exposé
IP_ADDRESS="Public"                        # Type d'IP (Public ou Private)
LOCATION="francecentral"
DNS_LABEL="app-django-g2"                  # Label DNS pour l'adresse publique
OS_TYPE="Linux"                            # Type d'OS (Linux ou Windows)

# Récupération dynamique des identifiants du ACR
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Suppression du conteneur existant
az container delete --name $APP_CONTAINER_NAME --resource-group $RESOURCE_GROUP -y || true


# Déploiement du conteneur
az container create \
    --name $APP_CONTAINER_NAME \
    --resource-group $RESOURCE_GROUP \
    --image $ACR_URL/$ACR_IMAGE \
    --cpu $CPU \
    --memory $MEMORY \
    --location $LOCATION \
    --registry-login-server $ACR_URL \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --ports $PORT \
    --ip-address $IP_ADDRESS \
    --os-type $OS_TYPE \
    --dns-name-label $DNS_LABEL \
    --environment-variables \
        DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
        MOVIES_FILE_PATH=$MOVIES_FILE_PATH \
        USERNAME=$USERNAME \
        EMAIL=$EMAIL \
        PASSWORD=$PASSWORD \
        API_URL=$API_URL \
        ACCESS_TOKEN=$ACCESS_TOKEN \
        DATABASE_NAME=$DATABASE_NAME \
        DATABASE_USERNAME=$DATABASE_USERNAME \
        DATABASE_PASSWORD=$DATABASE_PASSWORD \
        DATABASE_HOST=$DATABASE_HOST \
        DATABASE_PORT=$DATABASE_PORT \
        ACCOUNT_NAME=$ACCOUNT_NAME \
        ACCOUNT_KEY=$ACCOUNT_KEY \
        CONTAINER_NAME=$CONTAINER_NAME \
        saving_file=$saving_file \
        RESOURCE_GROUP=$RESOURCE_GROUP \
        ACR_NAME=$ACR_NAME 

# Affichage des informations
echo "Le déploiement terminé."


