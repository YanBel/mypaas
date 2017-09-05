#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    import ovh
except ImportError:
    print "failed=True msg='ovh required for this module'"
    sys.exit(1)

vlan_id=0
# Try to automate this in case the supplied credentials are not valid
def get_credentials():
    """This function is used to obtain an authentication token.
    It should only be called once."""
    client = ovh.Client()
    access_rules = [
        {'method': 'GET', 'path': '/cloud/*'},
        {'method': 'PUT', 'path': '/cloud/*'},
        {'method': 'POST', 'path': '/cloud/*'},
        {'method': 'DELETE', 'path': '/cloud/*'},
    ]
    validation = client.request_consumerkey(access_rules)
    print("Your consumer key is {}".format(validation['consumerKey']))
    print("Please visit {} to validate".format(validation['validationUrl']))

def main():
    module = AnsibleModule(
        argument_spec = dict(
            description = dict(required=True),
            project_name = dict(required=True),
            name = dict(required=True),
            id = dict(required=True),
            state = dict(required=True),
            region = dict(required=True),
            cidr = dict(required=True),
            start_ip = dict(required=True),
            end_ip = dict(required=True),

        )
    )

    # Get parameters
    description = module.params.get('description')
    project_name = module.params.get('project_name')
    vlan_name = module.params.get('name')
    vlan_id = module.params.get('id')
    state = module.params.get('state')
    region = module.params.get('region')
    cidr = module.params.get('cidr')
    start_ip = module.params.get('start_ip')
    end_ip = module.params.get('end_ip')
    # Connect to OVH API
    client = ovh.Client()
    # Check that the project exists
    get_ovh_projects = client.get('/cloud/project')
    project_exist = False
    for project_id in get_ovh_projects:
        project = client.get('/cloud/project/{}'.format(project_id))
        if description == project['description']:
            project_exist = True
            break
    #Get vRACK
    get_ovh_vracks = client.get('/vrack')
    vrack_exist= False
    if not get_ovh_vracks:
        vrack_exist='False'
        module.exit_json(changed=True, vrack_check=vrack_exist)
    else:
        vrack_exist= True
        for vracks_id in get_ovh_vracks:
            vrack_details = client.get('/vrack/{}'.format(vracks_id))
            vrack_id=vracks_id
    	    break
    # Get project vrack and attach if not
    try:
        ovh_project_vrack_check= client.get('/cloud/project/{}/vrack'.format(project_id))
        attach_vrack=True
    except:
        ovh_project_vrack_check=''
        attach_vrack=False
        #attack project to vrack
        try:
            ovh_attach_vrack = client.post('/vrack/{}/cloudProject'.format(vrack_id), project=project_id)
            task_id=result['id']
            service_name=result['serviceName']
        except Exception as ex:
            state='Failed to attach project to vRack'
            module.exit_json(changed=True, error=state)
        # Check task status
        time.sleep(60)

    state='OK'
    state_nok='vLan exist or Error'
    vlan_id2=int(vlan_id)
    # VLAN CREATION
    try:
        ovh_vlan_create = client.post('/cloud/project/{}/network/private'.format(project_id),
         name=vlan_name,
         vlanId=vlan_id2,
         #regions=region
        )
        time.sleep(60)
        ###### get vlan and create subnet
        try:
            ovh_get_vlans = client.get('/cloud/project/{}/network/private'.format(project_id))
            for vlan in ovh_get_vlans:
                if vlan['vlanId'] == vlan_id2:
                    vlan_ref=vlan['id']
                    # create sub network
                    try:
                        ovh_create_subnet = client.post('/cloud/project/{}/network/private/{}/subnet'.format(project_id,vlan_ref),
                         dhcp=True,
                         end=end_ip,
                         network=cidr,
                         noGateway=True,
                         region=region,
                         start=start_ip,
                        )
                        time.sleep(5)
                        ovh_get_subnets = client.get('/cloud/project/{}/network/private/{}/subnet'.format(project_id,vlan_ref))
                        module.exit_json(changed=True, output=ovh_get_subnets)
                    except Exception as ex:
                        stat='Subnet creation failed'
                        module.exit_json(changed=False, error=ex)
                    break

                else:
                    state='Not right vLan'
                    #module.exit_json(changed=False, output=stat)
        except Exception as ex:
            state='error get networks'
            module.exit_json(changed=False, output=ex)

        module.exit_json(changed=True, vlan=vlan)

    except Exception as ex:
        out='Vlan exist Or creation API error'
        module.exit_json(changed=False, res=out)


# import module snippets
from ansible.module_utils.basic import *
main()
