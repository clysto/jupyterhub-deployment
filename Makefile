all: nbimage hubimage sshdimage

nbimage: nbimage/Dockerfile
	cd nbimage && docker build -t jupyter-notebook:latest .

hubimage: hubimage/Dockerfile
	cd hubimage && docker build -t jupyterhub:latest .

sshdimage: sshdimage/Dockerfile
	cd sshdimage && docker build -t sshpiper:latest .

clean:
	docker image prune
