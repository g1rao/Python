import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="kubernetes-nginx-deployer",
    version="0.0.1",
    author="Jeevan Rao Talagan",
    author_email="jeevanrao.iiit@gmail.com",
    description=("knd (Kubernetes NGINX Deployer) deploys NGINX on a Kubernetes cluster, and verifies that it has come up healthy."
                "A CLI progress bar is provided to indicate the deployment/scaling progress."
                "The application can be deployed with a configurable number of replicas."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/g1rao/Kubenetes-Nginx-Deployer",
    project_urls={
        "Bug Tracker": "https://github.com/g1rao/Kubenetes-Nginx-Deployer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["halo", "tqdm", "yaml", "kubernetes"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "knd = knd.knd-cli:main",
        ]
    }
)