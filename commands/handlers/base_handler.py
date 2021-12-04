class BaseHandler:
    type = '__base__'

    def __init__(self, base_api, username, password):
        self.base_api = base_api
        self.base_api_without_schema = self.base_api[8:]  # Hacky hack to remove https://

        self.username = username
        self.password = password

    def autosetup(self, repo_name):
        raise NotImplementedError('Not yet implemented.')

    def teardown(self, repo_name):
        raise NotImplementedError('Not yet implemented.')
