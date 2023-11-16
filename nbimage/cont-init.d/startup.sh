#!/command/with-contenv sh

export HOME=/home/$MAMBA_USER

if [ -f /home/$MAMBA_USER/.startup ]; then
    /home/$MAMBA_USER/.startup
fi
