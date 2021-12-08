import base64
import pathlib

from handlers.base_handler import BaseHandler


NPMRC_TEMPLATE = """_auth = %s
email = %s
always-auth = true"""


class NpmHandler(BaseHandler):
    type = 'npm'

    def autosetup(self, repo_name):
        url = f'{self.base_api}artifactory/api/npm/npm_test/'
        command = f'npm config set registry={url}'

        _, error = self.run_subprocess(command)
        if error:
            return

        npmrc_path = pathlib.Path.home() / pathlib.Path('.npmrc')
        auth = base64.b64encode(f'{self.username}:{self.password}'.encode()).decode('utf-8')

        with npmrc_path.open('w+') as fobj:
            fobj.write(NPMRC_TEMPLATE % (auth, self.username))

        print('npm successfully set up. Deploying to this repository can be done by running the '
              'following command:')
        print(f'npm publish --registry {url}')
        print('To resolve a package using the npm CLI, run the following command:')
        print(f'npm install <PACKAGE_NAME> --registry {url}')

    def teardown(self, repo_name):
        npmrc_path = pathlib.Path.home() / pathlib.Path('.npmrc')
        if npmrc_path.exists():
            npmrc_path.unlink()

        print('Disconnected npm from the artifactory repo.')
