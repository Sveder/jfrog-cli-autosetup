from handlers.base_handler import BaseHandler


class ConanHandler(BaseHandler):
    type='conan'

    def autosetup(self, repo_name):
        command = f'conan remote add artifactory-{repo_name} ' \
                  f'{self.base_api}artifactory/api/conan/{repo_name}'

        _, error = self.run_subprocess(command)
        if error:
            return

        command = f'conan user -p {self.password} -r artifactory-{repo_name} {self.username}'

        _, error = self.run_subprocess(command)
        if error:
            return

        print('Conan successfully set up. To deploy a recipe:')
        print(f'conan upload <RECIPE> -r artifactory-{repo_name} --all')
        print('To install the dependencies defined in your project\'s conanfile.txt')
        print(f'conan install . -r artifactory-{repo_name}')


    def teardown(self, repo_name):
        command = f'conan remote remove artifactory-{repo_name}'

        _, error = self.run_subprocess(command)
        if error:
            return

        print('Disconnected conan from the artifactory repo.')
