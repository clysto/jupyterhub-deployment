import docker

c = get_config()

c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.port = 8080

c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"
c.NativeAuthenticator.open_signup = True
c.Authenticator.admin_users = ["admin"]

c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.network_name = "jupyterhub-network"
c.DockerSpawner.image = "jupyter-notebook"
c.DockerSpawner.debug = True
c.DockerSpawner.hub_connect_url = "http://jupyterhub:8080"
c.DockerSpawner.remove = True
# GPU Support
# c.DockerSpawner.extra_host_config = {
#     "device_requests": [
#         docker.types.DeviceRequest(
#             count=-1,
#             capabilities=[["gpu"]],
#         ),
#     ],
# }
c.DockerSpawner.notebook_dir = "/home/mambauser"
c.DockerSpawner.volumes = {"{username}": "/home/mambauser"}
