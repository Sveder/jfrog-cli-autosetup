import click
import requests

from handlers.python_handler import PythonHandler
from handlers.docker_handler import DockerHandler


repo_type_to_handler = {
    'pypi': PythonHandler,
    'docker': DockerHandler,
}


def find_repo_type(repo_name, username, password, base_api):
    res = requests.get(
        f'{base_api}artifactory/api/repositories/{repo_name}',
        auth=requests.auth.HTTPBasicAuth(username, password)
    )
    if res.status_code != 200:
        raise Exception(f'Failed to get {repo_name} info: {res.text}.')

    package_type = res.json()['packageType']
    return package_type


@click.group()
def cli():
    pass


@cli.command()
@click.argument('repo_name')
@click.option('--username')
@click.option('--password')
@click.option('--server-url')
def autosetup(repo_name, username, password, server_url):
    print('user', username, password, server_url)
    repo_type = find_repo_type(repo_name, username, password, server_url)

    if repo_type not in repo_type_to_handler.keys():
        raise Exception(f'Repo {repo_name} does not exist or not supported.')

    handler = repo_type_to_handler[repo_type](server_url, username, password)
    handler.autosetup(repo_name)


if __name__ == '__main__':
    cli()
