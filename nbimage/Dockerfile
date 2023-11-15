FROM mambaorg/micromamba

USER $MAMBA_USER
WORKDIR /home/mambauser

RUN micromamba install --name base -c conda-forge --yes \
    'python=3.10' \
    'pytorch-gpu' \
    'gnuradio' \
    'beautifulsoup4' \
    'cython' \
    'ipympl'\
    'ipywidgets' \
    'matplotlib' \
    'numba' \
    'pandas' \
    'scikit-image' \
    'scikit-learn' \
    'scipy' \
    'seaborn' \
    'sympy' \
    'jupyterhub=4.0.2' \
    'notebook' && \
    micromamba clean --all --yes

USER root
RUN rm -rf /etc/apt/sources.list.d/debian.sources && \
    echo "deb http://mirrors.ustc.edu.cn/debian bookworm main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/debian bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/debian-security/ bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    'tmux' \
    'nvtop' \
    'cmake' \
    'build-essential' \
    'openssh-server' \
    'systemd' \
    'htop' \
    'vim' \
    'curl' \
    'wget' \
    'zip' \
    'unzip' \
    'sudo' && \
    rm -rf /var/lib/apt/lists/* && \
    echo "mambauser:mambauser" | chpasswd && adduser mambauser sudo

USER $MAMBA_USER
COPY --chown=mambauser:mambauser .bashrc .profile /home/mambauser/
ENV SHELL /bin/bash

CMD echo mambauser | sudo -S /etc/init.d/ssh restart && jupyterhub-singleuser
