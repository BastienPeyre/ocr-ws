# Déploiement sur OpenShift

Ce document explique comment déployer l'application OCR-WS sur une plateforme OpenShift.

## Prérequis

- Accès à un cluster OpenShift
- La commande `oc` (OpenShift CLI) installée
- Compte avec droits suffisants pour créer des ressources dans un projet

## Méthodes de déploiement

### Option 1: Utiliser les fichiers YAML

1. Connectez-vous à votre cluster OpenShift :

```bash
oc login <cluster-url>
```

2. Créez un nouveau projet (si nécessaire) :

```bash
oc new-project ocr-ws
```

3. Créez les secrets avec vos informations sensibles :

```bash
# Encodez vos données sensibles en base64
DJANGO_SECRET_KEY_B64=$(echo -n "votre-cle-secrete-django" | base64)
OCR_API_URL_B64=$(echo -n "https://example.com/api/ocr" | base64)
OCR_API_KEY_B64=$(echo -n "votre-api-key" | base64)

# Créez un fichier temporaire secrets.yaml
cat <<EOF > secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ocr-ws-secrets
type: Opaque
data:
  django-secret-key: $DJANGO_SECRET_KEY_B64
  ocr-api-url: $OCR_API_URL_B64
  ocr-api-key: $OCR_API_KEY_B64
EOF

# Appliquez le fichier secret
oc apply -f secrets.yaml

# Supprimez le fichier temporaire
rm secrets.yaml
```

4. Déployez l'application en utilisant le fichier YAML de déploiement :

```bash
# Modifiez le fichier deployment.yaml pour remplacer ${REGISTRY_URL} par l'URL de votre registre
sed -i 's|${REGISTRY_URL}|image-registry.openshift-image-registry.svc:5000/ocr-ws|g' openshift/deployment.yaml

# Appliquez le fichier de déploiement
oc apply -f openshift/deployment.yaml
```

### Option 2: Utiliser S2I (Source-to-Image)

1. Connectez-vous à votre cluster OpenShift :

```bash
oc login <cluster-url>
```

2. Créez un nouveau projet (si nécessaire) :

```bash
oc new-project ocr-ws
```

3. Créez les mêmes secrets que dans l'option 1.

4. Utilisez S2I pour déployer directement à partir de votre dépôt Git :

```bash
oc new-app python:3.10-ubi8~https://github.com/BastienPeyre/ocr-ws.git --name=ocr-ws

# Créez un service
oc expose deployment ocr-ws --port=8000

# Créez une route
oc create route edge --service=ocr-ws --insecure-policy=Redirect
```

5. Configurez les variables d'environnement pour l'application :

```bash
oc set env deployment/ocr-ws \
  DJANGO_SETTINGS_MODULE=ocr_ws.settings \
  DJANGO_SECRET_KEY="$(oc get secret ocr-ws-secrets -o jsonpath='{.data.django-secret-key}' | base64 --decode)" \
  DEBUG="False" \
  ALLOWED_HOSTS="*" \
  OCR_API_URL="$(oc get secret ocr-ws-secrets -o jsonpath='{.data.ocr-api-url}' | base64 --decode)" \
  OCR_API_KEY="$(oc get secret ocr-ws-secrets -o jsonpath='{.data.ocr-api-key}' | base64 --decode)"
```

6. Configurez les volumes persistants :

```bash
# Créez les PVCs
oc apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ocr-ws-media-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ocr-ws-static-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
EOF

# Montez les volumes dans le déploiement
oc set volume deployment/ocr-ws --add --name=media-volume --type=persistentVolumeClaim --claim-name=ocr-ws-media-pvc --mount-path=/opt/app-root/src/media
oc set volume deployment/ocr-ws --add --name=static-volume --type=persistentVolumeClaim --claim-name=ocr-ws-static-pvc --mount-path=/opt/app-root/src/staticfiles
```

7. Configurez les sondes de vivacité et de préparation :

```bash
oc set probe deployment/ocr-ws --liveness --get-url=http://:8000/api/ocr/ --initial-delay-seconds=30 --timeout-seconds=1 --period-seconds=10
oc set probe deployment/ocr-ws --readiness --get-url=http://:8000/api/ocr/ --initial-delay-seconds=15 --timeout-seconds=1 --period-seconds=5
```

## Vérification du déploiement

1. Vérifiez que tous les pods sont en cours d'exécution :

```bash
oc get pods
```

2. Obtenez l'URL de l'application :

```bash
oc get route ocr-ws-route
```

3. Testez l'API avec curl :

```bash
curl -X POST -F "document=@chemin/vers/le/document.pdf" http://$(oc get route ocr-ws-route -o jsonpath='{.spec.host}')/api/ocr/
```

## Maintenance et mises à jour

Pour mettre à jour l'application vers une nouvelle version :

```bash
# Si vous utilisez S2I
oc start-build ocr-ws

# Si vous utilisez des images Docker
oc set image deployment/ocr-ws ocr-ws=nouvelle-image:tag
```
