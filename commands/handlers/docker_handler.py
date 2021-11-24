import subprocess

from handlers.base_handler import BaseHandler


class DockerHandler(BaseHandler):
    type='docker'

    def setup_deploy(self, repo_name):
        pass


    def setup_resolve(self, repo_name):
        res = subprocess.run(
            f'docker login -u {self.username} -p {self.password} {self.base_api_without_schema}',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True,
        )

        print('Docker resolve setup finished successfully. To download a package run:')
        print(f'docker push {self.base_api_without_schema}<DOCKER_REPOSITORY>:<DOCKER_TAG>')
