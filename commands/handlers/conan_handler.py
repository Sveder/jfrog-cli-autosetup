import subprocess

from handlers.base_handler import BaseHandler


class ConanHandler(BaseHandler):
    type='conan'

    def autosetup(self, repo_name):
        command = f'conan remote add artifactory-{repo_name} ' \
                  f'{self.base_api}artifactory/api/conan/{repo_name}'

        res = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True,
        )

        command = f'conan user -p {self.password} -r artifactory-{repo_name} {self.username}'

        res = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True,
        )


        print('Conan successfully set up. Deploying to this repository can be done by running the '
              'following command:')
        print(f'conan upload <RECIPE> -r artifactory-{repo_name} --all')
        print('To resolve a package using the conan CLI, run the following command:')
        print(f'conan install . -r artifactory-{repo_name}')


def teardown(self, repo_name):
        command = f'conan remote remove artifactory-{repo_name}'

        res = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True,
        )

        print('Disconnected conan from the artifactory repo.')