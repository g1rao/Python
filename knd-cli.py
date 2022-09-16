# CommandLine Interface for Kubernetes NGINX deployer

# Purpose:
#    knd (Kubernetes NGINX deployer) deploys NGINX on a Kubernetes cluster, and verifies that it has come up healthy.
#    A CLI progress bar is provided to indicate the deployment/scaling progress.
#    The application can be deployed with a configurable number of replicas.

__author__ = "Jeevan Rao Talagana"
import sys
import logging
from argparse import ArgumentParser, HelpFormatter
from .knd import KND


def main():
    formatter_class=lambda prog: HelpFormatter(prog,max_help_position=65, width=100)
    parser = ArgumentParser(description='Kubernetes NGINX Deployer',formatter_class=formatter_class)
    parser.add_argument('-r', '--replicas', metavar='<no-of-replicas>', type=int, dest='replicas', default=1, action='store', help='Specify no of replicas')
    parser.add_argument('-n', '--nginx-version', metavar='<nginx-version>', dest='nginx_version', default="latest", action='store', help='Specify nginx version')
    parser.add_argument('-d', '--deployment-name', metavar='<deployment-name>', dest='deployment_name', action='store', help='* Specify deployment name', required=True)
    parser.add_argument('-i', '--deployment-file', metavar='<deployment-file>', dest='deployment_file', default=None, action='store', help='Specify deployment file if any')
    parser.add_argument('-f', '--force', dest='recreate', action='store_true', help='If removes existing deployment with specified name and recreates')
    # parser.add_argument('-r', '--remove-deployment', dest='delete_deployment', action='store_true', help='If specifies it removes given deployment name')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Print debug messages')
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    try:
        replicas = args.replicas
        deployment_name = args.deployment_name
        nginx_version = args.nginx_version
        deployment_file = args.deployment_file
        verbose = args.verbose
        recreate = args.recreate
        knd = KND(deployment_file, deployment_name, nginx_version, replicas, recreate, verbose)
        knd.deploy_nginx()
    except KeyboardInterrupt as e:
        logging.error("KeyboardInterrupt")
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()