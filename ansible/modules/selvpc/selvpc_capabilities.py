#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: selvpc_capabilities
short_description: get possible values of different variables
description:
    - Get info about possible values
version_added: "2.3"
author: Rutskiy Daniil (@rutskiy)
options:
  token:
    description:
     - Selectel VPC API token.
  state:
    description:
     - Indicate desired state
    required: true
    default: present
    choices: ['present', 'absent']
requirements:
  - python-selvpcclient
'''

EXAMPLES = '''
# Get info about capabilities
- selvpc_capabilities:
      state: present
'''

import os

from selvpcclient.client import setup_http_client, Client
from selvpcclient.exceptions.base import ClientException


def main():
    module = AnsibleModule(argument_spec=dict(
        state=dict(choices=['present', 'absent'], default='present'),
        token=dict(type='str', no_log=True),
    ), supports_check_mode=True)

    state = module.params.get('state')

    if module.params['token']:
        token = module.params['token']
    else:
        token = os.environ.get('SEL_TOKEN')
    url = os.environ.get('SEL_URL')

    # Configure REST client
    try:
        http_client = setup_http_client(url, api_token=token)
        client = Client(http_client)
    except Exception as exp:
        module.fail_json(msg="No token given")

    if module.check_mode:
        module.exit_json(changed=False)

    if state == 'present':
        try:
            result = client.capabilities.get()
        except ClientException as exp:
            module.fail_json(msg=str(exp))
        module.exit_json(result=result._info)
    module.fail_json(msg="Wrong 'state' param for 'capabilities' operation.")


from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()