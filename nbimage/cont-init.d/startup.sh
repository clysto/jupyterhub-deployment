#!/command/with-contenv sh

export HOME=/home/$MAMBA_USER

echo $JUPYTERHUB_USER >/etc/ssh/ssh_principals
echo $SSH_CA_PUBKEY | base64 -d >/etc/ssh/ssh_ca.pub

if [ -f /home/$MAMBA_USER/.startup ]; then
    /home/$MAMBA_USER/.startup
fi
