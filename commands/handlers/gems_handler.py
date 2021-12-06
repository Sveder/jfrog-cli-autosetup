from urllib.parse import quote_plus

from handlers.base_handler import BaseHandler


class GemsHandler(BaseHandler):
    type = 'gems'

    def autosetup(self, repo_name):
        encoded_username = quote_plus(self.username)
        command = f'gem source -a https://{encoded_username}:{self.password}@' \
                  f'{self.base_api_without_schema}artifactory/api/gems/gems_test/'

        _, error = self.run_subprocess(command)
        if error:
            return

        repo_url = f'{self.base_api}artifactory/api/gems/gems_test/'
        print('Gems successfully set up. Deploying to this repository can be done by running the '
              'following command:')
        print(f'gem push <PACKAGE> --host {repo_url}')
        print('To resolve a package, run the following command:')
        print(f'gem install <PACKAGE> --source {repo_url}')

    def teardown(self, repo_name):
        encoded_username = quote_plus(self.username)
        command = f'gem source -r https://{encoded_username}:{self.password}@' \
                  f'{self.base_api_without_schema}artifactory/api/gems/gems_test/'

        _, error = self.run_subprocess(command)
        if error:
            return

        print('Disconnected gems from the artifactory repo.')
