# Setup host machine for Docker (Ubuntu 22.04 LTS)

Steps required to prepare the host machine to run the app with Docker and integrate into CI.
This documentation will use `nginx` as a webserver however, there is no strict requirement for nginx and other 
webservers can be used (such as Apache). Most of what is described here is not a strict requirement and can be done 
in a variety of ways and can be adjusted to work with a different OS. 

**NOTE** this documentation may be out of date, as it is highly coupled to upstream particularities (OS, docker, nginx etc.)
that can and will change with every update. 

## Prerequisites:

- Ubuntu 22.04+ installed
- Security hardening setup in place (disable root login, firewall, etc.)
- Automatic upgrade in place (e.g. unattended-upgrades service)

## Install docker and webserver (nginx)

1. Update existing sources and packages, reboot machine after if necessary:
    ```shell
    sudo apt update
    sudo apt upgrade
    ```
1. Install nginx:
    ```shell
    sudo apt install nginx
    ```
1. Install `docker` and `docker-compose-plugin`. See [official docs](https://docs.docker.com/engine/install/ubuntu/) 
for up-to-date documentation.
1. Make sure docker and nginx are running:
   ```shell
   sudo systemctl status nginx
   sudo systemctl status docker
   ```
1. Create a docker user group, in case it was not created automatically
(more details in [official docs](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)):
    ```shell
    sudo groupadd docker
    ```
   
## Create user for running the app

Create a new user for the app and add it to the docker group. Any name can be used, in this example we are using `desi`:

   ```shell
   sudo useradd --shell /bin/bash --create-home --home-dir /var/local/desi/ --groups docker desi    
   ```

Alternatively, if the user already exists, simply add it to the docker group:

   ```shell
   sudo usermod -aG docker desi   
   ```

## Setup nginx

Setup main nginx configuration for the host together with a SSL certificate. 
See example configuration [here](../config/host-example.nginx.conf) 

## Install a new self-hosted GitHub actions runner

1. Create a directory for the actions runner and change ownership to the app user:
   ```shell
   sudo mkdir /var/local/actions-runner/
   sudo chown desi.desi /var/local/actions-runner/
   ```
1. Log in as the new user and change directory to newly created one:
   ```shell
   sudo su - desi
   cd /var/local/actions-runner/   
   ```
1. Follow the steps [here](https://github.com/digital-agenda-data/digital-agenda/settings/actions/runners/new) to 
install a new self-hosted runner. Make sure to add a label to identify when setting up the deployment workflow when configuring:
   ```shell
   ./config.sh --url https://github.com/digital-agenda-data/digital-agenda --token [REDACTED]
   
   --------------------------------------------------------------------------------
   |        ____ _ _   _   _       _          _        _   _                      |
   |       / ___(_) |_| | | |_   _| |__      / \   ___| |_(_) ___  _ __  ___      |
   |      | |  _| | __| |_| | | | | '_ \    / _ \ / __| __| |/ _ \| '_ \/ __|     |
   |      | |_| | | |_|  _  | |_| | |_) |  / ___ \ (__| |_| | (_) | | | \__ \     |
   |       \____|_|\__|_| |_|\__,_|_.__/  /_/   \_\___|\__|_|\___/|_| |_|___/     |
   |                                                                              |
   |                       Self-hosted runner registration                        |
   |                                                                              |
   --------------------------------------------------------------------------------
   
   # Authentication
   
   √ Connected to GitHub
   
   # Runner Registration
   
   Enter the name of the runner group to add this runner to: [press Enter for Default] 
   
   Enter the name of runner: [press Enter for desi-test] 
   
   This runner will have the following labels: 'self-hosted', 'Linux', 'X64' 
   Enter any additional labels (ex. label-1,label-2): [press Enter to skip] desi-test
   
   √ Runner successfully added
   √ Runner connection is good
   
   # Runner settings
   
   Enter name of work folder: [press Enter for _work] 
   
   √ Settings Saved.
   
   ```
1. Configuring the self-hosted runner application as a service under the app user. 
See [official documentation](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/configuring-the-self-hosted-runner-application-as-a-service).
   ```shell
   # first logout from the app user, since it will not have sudo permissions 
   logout
   cd /var/local/actions-runner/
   sudo ./svc.sh install desi 
   ```
2. Start the service:
   ```shell
   sudo ./svc.sh start
   ```
   
## Install app

The app should be ready to install now in the app folder `/var/local/desi/`. See [install instructions](./install_docker.md).
