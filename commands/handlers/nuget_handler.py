import subprocess


from handlers.base_handler import BaseHandler


class NugetHandler(BaseHandler):
    type='nuget'

    def autosetup(self, repo_name):
        command = f'nuget sources Add -Name Artifactory-{repo_name} ' \
                  f'-Source {self.base_api}artifactory/api/nuget/{repo_name} ' \
                  f'-username {self.username} -password {self.password}'

        res = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True,
        )

        print('Nuget successfully set up. Deploying to this repository can be done by running the '
              'following command:')
        print(f'nuget push <PACKAGE_NAME> -Source Artifactory-{repo_name}')
        print('To resolve a package using the NuGet CLI, run the following command:')
        print(f'nuget install <PACKAGE_NAME> -Source Artifactory-{repo_name}')


    def teardown(self, repo_name):
        command = f'nuget sources Remove -Name Artifactory-{repo_name}'

        res = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True,
        )

        print('Disconnected nuget from the artifactory repo.')