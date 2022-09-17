# CommandLine Interface for Kubernetes NGINX deployer

# Purpose:
#    knd (Kubernetes NGINX deployer) deploys NGINX on a Kubernetes cluster, and verifies that it has come up healthy.
#    A CLI progress bar is provided to indicate the deployment/scaling progress.
#    The application can be deployed with a configurable number of replicas.

__author__ = "Jeevan Rao Talagana"
import sys
import logging
from argparse import ArgumentParser, HelpFormatter
from knd import KND


def main():
    formatter_class=lambda prog: HelpFormatter(prog,max_help_position=70, width=120)
    parser = ArgumentParser(description='Kubernetes Nginx Deployer',formatter_class=formatter_class)
    parser.add_argument('-f', '--force', dest='force_recreate', action='store_true', help='Removes existing deployment with specified name and recreates')
    parser.add_argument('-l', '--list-deployments', dest='list_deployments', action='store_true', help='List the deployements')
    parser.add_argument('-n', '--nginx-version', metavar='<nginx-version>', dest='nginx_version', default="latest", action='store', help='Specify nginx version')
    parser.add_argument('-r', '--replicas', metavar='<no-of-replicas>', type=int, dest='replicas', default=1, action='store', help='Specify no of replicas')
    # parser.add_argument('-i', '--deployment-file', metavar='<deployment-file>', dest='deployment_file', default=None, action='store', help='Specify deployment file if any')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Print debug messages')
    parser.add_argument("deployment_name",metavar='deployment-name', default="nginx-deployment", action='store', help='Specify deployment name', nargs='?')
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    try:
        replicas = args.replicas
        deployment_name = args.deployment_name
        nginx_version = args.nginx_version
        # deployment_file = args.deployment_file
        verbose = args.verbose
        list_deployments = args.list_deployments
        force_recreate = args.force_recreate
        knd = KND(deployment_name, nginx_version, replicas, force_recreate, list_deployments, verbose)
        knd.deploy_nginx()
    except KeyboardInterrupt as e:
        logging.error("KeyboardInterrupt")
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()