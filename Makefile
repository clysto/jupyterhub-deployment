all: nbimage hubimage sshdimage

nbimage: nbimage/Dockerfile
	cd nbimage && docker build -t jupyter-notebook:latest .

hubimage: hubimage/Dockerfile
	cd hubimage && docker build -t jupyterhub:latest .

sshdimage: sshdimage/Dockerfile
	cd sshdimage && docker build -t sshpiper:latest .

archive: jupyter-notebook.tar jupyterhub.tar sshpiper.tar

jupyter-notebook.tar:
	docker save jupyter-notebook:latest -o archive/jupyter-notebook.tar

jupyterhub.tar:
	docker save jupyterhub:latest -o archive/jupyterhub.tar

sshpiper.tar:
	docker save sshpiper:latest -o archive/sshpiper.tar

clean:
	docker image prune
