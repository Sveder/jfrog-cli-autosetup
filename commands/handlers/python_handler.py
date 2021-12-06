import pathlib
import configparser

from handlers.base_handler import BaseHandler


class PythonHandler(BaseHandler):
    type = 'pypi'

    def autosetup(self, repo_name):
        self.setup_deploy(repo_name)
        self.setup_resolve(repo_name)

    def setup_deploy(self, repo_name):
        pypirc_path = pathlib.Path.home() / pathlib.Path('.pypirc')

        cp = configparser.ConfigParser()
        cp.read(pypirc_path)

        repo_section_name = f'artifactory-{repo_name}'

        if 'distutils' not in cp.sections():
            cp['distutils'] = {
                'index-servers': f'artifactory-{repo_name}'
            }
        else:
            cur_distutils = cp['distutils']['index-servers']
            if repo_section_name not in cur_distutils.split('\n'):
                cur_distutils += f'\nartifactory-{repo_name}'
                cp['distutils']['index-servers'] = cur_distutils

        cp[repo_section_name] = {
            'repository': f'{self.base_api}artifactory/api/pypi/{repo_name}',
            'username': self.username,
            'password': self.password,
        }

        with pypirc_path.open('w+') as writable_pypirc:
            cp.write(writable_pypirc)

        print('Python deploy setup finished successfully. To upload a package run:')
        print(f'python setup.py sdist upload -r {repo_section_name}')

    def setup_resolve(self, repo_name):
        pip_conf_path = pathlib.Path.home() / pathlib.Path('.pip') / pathlib.Path('pip.conf')

        if not pip_conf_path.parent.exists():
            pip_conf_path.parent.mkdir(parents=True)

        cp = configparser.ConfigParser()
        cp.read(pip_conf_path)

        url = self._get_pypi_repo_url(repo_name)
        config = {'extra-index-url': url}

        if 'global' in cp.sections() and 'index_url' not in cp['global']:
            config.update({'index-url': 'https://pypi.org/simple'})

        cp['global'] = config

        with pip_conf_path.open('w+') as writable_pip_conf:
            cp.write(writable_pip_conf)

        print('Python resolve setup finished successfully. To download a package run:')
        print('pip install <package_name>')

    def teardown(self, repo_name):
        pip_conf_path = pathlib.Path.home() / pathlib.Path('.pip') / pathlib.Path('pip.conf')
        if pip_conf_path.exists():
            pip_conf_path.unlink()

        pypirc_path = pathlib.Path.home() / pathlib.Path('.pypirc')
        if pypirc_path.exists():
            pypirc_path.unlink()

        print('Disconnected pip from the artifactory repo.')

    def _get_pypi_repo_url(self, repo_name):
        return f'https://{self.username}:{self.password}@' \
               f'{self.base_api_without_schema}artifactory/api/pypi/{repo_name}/simple'
