helm upgrade --install jhub jupyterhub/jupyterhub \
  --namespace jhub \
  --version=3.2.1 \
  --values values.yaml
