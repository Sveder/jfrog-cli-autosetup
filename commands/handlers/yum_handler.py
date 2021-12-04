import pathlib
from urllib.parse import quote_plus

from handlers.base_handler import BaseHandler

REPO_CONFIG_TEMPLATE = """[Artifactory]
name=Artifactory
baseurl=https://%s:%s@%sartifactory/yum_test/
enabled=1
gpgcheck=0
"""

class YumHandler(BaseHandler):
    type='yum/rpm'

    def autosetup(self, repo_name):
        config_path = pathlib.Path('/etc/yum.repos.d/artifactory.repo')
        if not config_path.parent.exists():
            config_path.parent.mkdir(parents=True)

        try:
            with config_path.open('w') as config:
                encoded_username = quote_plus(self.username)
                config.write(REPO_CONFIG_TEMPLATE % (
                    encoded_username, self.password, self.base_api_without_schema
                ))
        except PermissionError:
            print('To autosetup a yum/rpm repository you must run the autosetup command '
                  'as root (for example, using sudo).')


    def teardown(self, repo_name):
        config_path = pathlib.Path('/etc/yum.repos.d/artifactory.repo')
        try:
            if config_path.exists():
                config_path.unlink()
        except PermissionError:
            print('To teardown a yum/rpm repository you must run the teardown command '
                  'as root (for example, using sudo).')
