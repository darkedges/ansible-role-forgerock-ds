#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: frds_replication_status

short_description: This is my sample module

version_added: "2.4"

description:
    - "This is my longer description explaining my sample module"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule


def get_status(module, policy_name, frds_bin_dir, server_hostname, server_admin_port,
               bind_dn, bind_password):
    status_command = [
        frds_bin_dir + '/dsconfig',
        'get-global-access-control-policy-prop',
        '--policy-name', policy_name,
        '--hostname', server_hostname,
        '--port', str(server_admin_port),
        '--bindDn', bind_dn,
        '--bindPassword', bind_password,
        '--no-prompt',
        '--trustAll',
        '--script-friendly'
    ]

    rc, stdout, stderr = module.run_command(status_command)
    if rc == 0:
        newData = {}
        for line in stdout.split('\n'):
            line = line.rstrip()
            try:
                key, value = line.split('\t', 1)
                newData[key] = value.split('\t')
            except ValueError:
                newData[line] = ""
                continue
        return True, newData
    else:
        if "The Global Access Control Policy does not exist" in stderr:
            return False, {}
        else:
            module.fail_json(msg="Error message: " + stderr)


def update_gacpp(module, frds_bin_dir, server_hostname, server_admin_port, bind_dn,
                 bind_password, policy_name, current_properties, proposed_properties):
    # Work out differences
    commands = []
    for key in current_properties:
        try:
            a = proposed_properties[key]
            b = current_properties[key]
            if not isinstance(a, list):
                a = [a]
            s = set(a)
            deletes = [x for x in b if x not in s]
            s = set(b)
            adds = [x for x in a if x not in s]

            for x in deletes:
                commands.append('--remove')
                commands.append(key+':'+x)
            for x in adds:
                commands.append('--add')
                commands.append(key+':'+x)
        except KeyError:
            continue
        # Check to see if we need to execute any updates
        if len(commands) > 0:
            # need to build and execute command
            set_command = [
                frds_bin_dir + '/dsconfig',
                'set-global-access-control-policy-prop',
                '--hostname', server_hostname,
                '--port', str(server_admin_port),
                '--bindDn', bind_dn,
                '--bindPassword', bind_password,
                '--policy-name', policy_name,
                '--trustAll',
                '--no-prompt'
            ]
            set_command.extend(commands)
            rc, stdout, stderr = module.run_command(set_command)
            if rc == 0:
                return True, stdout
            else:
                module.fail_json(msg="Error message: " + stderr)
    return False, ""


def create_gacpp(module, frds_bin_dir, server_hostname, server_admin_port, bind_dn,
                 bind_password, policy_name, properties):
    create_command = [
        frds_bin_dir + '/dsconfig',
        'create-global-access-control-policy',
        '--hostname', server_hostname,
        '--port', str(server_admin_port),
        '--bindDn', bind_dn,
        '--bindPassword', bind_password,
        '--policy-name', policy_name,
        '--trustAll',
        '--no-prompt'
    ]
    commands = []
    for key in properties:
        values = properties[key]
        if not isinstance(values, list):
            values = [values]
        for value in values:
            commands.append('--set')
            commands.append(key+':'+value)
    create_command.extend(commands)
    rc, stdout, stderr = module.run_command(create_command)
    if rc == 0:
        return True, stdout
    else:
        module.fail_json(msg="Error message: " + stderr)
    return True


def delete_gacpp(module, frds_bin_dir, server_hostname, server_admin_port, bind_dn,
                 bind_password, policy_name,):
    delete_command = [
        frds_bin_dir + '/dsconfig',
        'delete-global-access-control-policy',
        '--hostname', server_hostname,
        '--port', str(server_admin_port),
        '--bindDn', bind_dn,
        '--bindPassword', bind_password,
        '--policy-name', policy_name,
        '--trustAll',
        '--no-prompt'
    ]
    rc, stdout, stderr = module.run_command(delete_command)
    if rc == 0:
        return True, stdout
    else:
        module.fail_json(msg="Error message: " + stderr)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        policy_name=dict(type='str', required=True),
        frds_bin_dir=dict(type='path', default="/opt/oid/frds/bin"),
        directory_server_hostname=dict(type='str', required=True),
        directory_server_admin_port=dict(default=4444),
        directory_server_bind_dn=dict(
            type='str', default="cn=Directory Manager"),
        directory_server_bind_password=dict(
            type='str', required=True, no_log=True),
        state=dict(type='str', default="present"),
        properties=dict(type='dict', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    frds_bin_dir = module.params['frds_bin_dir']
    directory_server_hostname = module.params['directory_server_hostname']
    directory_server_admin_port = module.params['directory_server_admin_port']
    directory_server_bind_dn = module.params['directory_server_bind_dn']
    directory_server_bind_password = module.params['directory_server_bind_password']
    state = module.params['state'].lower()
    properties = module.params['properties']
    policy_name = module.params['policy_name']

    exists, current_properties = get_status(module,
                                            frds_bin_dir=frds_bin_dir,
                                            policy_name=policy_name,
                                            server_hostname=directory_server_hostname,
                                            server_admin_port=directory_server_admin_port,
                                            bind_dn=directory_server_bind_dn,
                                            bind_password=directory_server_bind_password
                                            )
    if state == 'present':
        if exists:
            changed, updateResult = update_gacpp(module,
                                                 frds_bin_dir=frds_bin_dir,
                                                 policy_name=policy_name,
                                                 server_hostname=directory_server_hostname,
                                                 server_admin_port=directory_server_admin_port,
                                                 bind_dn=directory_server_bind_dn,
                                                 bind_password=directory_server_bind_password,
                                                 current_properties=current_properties,
                                                 proposed_properties=properties)
            result['message'] = updateResult
            result['changed'] = changed
            module.exit_json(**result)
        else:
            createResult = create_gacpp(module,
                                        frds_bin_dir=frds_bin_dir,
                                        policy_name=policy_name,
                                        server_hostname=directory_server_hostname,
                                        server_admin_port=directory_server_admin_port,
                                        bind_dn=directory_server_bind_dn,
                                        bind_password=directory_server_bind_password,
                                        properties=properties)
            result['message'] = createResult
            result['changed'] = True
            module.exit_json(**result)
    else:
        if exists:
            deleteResult = delete_gacpp(module,
                                        frds_bin_dir=frds_bin_dir,
                                        policy_name=policy_name,
                                        server_hostname=directory_server_hostname,
                                        server_admin_port=directory_server_admin_port,
                                        bind_dn=directory_server_bind_dn,
                                        bind_password=directory_server_bind_password)
            result['message'] = deleteResult
            result['changed'] = True
            module.exit_json(**result)
        else:
            module.exit_json(changed=False)


def main():
    run_module()


if __name__ == '__main__':
    main()
