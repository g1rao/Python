# Purpose:
#    knd (Kubernetes NGINX Deployer) deploys NGINX on a Kubernetes cluster, and verifies that it has come up healthy.
#    A CLI progress bar is provided to indicate the deployment/scaling progress.
#    The application can be deployed with a configurable number of replicas.

__author__ = "Jeevan Rao Talagana"
import os
import time
import yaml
import logging
from traceback import format_exc
from kubernetes import client, config
from kubernetes.client.rest import ApiException

DEPLOYMENT_NAME = "nginx-deployment"

class KND:
    """ Kubernetes NGINX Deployer """
    def __init__(self, deployment_file, deployment_name, nginx_version, replicas, recreate=False, verbose=False):
        self.deployment_file = deployment_file
        self.deployment_name = deployment_name
        self.deployment_namespace = "default"
        self.recreate = recreate
        self.nginx_version = nginx_version
        self.replicas = replicas
        self.port = 80
        self.image = "nginx"
        log_level = logging.INFO
        if verbose: log_level = logging.DEBUG
        logging.basicConfig(level=log_level, 
                            format='[%(asctime)s] %(levelname)s: %(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S %p')

        config.load_kube_config()
        self.k8s_api_client = client.AppsV1Api()
        if not self.nginx_version: self.nginx_version = "latest"


    def validate_nginx_deployment_yaml(self, deployment_file):
        """ Validates given nginx deployment yaml"""
        ##### not validating the yaml file as mentioned not to validate in problem statement
        return True

    def get_deployment_template(self, deployment_file, image, nginx_version, port, deployment_name):
        """ Generates nginx deployment template"""
        try:
            if deployment_file and os.path.isfile(deployment_file):
                with open(deployment_file) as _nginx_data:
                    nginx_deployment = yaml.safe_load(_nginx_data)
            else:
                nginx_deployment = self.create_default_nginx_deployment(image, nginx_version, port, deployment_name)

            return nginx_deployment
        except Exception as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error("Failed to generate deployment template")

    def create_default_nginx_deployment(self, image, nginx_version, port, deployment_name):
        """ Creates default nginx deployment configuration """
        try:
            container = client.V1Container(
                            name="nginx",
                            image=f"{image}:{nginx_version}",
                            ports=[client.V1ContainerPort(container_port=port)],
                            resources=client.V1ResourceRequirements(
                                        requests={"cpu": "100m", "memory": "200Mi"},
                                        limits={"cpu": "500m", "memory": "500Mi"},
                                        )
                        )
            template = client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "nginx"}),
                spec=client.V1PodSpec(containers=[container]))
            spec = client.V1DeploymentSpec(replicas=self.replicas, template=template, selector={"matchLabels": {"app": "nginx"}} )
            deployment = client.V1Deployment(
                            api_version="apps/v1",
                            kind="Deployment",
                            metadata=client.V1ObjectMeta(name=deployment_name),
                            spec=spec)
            return deployment
        except Exception as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error("Failed to generate the nginx deployment template")

    def create_deployment(self, k8s_api_client, deployment, deployment_name, deployment_namespace, replicas):
        """ Creates deployment with specified deployment name"""
        try:
            deployment_response = k8s_api_client.create_namespaced_deployment(
                        body=deployment, namespace=deployment_namespace)

            while True:
                response = k8s_api_client.read_namespaced_deployment_status(name=deployment_name, namespace=deployment_namespace)
                if response.status.available_replicas != replicas:
                    print("Waiting for Deployment to become ready...")
                    time.sleep(5)
                else:
                    break
            logging.info(f"Deployment {deployment_response.metadata.name} has been created.")

        except Exception as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error("Failed to create deployment")

    def get_replica_count(self, k8s_api_client, deployment_name, deployment_namespace="default"):
        """ Return replicas count """
        try:
            response = k8s_api_client.read_namespaced_deployment_status(name=deployment_name, namespace=deployment_namespace)
            return response.status.available_replicas
        except ApiException as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error(f"Failed to retrive replica count for the deployment: {deployment_name}")

    def scale_replicas(self, k8s_api_client, deployment_name, deployment_namespace, replicas):
        """ Scales up/down with number of replicas """
        try:
            if self.get_replica_count(k8s_api_client, deployment_name) == replicas:
                logging.info(f"Already scaled to {replicas}")
                return
            api_response = k8s_api_client.patch_namespaced_deployment_scale(deployment_name,
                                                deployment_namespace,
                                                {'spec': {'replicas': replicas}})
            while True:
                response = k8s_api_client.read_namespaced_deployment_status(name=deployment_name, namespace=deployment_namespace)
                if response.status.available_replicas != replicas:
                    print("Waiting for Deployment to become ready...")
                    time.sleep(5)
                else:
                    break
            logging.info(api_response)
        except Exception as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error(f"Failed to scale the deployment-{deployment_name} by {replicas}")

    def check_deployment(self, k8s_api_client, deployment_name, deployment_namespace="default"):
        """ Check if deployment is available in specified deployment namespace""" 
        try:
            deployment = k8s_api_client.read_namespaced_deployment(namespace=deployment_namespace, name=deployment_name)
            # deployment = self.k8s_api_client.list_namespaced_deployment(namespace=self.deployment_namespace, name=self.deployment_name)
            return True
        except ApiException as E:
            logging.warning(f"Seem {deployment_name} doesn't exists in {deployment_namespace}")
        return False

    def delete_deployment(self, k8s_api_client, deployment_name, deployment_namespace="default"):
        """ Delete deployment """
        try:
            deployment = k8s_api_client.delete_namespaced_deployment(
                name=deployment_name,
                namespace=deployment_namespace,
                body=client.V1DeleteOptions(propagation_policy="Foreground", grace_period_seconds=5),
                )
            logging.info(f"Deployment {deployment_name} has been deleted.")
        except ApiException as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error(f"Failed to delete deployment: {deployment_name}")
        return False

    def deploy_nginx(self):
        """ Driver method and invocation starts from here. """
        try:
            deploy = self.check_deployment(self.k8s_api_client, self.deployment_name)
            if self.recreate and deploy:
                self.delete_deployment(self.k8s_api_client, self.deployment_name)
            if not deploy:
                nginx_deployment = self.get_deployment_template(self.deployment_file, self.image, self.nginx_version, self.port, self.deployment_name)
                self.create_deployment(self.k8s_api_client, nginx_deployment, self.deployment_name, self.deployment_namespace, self.replicas)
            else:
                self.scale_replicas(self.k8s_api_client, self.deployment_name, self.deployment_namespace, self.replicas)

        except Exception as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error("Failed to deploy nginx service.")
