# Kubenetes-Nginx-Deployer 

NAME

    knd

SYNOPSIS

    knd [--replicas=replicas] [--nginx-version=version] [deployment-name]

DESCRIPTION

    knd (Kubernetes NGINX deployer) deploys NGINX on a Kubernetes cluster, and verifies that it has come up healthy.

    A CLI progress bar is provided to indicate the deployment/scaling progress.
    
    The application can be deployed with a configurable number of replicas.
    
    A Kubernetes cluster is a prerequisite to using knd, therefore kind (Kubernetes in Docker) is used to bring up a cluster.

    knd will deploy a new cluster using kind if it detects that one isn't already present.

    The following options are available:

    --replicas=replicas
        Deploys the application using the specified number of replicas.

    --nginx-version=version
        Deploys NGINX using the specified version.

    --deployment-name
        The name of the deployment that you will be deploying into the cluster.
