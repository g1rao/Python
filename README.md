# Kubenetes-Nginx-Deployer 

NAME

    knd

SYNOPSIS

    knd [-h] [--force] [--list-deployments] [--replicas=replicas] [--nginx-version=version] [-v] [deployment-name]

DESCRIPTION

    knd (Kubernetes NGINX deployer) deploys NGINX on a Kubernetes cluster, and verifies that it has come up healthy.

    A CLI progress bar is provided to indicate the deployment/scaling progress.
    
    The application can be deployed with a configurable number of replicas.
    
    A Kubernetes cluster is a prerequisite to using knd, therefore kind (Kubernetes in Docker) is used to bring up a cluster.

    knd will deploy a new cluster using kind if it detects that one isn't already present.

    The following options are available:

    --list-deployments
        Returns the list of deployments are available.

    --replicas=replicas
        Deploys the application using the specified number of replicas.

    --nginx-version=version
        Deploys NGINX using the specified version.

    --force
        Removes existing deployment with specified name and recreates

    --verbose
        Print debug messages

    --deployment-name
        The name of the deployment that you will be deploying into the cluster.

INSTALLATION

    git clone https://github.com/g1rao/Kubenetes-Nginx-Deployer.git
    cd Kubenetes-Nginx-Deployer
    sudo pip3 install .

    
        jeevan@jeevan-mac ~ % mkdir Code
        jeevan@jeevan-mac ~ % cd Code
        jeevan@jeevan-mac Code % git clone https://github.com/g1rao/Kubenetes-Nginx-Deployer.git
        Cloning into 'Kubenetes-Nginx-Deployer'...
        remote: Enumerating objects: 19, done.
        remote: Counting objects: 100% (19/19), done.
        remote: Compressing objects: 100% (13/13), done.
        remote: Total 19 (delta 2), reused 16 (delta 2), pack-reused 0
        Receiving objects: 100% (19/19), 18.43 KiB | 258.00 KiB/s, done.
        Resolving deltas: 100% (2/2), done.
        jeevan@jeevan-mac Code % cd Kubenetes-Nginx-Deployer
        jeevan@jeevan-mac Kubenetes-Nginx-Deployer % sudo pip3 install .
        Processing /Users/jeevan/Code/Kubenetes-Nginx-Deployer
        Installing build dependencies ... done
        Getting requirements to build wheel ... done
        Installing backend dependencies ... done
        Preparing metadata (pyproject.toml) ... done
        Requirement already satisfied: tqdm in /usr/local/lib/python3.9/site-packages (from kubernetes-nginx-deployer==0.0.1) (4.64.1)
        Requirement already satisfied: PyYAML in /usr/local/lib/python3.9/site-packages (from kubernetes-nginx-deployer==0.0.1) (6.0)
        Requirement already satisfied: halo in /usr/local/lib/python3.9/site-packages (from kubernetes-nginx-deployer==0.0.1) (0.0.31)
        Requirement already satisfied: kubernetes in /usr/local/lib/python3.9/site-packages (from kubernetes-nginx-deployer==0.0.1) (24.2.0)
        Requirement already satisfied: spinners>=0.0.24 in /usr/local/lib/python3.9/site-packages (from halo->kubernetes-nginx-deployer==0.0.1) (0.0.24)
        Requirement already satisfied: log-symbols>=0.0.14 in /usr/local/lib/python3.9/site-packages (from halo->kubernetes-nginx-deployer==0.0.1) (0.0.14)
        Requirement already satisfied: colorama>=0.3.9 in /usr/local/lib/python3.9/site-packages (from halo->kubernetes-nginx-deployer==0.0.1) (0.4.5)
        Requirement already satisfied: six>=1.12.0 in /usr/local/lib/python3.9/site-packages (from halo->kubernetes-nginx-deployer==0.0.1) (1.12.0)
        Requirement already satisfied: termcolor>=1.1.0 in /usr/local/lib/python3.9/site-packages (from halo->kubernetes-nginx-deployer==0.0.1) (1.1.0)
        Requirement already satisfied: google-auth>=1.0.1 in /usr/local/lib/python3.9/site-packages (from kubernetes->kubernetes-nginx-deployer==0.0.1) (2.11.0)
        Requirement already satisfied: requests in /usr/local/lib/python3.9/site-packages (from kubernetes->kubernetes-nginx-deployer==0.0.1) (2.22.0)
        Requirement already satisfied: urllib3>=1.24.2 in /usr/local/lib/python3.9/site-packages (from kubernetes->kubernetes-nginx-deployer==0.0.1) (1.25.11)
        Requirement already satisfied: python-dateutil>=2.5.3 in /usr/local/lib/python3.9/site-packages (from kubernetes->kubernetes-nginx-deployer==0.0.1) (2.8.1)
        Requirement already satisfied: requests-oauthlib in /usr/local/lib/python3.9/site-packages (from kubernetes->kubernetes-nginx-deployer==0.0.1) (1.3.0)
        Requirement already satisfied: setuptools>=21.0.0 in /usr/local/lib/python3.9/site-packages (from kubernetes->kubernetes-nginx-deployer==0.0.1) (59.0.1)
        Requirement already satisfied: websocket-client!=0.40.0,!=0.41.*,!=0.42.*,>=0.32.0 in /usr/local/lib/python3.9/site-packages (from kubernetes->kubernetes-nginx-deployer==0.0.1) (1.4.1)
        Requirement already satisfied: certifi>=14.05.14 in /usr/local/lib/python3.9/site-packages (from kubernetes->kubernetes-nginx-deployer==0.0.1) (2020.12.5)
        Requirement already satisfied: rsa<5,>=3.1.4 in /usr/local/lib/python3.9/site-packages (from google-auth>=1.0.1->kubernetes->kubernetes-nginx-deployer==0.0.1) (4.9)
        Requirement already satisfied: cachetools<6.0,>=2.0.0 in /usr/local/lib/python3.9/site-packages (from google-auth>=1.0.1->kubernetes->kubernetes-nginx-deployer==0.0.1) (5.2.0)
        Requirement already satisfied: pyasn1-modules>=0.2.1 in /usr/local/lib/python3.9/site-packages (from google-auth>=1.0.1->kubernetes->kubernetes-nginx-deployer==0.0.1) (0.2.8)
        Requirement already satisfied: chardet<3.1.0,>=3.0.2 in /usr/local/lib/python3.9/site-packages (from requests->kubernetes->kubernetes-nginx-deployer==0.0.1) (3.0.4)
        Requirement already satisfied: idna<2.9,>=2.5 in /usr/local/lib/python3.9/site-packages (from requests->kubernetes->kubernetes-nginx-deployer==0.0.1) (2.8)
        Requirement already satisfied: oauthlib>=3.0.0 in /usr/local/lib/python3.9/site-packages (from requests-oauthlib->kubernetes->kubernetes-nginx-deployer==0.0.1) (3.1.1)
        Requirement already satisfied: pyasn1<0.5.0,>=0.4.6 in /usr/local/lib/python3.9/site-packages (from pyasn1-modules>=0.2.1->google-auth>=1.0.1->kubernetes->kubernetes-nginx-deployer==0.0.1) (0.4.8)
        Building wheels for collected packages: kubernetes-nginx-deployer
        Building wheel for kubernetes-nginx-deployer (pyproject.toml) ... done
        Created wheel for kubernetes-nginx-deployer: filename=kubernetes_nginx_deployer-0.0.1-py3-none-any.whl size=18887 sha256=6d8f17628ec3bd90219d93dba7e87cc21b938d18b96609f21aeeb7d90b3233cd
        Stored in directory: /Users/jeevan/Library/Caches/pip/wheels/ad/cb/4d/f96317559342947e1824643664411fb1ed3ac6cca1d8a6dd46
        Successfully built kubernetes-nginx-deployer
        Installing collected packages: kubernetes-nginx-deployer
        Successfully installed kubernetes-nginx-deployer-0.0.1


MAN PAGE 
        pandoc README.md -s -t man -o knd.1
        # add path /usr/local/man/ to manpath if it doesn't exists
        MANPATH=/usr/local/man/:$MANPATH; export MANPATH
        man knd
