# bitbucket-deployments-envbuilder

## 1. Overview
*This project goal is provide a way to set up bitbucket deployment environment variables automatically based on .env files. The boring process is gone!*

## 2. Installation
1. Clone this project:
```shell
$ git clone git@github.com:ruanmaia/bitbucket-deployments-envbuilder.git
```
2. Create a python3.8 virtualenv:
```shell
$ cd bitbucket-deployments-envbuilder && virtualenv -p python3.8 --always-copy venv
```
3. Activate the environment:
```shell
$ source venv/bin/activate
```
4. Install pip packages:
```shell
$ pip install -r requirements.txt
```
## 3. Usage
```shell
$ ./bitbucket-deployments-envbuilder sync <filename> -c <oauth_client_id> -s <oauth_secret_key> -u <bitbucket_username> -w <workspace_slug> -r <repository_slug>
```