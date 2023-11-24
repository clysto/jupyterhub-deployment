from sshkey_tools.keys import RsaPrivateKey
from sshkey_tools.cert import SSHCertificate, CertificateFields
import hashlib
from .orm import UserKeyInfo
from nativeauthenticator import NativeAuthenticator
from .handlers import UserKeyHandler, PrivateKeyHandler
from traitlets import Unicode
import datetime
import base64


class MyAuthenticator(NativeAuthenticator):
    ca_private_key_file = Unicode(
        config=True,
        help=("The path to the CA private key file. "),
    ).tag(default=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ca_private_key = RsaPrivateKey.from_file(self.ca_private_key_file)

    def get_handlers(self, app):
        handlers = super().get_handlers(app)

        handlers.extend(
            [
                (r"/ssh-key", UserKeyHandler),
                (r"/ssh-key-download", PrivateKeyHandler),
            ]
        )
        return handlers

    def sha256_fingerprint(self, data):
        digest = hashlib.sha256(data).digest()
        return digest.hex()

    def generate_rsa_key_pair(self, key_size=2048):
        private_key = RsaPrivateKey.generate(key_size)
        return private_key, private_key.public_key

    def sign_public_key(self, ca_private_key, public_key, key_id, principals):
        cert_fields = CertificateFields(
            serial=0,
            cert_type=1,
            key_id=key_id,
            principals=principals,
            critical_options=[],
            extensions=[
                "permit-X11-forwarding",
                "permit-agent-forwarding",
                "permit-pty",
            ],
            valid_after=datetime.datetime.now(),
            valid_before="forever",
        )
        certificate = SSHCertificate.create(
            subject_pubkey=public_key,
            ca_privkey=ca_private_key,
            fields=cert_fields,
        )
        certificate.header.pubkey_type = "ssh-rsa-cert-v01@openssh.com"
        certificate.sign()
        return certificate

    def get_user_key(self, user):
        user_key_info = UserKeyInfo.find(self.db, user)
        return user_key_info

    def create_user_key(self, user):
        key = self.get_user_key(user)
        if key:
            self.db.delete(key)
            self.db.commit()

        user_private_key, user_public_key = self.generate_rsa_key_pair(4096)
        certificate = self.sign_public_key(
            self._ca_private_key, user_public_key, "user@jupyterhub", [user]
        )
        hash = user_public_key.get_fingerprint(self.sha256_fingerprint)

        user_key_info = UserKeyInfo(
            private_key=user_private_key.to_string(),
            public_key=user_public_key.to_string(),
            certificate=certificate.to_string(),
            fingerprint=hash,
            username=user,
        )

        self.db.add(user_key_info)
        self.db.commit()
        return user_key_info

    def delete_user(self, user):
        key = self.get_user_key(user.name)
        if key:
            self.db.delete(key)
            self.db.commit()
        return super().delete_user(user)
