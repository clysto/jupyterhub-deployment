FROM mambaorg/micromamba

ARG S6_OVERLAY_VERSION=3.1.6.0
ARG JUPYTERHUB_VERSION=4.0.2

# install conda packages using MAMBA_USER
USER $MAMBA_USER
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
    "jupyterhub=${JUPYTERHUB_VERSION}" \
    'notebook' && \
    micromamba clean --all --yes

# install apt packages using root
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
    'htop' \
    'vim' \
    'curl' \
    'wget' \
    'zip' \
    'unzip' \
    'sudo' \
    'git' \
    'locales' && \
    rm -rf /var/lib/apt/lists/* 

# set locale
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG=en_US.utf8

# set default password for MAMBA_USER and enable ssh
RUN echo "mambauser:mambauser" | chpasswd && \
    adduser mambauser sudo && \
    ssh-keygen -A && \
    mkdir /run/sshd

# add s6-overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

# copy s6 services
COPY services.d/ /etc/services.d/
COPY cont-init.d/ /etc/cont-init.d/

CMD ["/init"]
