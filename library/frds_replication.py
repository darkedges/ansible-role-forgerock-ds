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
import csv


def get_status(module, frds_bin_dir, server_hostname, server_admin_port,
               admin_uid, admin_password, base_dn):
    status_command = [
        frds_bin_dir + '/dsreplication',
        'status',
        '--hostname', server_hostname,
        '--port', str(server_admin_port),
        '--adminUid', admin_uid,
        '--adminPassword', admin_password,
        '--no-prompt',
        '--trustAll',
        '--script-friendly'
    ]
    if len(base_dn) > 0:
        for basedn in base_dn:
            status_command.append('--baseDN')
            status_command.append(basedn)

    # return status_command

    host_details = server_hostname + ':'+str(server_admin_port)

    rc, stdout, stderr = module.run_command(status_command)
    fieldnames = ['suffix_dn', 'server', 'entries', 'replication_enabled',
                  'ds_id', 'rs_id', 'rs_port', 'delay', 'security ']
    reader = csv.DictReader(stdout.splitlines(),
                            fieldnames=fieldnames, delimiter='\t', restval='')
    count = 0
    for line in reader:
        if line['suffix_dn'] in base_dn and line['server'].lower() == host_details.lower() and line['replication_enabled'].lower() == 'true':
            count += 1
    if rc == 0:
        return count == len(base_dn)
    else:
        raise Exception("Error message: " + stderr)


def replication_configure(module, frds_bin_dir, admin_uid, admin_password, base_dn, directory_server_hostname, directory_server_admin_port,
                          directory_server_bind_dn, directory_server_replication_port, replication_server_hostname, replication_server_admin_port,
                          replication_server_bind_dn, directory_server_bind_password, replication_server_bind_password,
                          replication_server_replication_port, embedded_replication_server):
    configure_command = [
        frds_bin_dir + '/dsreplication',
        'configure',
        '--adminUid', admin_uid,
        '--adminPassword', admin_password,
        '--no-prompt',
        '--trustAll',
        '--host1', directory_server_hostname,
        '--port1', str(directory_server_admin_port),
        '--bindDN1', directory_server_bind_dn,
        '--bindPassword1', directory_server_bind_password,
        '--host2', replication_server_hostname,
        '--port2', str(replication_server_admin_port),
        '--bindDN2', replication_server_bind_dn,
        '--bindPassword2', replication_server_bind_password,
        '--replicationPort2', str(replication_server_replication_port),
    ]

    if (embedded_replication_server):
        configure_command.append('--replicationPort1')
        configure_command.append(str(directory_server_replication_port))
    else:
        configure_command.append('--noReplicationServer1')
        configure_command.append('--onlyReplicationServer2')

    if len(base_dn) > 0:
        for basedn in base_dn:
            configure_command.append('--baseDN')
            configure_command.append(basedn)

    # return configure_command
    rc, stdout, stderr = module.run_command(configure_command)
    if rc == 0:
        return stdout
    else:
        module.fail_json(msg="Error message: " + stderr)


def replication_unconfigure(module,
                            frds_bin_dir,
                            base_dn,
                            replication_server_hostname,
                            replication_server_admin_port,
                            admin_uid,
                            admin_password):
    unconfigure_command = [
        frds_bin_dir + '/dsreplication',
        'unconfigure',
        '--no-prompt',
        '--trustAll',
        '--hostname', replication_server_hostname,
        '--port', str(replication_server_admin_port),
        '--adminUid', admin_uid,
        '--adminPassword', admin_password,
    ]
    if len(base_dn) > 0:
        for basedn in base_dn:
            unconfigure_command.append('--baseDN')
            unconfigure_command.append(basedn)
    # return configure_command
    rc, stdout, stderr = module.run_command(unconfigure_command)
    if rc == 0:
        return stdout
    else:
        module.fail_json(msg="Error message: " + stderr)


def replication_initialize(module,
                           frds_bin_dir,
                           state,
                           base_dn,
                           replication_server_hostname,
                           replication_server_admin_port,
                           admin_uid,
                           admin_password):
    initialize_command = [
        frds_bin_dir + '/dsreplication',
    ]
    if state == 'initialize':
        initialize_command.extend([
            'initialize',
        ])
    else:
        initialize_command.extend([
            'initialize-all'
        ])

    initialize_command.extend([
        '--no-prompt',
        '--trustAll',
        '--hostname', replication_server_hostname,
        '--port', str(replication_server_admin_port),
        '--adminUid', admin_uid,
        '--adminPassword', admin_password
    ])

    if len(base_dn) > 0:
        for basedn in base_dn:
            initialize_command.append('--baseDN')
            initialize_command.append(basedn)

    # return initialize_command
    rc, stdout, stderr = module.run_command(initialize_command)
    if rc == 0:
        return stdout
    else:
        module.fail_json(msg="Error message: " + stderr)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        frds_bin_dir=dict(type='path', default="/opt/oid/frds/rs/bin"),
        admin_uid=dict(type='str', default="admin"),
        admin_password=dict(type='str', required=True, no_log=True),
        base_dn=dict(type='list', default=[]),
        directory_server_hostname=dict(type='str', required=True),
        directory_server_admin_port=dict(default=4444),
        directory_server_bind_dn=dict(
            type='str', default="cn=Directory Manager"),
        directory_server_bind_password=dict(
            type='str', required=True, no_log=True),
        directory_server_replication_port=dict(default=8989),
        replication_server_hostname=dict(type='str', required=True),
        replication_server_admin_port=dict(type='str', required=True),
        replication_server_bind_dn=dict(
            type='str', default="cn=Directory Manager"),
        replication_server_bind_password=dict(
            type='str', required=True, no_log=True),
        replication_server_replication_port=dict(default=8989),
        state=dict(type='str', default="present"),
        embedded_replication_server=dict(
            type='bool', default=False)
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
    admin_uid = module.params['admin_uid']
    admin_password = module.params['admin_password']
    base_dn = module.params['base_dn']
    directory_server_hostname = module.params['directory_server_hostname']
    directory_server_admin_port = module.params['directory_server_admin_port']
    directory_server_bind_dn = module.params['directory_server_bind_dn']
    directory_server_bind_password = module.params['directory_server_bind_password']
    directory_server_replication_port = module.params['directory_server_replication_port']
    replication_server_hostname = module.params['replication_server_hostname']
    replication_server_admin_port = module.params['replication_server_admin_port']
    replication_server_bind_dn = module.params['replication_server_bind_dn']
    replication_server_bind_password = module.params['replication_server_bind_password']
    replication_server_replication_port = module.params['replication_server_replication_port']
    state = module.params['state'].lower()
    embedded_replication_server = module.params['embedded_replication_server']

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    try:
        validate = get_status(module,
                              frds_bin_dir=frds_bin_dir,
                              server_hostname=directory_server_hostname,
                              server_admin_port=directory_server_admin_port,
                              admin_uid=admin_uid,
                              admin_password=admin_password,
                              base_dn=base_dn
                              )
    except Exception as e:
        if embedded_replication_server:
            validate = False
        else:
            module.fail_json(msg=e.message)

    if state == 'present':
        if validate:
            module.exit_json(changed=False)
        else:
            configure_result = replication_configure(module,
                                                     frds_bin_dir=frds_bin_dir,
                                                     admin_uid=admin_uid,
                                                     admin_password=admin_password,
                                                     base_dn=base_dn,
                                                     directory_server_hostname=directory_server_hostname,
                                                     directory_server_admin_port=directory_server_admin_port,
                                                     directory_server_bind_dn=directory_server_bind_dn,
                                                     directory_server_bind_password=directory_server_bind_password,
                                                     directory_server_replication_port=directory_server_replication_port,
                                                     replication_server_hostname=replication_server_hostname,
                                                     replication_server_admin_port=replication_server_admin_port,
                                                     replication_server_bind_dn=replication_server_bind_dn,
                                                     replication_server_bind_password=replication_server_bind_password,
                                                     replication_server_replication_port=replication_server_replication_port,
                                                     embedded_replication_server=embedded_replication_server)
            result['message'] = configure_result
            result['changed'] = True
            module.exit_json(**result)

    if state == 'absent':
        if validate:
            unconfigure_result = replication_unconfigure(module,
                                                         frds_bin_dir=frds_bin_dir,
                                                         base_dn=base_dn,
                                                         replication_server_hostname=directory_server_hostname,
                                                         replication_server_admin_port=directory_server_admin_port,
                                                         admin_uid=admin_uid,
                                                         admin_password=admin_password
                                                         )
            result['message'] = unconfigure_result
            result['changed'] = True
            module.exit_json(**result)
        else:
            module.exit_json(changed=False)

    if state.startswith('initialize'):
        if validate:
            initialize_result = replication_initialize(module,
                                                       frds_bin_dir=frds_bin_dir,
                                                       state=state,
                                                       base_dn=base_dn,
                                                       replication_server_hostname=directory_server_hostname,
                                                       replication_server_admin_port=directory_server_admin_port,
                                                       admin_uid=admin_uid,
                                                       admin_password=admin_password
                                                       )
            result['message'] = initialize_result
            result['changed'] = True
            module.exit_json(**result)
        else:
            module.exit_json(changed=False)


def main():
    run_module()


if __name__ == '__main__':
    main()
