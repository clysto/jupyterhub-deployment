FROM jupyterhub/jupyterhub:4.0.2

RUN python3 -m pip install --no-cache-dir \
    dockerspawner \
    jupyterhub-nativeauthenticator

CMD ["jupyterhub"]
