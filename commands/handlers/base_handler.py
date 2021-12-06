import subprocess
from urllib.parse import urlparse


def strip_scheme(url):
    parsed = urlparse(url)
    scheme = '%s://' % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)


class BaseHandler:
    type = '__base__'

    def __init__(self, base_api, username, password):
        self.base_api = base_api
        self.base_api_without_schema = strip_scheme(base_api)

        self.username = username
        self.password = password

    def autosetup(self, repo_name):
        raise NotImplementedError('Not yet implemented.')

    def teardown(self, repo_name):
        raise NotImplementedError('Not yet implemented.')

    def run_subprocess(self, command):
        try:
            res = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f'Command "{e.cmd}" failed with code "{e.returncode}". Stdout:\n'
                  f'{e.stdout}\nStderr:\n{e.stderr}')
            return None, e

        return res, None
