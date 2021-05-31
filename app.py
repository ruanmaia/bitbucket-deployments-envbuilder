
#### LIBRARIES IMPORT
import click
import requests

from loguru import logger
from dotenv import dotenv_values


#### DEFAULT CLI GROUP
@click.group()
def cli(): pass


@cli.command('sync')
@click.option('-c', '--oauth-consumer-key', required=True, prompt=True)
@click.option('-s', '--oauth-secret-key', required=True, prompt=True)
@click.option('-u', '--username', required=True, prompt=True)
@click.option('-p', '--password', required=True, prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('-w', '--workspace-slug', required=True, prompt=True)
@click.option('-r', '--repo-slug', required=True, prompt=True)
@click.argument('filename', type=click.Path(exists=True))
def sync(
    oauth_consumer_key, 
    oauth_secret_key, 
    username, 
    password, 
    workspace_slug,
    repo_slug,
    filename
    ):
    
    click.secho("\nBitbucket environment variables synchronization script started!!\n", fg='white', bg='magenta', bold=True)

    # Loading environment variables from file
    click.secho('Loading variables from file %s ... ' % filename, nl=False)
    config = dotenv_values(filename)
    click.secho('OK', fg='green', bold=True)

    # Getting Bitbucket Access Token
    try:
        click.secho('Bitbucket API access validation... ', nl=False)
        r = requests.post(
            'https://bitbucket.org/site/oauth2/access_token', 
            auth=(
                oauth_consumer_key, 
                oauth_secret_key
            )
            ,
            data={
                'grant_type': 'password',
                'username'  : username,
                'password'  : password
            }
        )
        ACCESS_TOKEN = r.json()['access_token']
        API_BASE_URL = 'https://api.bitbucket.org'
        click.secho('OK', fg='green', bold=True)

        with requests.Session() as s:

            # Authorization access token setup
            s.headers.update({ 'Authorization': 'Bearer ' + ACCESS_TOKEN })
            
            # Getting available deployment environments
            click.secho('Getting available deployment environments... ', nl=False)
            r = s.get(
                '{}/2.0/repositories/{}/{}/environments/'.format(
                    API_BASE_URL,
                    workspace_slug,
                    repo_slug
                )
            )
            click.secho('OK', fg='green', bold=True)

            click.secho('Synchronizing variables with available deployments environments...')            
            for deployment_environment in r.json()['values']:

                click.secho(
                    "\n%s %s: \n" % (deployment_environment['name'], deployment_environment['uuid']), 
                    fg='yellow', bold=True
                )
                for key, value in config.items():

                    click.secho("    %s -> %s" % (key, value), fg='white')
                    r = s.post(
                        '{}/2.0/repositories/{}/{}/deployments_config/environments/{}/variables'.format(
                            API_BASE_URL,
                            workspace_slug,
                            repo_slug,
                            deployment_environment['uuid']
                        ),
                        json={
                            'key'       : key,
                            'value'     : value,
                            'secured'   : False
                        }
                    )
            
            click.secho("\n\nSynchronization succeed!\n", fg='green', bold=True)

    except:
        click.secho('ERROR', fg='red', bold=True)
        logger.exception('what?')