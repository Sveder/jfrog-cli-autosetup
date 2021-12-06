from handlers.base_handler import BaseHandler


class DockerHandler(BaseHandler):
    type = 'docker'

    def autosetup(self, repo_name):
        command = f'docker login -u {self.username} -p {self.password} ' \
                  f'{self.base_api_without_schema}'

        _, error = self.run_subprocess(command)
        if error:
            return

        print('Docker setup finished successfully. To push a docker run:')
        print(f'docker push {self.base_api_without_schema}<DOCKER_REPOSITORY>:<DOCKER_TAG>')
        print('To pull a docker:')
        print(f'docker pull {self.base_api_without_schema}<DOCKER_REPOSITORY>:<DOCKER_TAG>')

    def teardown(self, repo_name):
        command = f'docker logout {self.base_api_without_schema}'

        _, error = self.run_subprocess(command)
        if error:
            return

        print('Disconnected docker from the artifactory repo.')
