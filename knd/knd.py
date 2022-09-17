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
from progress_bar import ProgressBar

class KND:
    """ Kubernetes NGINX Deployer """
    def __init__(self, deployment_name, nginx_version, replicas, force_recreate=False, listing=False, verbose=False):
        self.deployment_file = None  # As per requirement cli option commented
        self.deployment_name = deployment_name
        self.deployment_namespace = "default"
        self.force_recreate = force_recreate
        self.listing = listing
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

    def get_deployment_template(self, image, nginx_version, port, deployment_name):
        """ Generates nginx deployment template"""
        try:
            # deployment_file is None, as we are not focussing on yaml based deployment
            if self.deployment_file and os.path.isfile(self.deployment_file):
                with open(self.deployment_file) as _nginx_data:
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

            logging.info(f"Deployment {deployment_name} is being created...")
            self.cluster_status(k8s_api_client, deployment_name, replicas, deployment_namespace="default")
            logging.info(f"Deployment {deployment_name} has been created and ready to use...")

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

    def scale_replicas(self, k8s_api_client, deployment_name, replicas, deployment_namespace="default"):
        """ Scales up/down with number of replicas """
        try:
            if self.get_replica_count(k8s_api_client, deployment_name) == replicas:
                logging.info(f"Deployment {deployment_name} exists and already scaled to {replicas}")
                return
            api_response = k8s_api_client.patch_namespaced_deployment_scale(deployment_name,
                                                deployment_namespace,
                                                {'spec': {'replicas': replicas}})
            logging.info(f"Deployment is being scaled to {replicas}")
            self.cluster_status(k8s_api_client, deployment_name, replicas, deployment_namespace="default")
            logging.debug(api_response)
            logging.info(f"Deployment is scaled to {replicas}")
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
        logging.info(f"Deployment {deployment_name} is being deleted.")
        while True:
            try:
                deployment = k8s_api_client.delete_namespaced_deployment(
                    name=deployment_name,
                    namespace=deployment_namespace,
                    body=client.V1DeleteOptions(propagation_policy="Foreground", grace_period_seconds=5),
                    )
            except ApiException:
                break
        logging.info(f"Deployment {deployment_name} has been deleted.")

    def update_deployment(self, k8s_api_client, nginx_deployment, nginx_version, deployment_name, replicas, deployment_namespace="default"):
        """ Updates image of specific deployment"""
        try:
            logging.info(f"Updating container image to nginx:{self.nginx_version}")
            nginx_deployment.spec.template.spec.containers[0].image =f"nginx:{nginx_version}"
            update_resp = k8s_api_client.patch_namespaced_deployment(
                name=deployment_name, namespace=deployment_namespace, body=nginx_deployment)
            logging.info(f"Deployment is being updated to nginx:{nginx_version}")
            self.cluster_status(k8s_api_client, deployment_name, replicas, deployment_namespace="default")
            logging.info(f"Deployment image is updated to nginx:{nginx_version}")

        except ApiException as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error("Failed to update nginx version")

    @ProgressBar.progress_bar()
    def cluster_status(self, k8s_api_client, deployment_name, replicas, deployment_namespace="default"):
        try:
            while True:
                response = k8s_api_client.read_namespaced_deployment_status(name=deployment_name, namespace=deployment_namespace)
                if response.status.available_replicas != replicas:
                    time.sleep(5)
                else:
                    break
        except Exception as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error("Failed to get deployment status")

    def list_deployments(self, k8s_api_client, deployment_namespace="default"):
        """ Lists all deployments """
        deployment_list = k8s_api_client.list_namespaced_deployment(namespace="default")
        print(f"{'DeploymentName':<30}{'Image':<30}{'Replicas':<30}")
        deployments = {}
        for item in deployment_list.items:
            if item.spec.selector.match_labels['app'] == "nginx":
                deployments.update({item.metadata.name: [item.spec.template.spec.containers[0].image, item.status.available_replicas]})
                print(f"{item.metadata.name:<30}{item.spec.template.spec.containers[0].image:<30}{item.status.available_replicas!s:<30}")
        return deployments

    def deploy_nginx(self):
        """ Driver method and invocation starts from here. """
        try:
            all_deployments = self.list_deployments(self.k8s_api_client)
            if self.listing:
                return
            nginx_deployment = self.get_deployment_template(self.image, self.nginx_version, self.port, self.deployment_name)
            if self.deployment_name in all_deployments:
                logging.info(f"{self.deployment_name} is already exists.")
                if all_deployments[self.deployment_name][0] != f"nginx:{self.nginx_version}":
                    self.update_deployment(self.k8s_api_client, nginx_deployment, self.nginx_version, self.deployment_name, self.replicas)
                    self.list_deployments(self.k8s_api_client)
                if all_deployments[self.deployment_name][1] != self.replicas:
                    self.scale_replicas(self.k8s_api_client, self.deployment_name, self.replicas)
                    self.list_deployments(self.k8s_api_client)

                if (all_deployments[self.deployment_name][0] == f"nginx:{self.nginx_version}" and all_deployments[self.deployment_name][1] == self.replicas) and not self.force_recreate:
                    logging.info("No changes made to cluster...")
                if self.force_recreate:
                    self.delete_deployment(self.k8s_api_client, self.deployment_name)
                    self.list_deployments(self.k8s_api_client)
                    self.create_deployment(self.k8s_api_client, nginx_deployment, self.deployment_name, self.deployment_namespace, self.replicas)
                    self.list_deployments(self.k8s_api_client)
            else:
                self.create_deployment(self.k8s_api_client, nginx_deployment, self.deployment_name, self.deployment_namespace, self.replicas)
                self.list_deployments(self.k8s_api_client)

        except Exception as E:
            logging.debug(format_exc())
            logging.error(E)
            logging.error("Failed to deploy nginx service.")
