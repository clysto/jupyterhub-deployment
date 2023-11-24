import os
from nativeauthenticator.handlers import LocalBase as _LocalBase
from jinja2 import ChoiceLoader, FileSystemLoader
from tornado import web

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


class LocalBase(_LocalBase):
    _template_dir_registered = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not LocalBase._template_dir_registered:
            self.log.debug("Adding %s to template path", TEMPLATE_DIR)
            loader = FileSystemLoader([TEMPLATE_DIR])
            env = self.settings["jinja2_env"]
            previous_loader = env.loader
            env.loader = ChoiceLoader([previous_loader, loader])
            LocalBase._template_dir_registered = True


class UserKeyHandler(LocalBase):
    @web.authenticated
    async def get(self):
        user = await self.get_current_user()
        key = self.authenticator.get_user_key(user.name)
        html = await self.render_template(
            "ssh-key.html",
            key=key,
        )
        self.finish(html)

    @web.authenticated
    async def post(self):
        user = await self.get_current_user()
        key = self.authenticator.create_user_key(user.name)
        html = await self.render_template(
            "ssh-key.html",
            key=key,
        )
        self.finish(html)


class PrivateKeyHandler(LocalBase):
    @web.authenticated
    async def get(self):
        user = await self.get_current_user()
        key = self.authenticator.get_user_key(user.name)
        if key is None:
            raise web.HTTPError(404)
        self.finish(key.private_key)
