#!/user/env python3

import ldap
import re
import csv
import sys


ldap_config = {
    'server': r'',
    'username': r'',
    'password': r'',
    'domains': r''
}


connect = ldap.initialize(ldap_config['server'], bytes_mode=False)
connect.simple_bind_s(ldap_config['username'], ldap_config['password'])


def user_info(query, **kwargs):
    if 'Justin' in query:
        print("?")
    resId = connect.search("DC=cable,DC=comcast,DC=com", ldap.SCOPE_SUBTREE, query, None)
    res = connect.result(resId, 1)

    if 'manager' in kwargs:
        for info in res[1]:
            if info[1]['manager'][0] == kwargs['manager']:
                return info[1]
    else:
        info = res[1][0][1]
        return info

def find_direct_reports(user):
    direct_reports = user['directReports']
    if 'mdaloi200' in user['sAMAccountName'][0].decode('ascii'):
        print('found!')
    users = []
    for d in direct_reports:
        try:
            drep = d.decode('ascii')
            m = re.search('CN=(.+?),OU', drep)
            cn = m.group(1).replace("\\", "")
            u = user_info("CN={}*".format(cn), manager=user['distinguishedName'][0])
            users.append(u)
        except:
            pass
    return users


app_reports = []
def traverse(user):
    if not user:
        return
    if 'directReports' in user:
        reps = find_direct_reports(user)
        for rep in reps:
            app_reports.append(rep)
            traverse(rep)


def write_csv(filepath):
    with open(filepath, "w") as csvfile:
        fields = ["ntid", "email", "manager"]
        writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for user in app_reports:
            if user:
                ntid = user['sAMAccountName'][0].decode('ascii')
                mail = ''
                if 'mail' in user:
                    mail = user['mail'][0].decode('ascii')
                manager = user['manager'][0].decode('ascii')
                m = re.search('CN=(.+?),OU', manager)
                manager_name = m.group(1)

                status = 'U'
                if 'ComcastEmployeeStatus' in user:
                    status = user['ComcastEmployeeStatus'][0].decode('ascii')
                    if status == 'A':
                        writer.writerow({'ntid': ntid, 'email': mail, 'manager': manager_name})


def main(query):
    target = user_info("sAMAccountName={}*".format(query))
    # target = user_info("CN=Lang, Richard*")
    traverse(target)
    write_csv("output.csv")
    print("DONE!...\t {}".format(len(app_reports)))
    print(len(app_reports))

    
TARGET_SAM_ACCOUNT_NAME = ''

if __name__=='__main__':
    main(TARGET_SAM_ACCOUNT_NAME)
