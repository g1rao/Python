#Usage: Use one of the following ways
#       python spjb.py --help
#       python spjb.py -u username -p password  -t token -f project
#

import os
import sys
import argparse
import logging as logger
import configparser
import requests

logger.basicConfig(
        level=logger.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')

formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=60)
parser = argparse.ArgumentParser(
                prog='spjb', description="Description:  Sandbox Pipeline Job Builder",
                epilog='Run spjb --help for more information')

parser.add_argument('--user', '-u', dest="username" ,help="user name")
parser.add_argument('--pass', '-p', dest="password" ,help="password")
parser.add_argument('--token', '-t', dest="token" ,help="token")
parser.add_argument("--folder", "-f", dest="project",help="project folder which contains jenkins job config", required=True)




def installPlugin(pluginShortName,header,destination_jenkinsUrl,destination_jenkins_username,destination_jenkins_password):
    #Purpose: install plugins by given pluginShortName on destination jenkins
    logger.info('Installing Plugin for "' + pluginShortName + '" on Jenkins server "' + destination_jenkinsUrl+'"')
    final_url = "{0}/pluginManager/installNecessaryPlugins".format(destination_jenkinsUrl)
    payload = '<jenkins><install plugin="{0}@latest"/></jenkins>'.format(pluginShortName) #Install plugin with latest version API call
    response = requests.post(final_url, data=payload, headers=header, auth=(destination_jenkins_username, destination_jenkins_password),verify=True)
    if response.status_code==200 :  # HTTP
        logger.info('Plugin "' +pluginShortName+'" installed successfully')
    else:
        logger.info('Plugin "' +pluginShortName+'" creation failed')
        logger.info('Plugin Creation Failure status code : ' +str(response.status_code))

def installPluginOnDestination(project,header,destination_jenkinsUrl,destination_jenkins_username,destination_jenkins_password):
    logger.info('Installing plugins on destination jenkins server "'+destination_jenkinsUrl+'"')
    f = open(os.path.join(project,"plugins.txt"))
    pluginList=f.read().split("\n")
    f.close()
    for plugin in pluginList:
        pluginDetails=plugin.strip().split('|')
        pluginShortName=pluginDetails[0]
        installPlugin(pluginShortName,header,destination_jenkinsUrl,destination_jenkins_username,destination_jenkins_password)  #function to install plugin
    logger.info('Installation of plugins on destination jenkins server "'+destination_jenkinsUrl+'" completed')

def getCrumbHeader(jenkinsUrl, jenkinsUser, JenkinsToken):
    # Purpose: create and return crumb header required to trigger remote jenkins build.
    logger.info('Building crumb header')
    crumb_issue_url = "{}/crumbIssuer/api/json".format(jenkinsUrl)
    try:
        crumb_response = requests.get(crumb_issue_url, auth=(jenkinsUser, JenkinsToken),verify=True)
        crumb_dict = crumb_response.json()
        crumb_field = crumb_dict["crumbRequestField"]
        crumb_value = crumb_dict["crumb"]
    except Exception as e:
        logger.error("Failed to retrieve crumb. Cannot make API call to Jenkins in lieu of this. Exception: {}".format(e))
        sys.exit(255)
    headers = {
        "{}".format(crumb_field): "{}".format(crumb_value),
        "Content-Type":"application/xml"
    }
    logger.info('Crumb header build successfully '+ crumb_value)
    return headers

def create_job(username,password,token,project):
    """
    This method is used to create jenkins job
    """
    if not os.path.isdir(project) or os.path.isfile(project):
        logger.error("Specify project directory which contains jenkins job config files.\n")
        sys.exit(255)
    try:
        config_file = os.path.join(project,"conf/spjb.conf")
        config = configparser.ConfigParser()
        config.read(config_file)
        if not username:
            username = config.get('jaas_server_info', 'username').strip(' ')
        if not password:
            password = config.get('jaas_server_info', 'password').strip(' ')
        if not token:
            token = config.get('jaas_server_info', 'token').strip(' ')
        servers = config.get('jaas_server_info', 'servers').strip(' ').strip(',').split(",")
        if username == '':
            logger.error("Please specify username in cli or spjb.ini file.\n")
            sys.exit(255)
        if password == '':
            logger.error("Please specify password in cli or spjb.ini file.\n")
            sys.exit(255)
        if token == '':
            logger.error("Please specify token in cli or spjb.ini file.\n")
            sys.exit(255)
        if len(servers)==1 and servers[0] == '':
            logger.error("Please specify atlease one jass server in spjb.ini file.\n")
            sys.exit(255)
        cred_username = config.get('create_credentials_info','username').strip(' ').strip(',').split(',')
        cred_password = config.get('create_credentials_info','password').strip(' ').strip(',').split(',')
        cred_id = config.get('create_credentials_info','credential_id').strip(' ').strip(',').split(',')
        cred_descri = config.get('create_credentials_info','description').strip(' ').strip(',').split(',')
        num_of_creds = len(cred_username)
        num_of_passwds = len(cred_password)
        if not(num_of_creds ==1 and cred_username[0] == ''):
            if num_of_passwds == 1 and cred_password[0] == '':
                logger.error("Specify only one password or all passwords in create_credential_info")
                sys.exit(255)
            elif num_of_passwds != 1 and num_of_passwds < num_of_creds:
                logger.error("Specify only one password or all passwords in create_credential_info")
                sys.exit(255)
            else:
                cred_password = cred_password * num_of_creds
            if len(cred_id) != num_of_creds:
                logger.error("Specify credential ids of all usernames")
                sys.exit(255)
            if len(cred_descri) != num_of_creds:
                cred_descri = cred_id
        for i in range(len(servers)):
            for j in range(num_of_creds):
                logger.info("Adding credentials to %s"%(servers[i]))
                #create_cred_cmd = ["curl","-X","POST","%s/credentials/store/system/domain/_/createCredentials"%servers[i],\
                #    "--data-urlencode",'\'json={"": "0", "credentials": {"scope": "GLOBAL", "id": "%s", "username": "%s",\
                #    "password": "%s", "description": "%s", "$class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl"\
                #    } }\''%(cred_id[j],cred_username[j],cred_password[j],cred_descri[j]),"--user","%s:%s"%(username,token),"-sSf"]

                create_cred_cmd = """curl -X POST %s/credentials/store/system/domain/_/createCredentials --data-urlencode\
                     'json={"": "0", "credentials": {"scope": "GLOBAL", "id": "%s", "username": "%s","password": "%s", "description": "%s", "$class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl" } }' --user %s:%s -sSf"""%(servers[i],cred_id[j],cred_username[j],cred_password[j],cred_descri[j],username,token)
                os.system(create_cred_cmd)

            jjb_config = """\
                        [job_builder]
                        ignore_cache=True
                        keep_descriptions=False
                        recursive=False
                        allow_duplicates=False
                        [jenkins]
                        user=%s
                        password=%s
                        url=%s
                        query_plugins_info=True"""%(username,password,servers[i])
            jjb_config = jjb_config.replace(" ","")
            project = os.path.abspath(project)
            project_yamls = os.path.join(project,"yamls")
            jjb_config_file = os.path.join(project,"conf","jjb_config.ini")
            with open(jjb_config_file,'w+') as jjb_data:
                jjb_data.writelines(jjb_config)
            header = getCrumbHeader(servers[i], username, password)
            installPluginOnDestination(project,header,servers[i],username,password)
            os.system("jenkins-jobs --conf "+jjb_config_file+" update "+project_yamls)
            logger.info("Donee...!")
    except Exception as e:
        logger.error("\nException Occurred:\n"+str(e)+"\n")
        sys.exit(255)

if __name__=="__main__":
    args=parser.parse_args(sys.argv[1:])
    token = args.token
    username = args.username
    password = args.password
    project = args.project
    create_job(username,password,token,project)
