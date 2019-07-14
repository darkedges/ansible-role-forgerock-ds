# Ansible Role: ForgeRock Directory Service

This Ansible Role helps with the installation and configuration of a ForgeRock Directory Service `directory-server` instance.

Although it has the options for `replication-server` and `proxy-server` they will be added a future date.

## Configuration

The following values are used as part of the configuration

### Common

| Variable                 | Default Value                                                  | Type      | Possible Values                             | Description |
| ------------------------ | -------------------------------------------------------------- | --------- | ------------------------------------------- | ----------- |
| `frds_default_password`  | `Passw0rd`                                                     | `string`  |                                             |             |
| `frds_version`           | `6.5.0`                                                        | `string`  |                                             |             |
| `frds_version_eval`      | `true`                                                         | `boolean` |                                             |             |
| `frds_install_file`      | `DS{{ '-eval' if frds_version_eval  }}-{{ frds_version }}.zip` | `string`  |                                             |             |
| `frds_fr_user`           | `forgerock`                                                    | `string`  |                                             |             |
| `frds_fr_group`          | `forgerock`                                                    | `string`  |                                             |             |
| `frds_install_path`      | `/opt/ois/frds`                                                | `string`  |                                             |             |
| `frds_instance_path`     | `{{ frds_install_path }}`                                      | `string`  |                                             |             |
| `frds_install_type`      | `directory-server`                                             | `string`  |                                             |             |
| `frds_install_operation` | `install`                                                      | `string`  | `install`<br/>`configure`<br/>`replication` |             |

### Directory Server

| Variable                                               | Default Value                                                                                                    | Type      | Possible Values | `CommandLine Map` | Description |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | --------- | --------------- | ----------------- | ----------- |
| `frds_ds_config_add_base_entry`                        | `false`                                                                                                          | `boolean` |                 |                   |             |
| `frds_ds_config_admin_port`                            | `{{ 4444 if (frds_ds_config_base_port == 0) else frds_ds_config_base_port + 444 }}`                              | `int`     |                 |                   |             |
| `frds_ds_config_base_dns`                              | ```- dc=example,dc=com```                                                                                        | `list`    |                 |                   |             |
| `frds_ds_config_base_port`                             | `0`                                                                                                              | `string`  |                 |                   |             |
| `frds_ds_config_cert_nickname`                         |                                                                                                                  | `list`    |                 |                   |             |
| `frds_ds_config_enable_start_tls`                      | `true`                                                                                                           | `boolean` |                 |                   |             |
| `frds_ds_config_hostname`                              | `{{ ansible_hostname }}`                                                                                         | `string`  |                 |                   |             |
| `frds_ds_config_http_port`                             | `{{ 8080 if (frds_ds_config_base_port == 0) else frds_ds_config_base_port + 880 }}`                              | `int`     |                 |                   |             |
| `frds_ds_config_https_port`                            | `{{ 8443 if (frds_ds_config_base_port == 0) else frds_ds_config_base_port + 843 }}`                              | `int`     |                 |                   |             |
| `frds_ds_config_import_ldif_file`                      |                                                                                                                  | `list`    |                 |                   |             |
| `frds_ds_config_instance_path`                         | `{{ frds_install_path if frds_ds_service_name length == 0 else frds_instance_path }}/{{ frds_ds_service_name }}` | `string`  |                 |                   |             |
| `frds_ds_config_jmx_port`                              | `{{ 1689 if (frds_ds_config_base_port == 0) else frds_ds_config_base_port + 689 }}`                              | `int`     |                 |                   |             |
| `frds_ds_config_keystore_password_file`                |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_keystore_password`                     |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_ldap_port`                             | `{{ 1389 if (frds_ds_config_base_port == 0) else frds_ds_config_base_port + 389 }}`                              | `int`     |                 |                   |             |
| `frds_ds_config_ldaps_port:`                           | `{{ 1636 if (frds_ds_config_base_port == 0) else frds_ds_config_base_port + 636 }}`                              | `int`     |                 |                   |             |
| `frds_ds_config_replication_port:`                     | `{{ 8989 if (frds_ds_config_base_port == 0) else frds_ds_config_base_port + 989 }}`                              | `int`     |                 |                   |             |
| `frds_ds_config_monitor_user_dn:`                      | `uid=monitor`                                                                                                    | `string`  |                 |                   |             |
| `frds_ds_config_monitor_user_password_file:`           |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_monitor_user_password:`                | `{{ frds_default_password }}`                                                                                    | `string`  |                 |                   |             |
| `frds_ds_config_production_mode:`                      | `false`                                                                                                          | `string`  |                 |                   |             |
| `frds_ds_config_profiles:`                             |                                                                                                                  | `list`    |                 |                   |             |
| `frds_ds_config_profiles_enabled:`                     | `{{ frds_ds_config_profiles length > 0 }}`                                                                       | `string`  |                 |                   |             |
| `frds_ds_config_reject_file:`                          |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_root_user_dn:`                         | `cn=Directory Manager`                                                                                           | `string`  |                 |                   |             |
| `frds_ds_config_root_user_password_file:`              |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_root_user_password:`                   | `{{ frds_default_password }}`                                                                                    | `string`  |                 |                   |             |
| `frds_ds_config_sample_data:`                          | `-1`                                                                                                             | `string`  |                 |                   |             |
| `frds_ds_config_skip_file:`                            |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_skip_port_check:`                      | `false`                                                                                                          | `boolean` |                 |                   |             |
| `frds_ds_config_start_server:`                         | `false`                                                                                                          | `boolean` |                 |                   |             |
| `frds_ds_config_use_jceks_keystore:`                   |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_use_jks_keystore:`                     |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_use_pkcs11_keystore:`                  |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_config_use_pkcs12_keystore:`                  |                                                                                                                  | `string`  |                 |                   |             |
| `frds_ds_group:`                                       | `{{ frds_fr_group }}`                                                                                            | `string`  |                 |                   |             |
| `frds_ds_install_directory:`                           | `{{ frds_install_path }}/{{ frds_ds_service_name }}`                                                             | `string`  |                 |                   |             |
| `frds_ds_service_name:`                                | `ds`                                                                                                             | `string`  |                 |                   |             |
| `frds_ds_user:`                                        | `{{ frds_fr_user }}`                                                                                             | `string`  |                 |                   |             |
| `frds_ds_enable_ports_http:`                           | `false`                                                                                                          | `boolean` |                 |                   |             |
| `frds_ds_enable_ports_https:`                          | `true`                                                                                                           | `boolean` |                 |                   |             |
| `frds_ds_enable_user_monitor:`                         | `false`                                                                                                          | `boolean` |                 |                   |             |
| `frds_ds_config_replication_admin_password:`           | `{{ frds_default_password }}`                                                                                    | `string`  |                 |                   |             |
| `frds_ds_config_replication_server1_admin_port:`       | `4444`                                                                                                           | `string`  |                 |                   |             |
| `frds_ds_config_replication_server1_hostname:`         | `{{ ansible_hostname }}`                                                                                         | `string`  |                 |                   |             |
| `frds_ds_config_replication_server1_admin_password:`   | `{{ frds_default_password }}`                                                                                    | `string`  |                 |                   |             |
| `frds_ds_config_replication_server1_replication_port:` | `8989`                                                                                                           | `int`     |                 |                   |             |
| `frds_ds_config_replication_server2_admin_port:`       | `4444`                                                                                                           | `int`     |                 |                   |             |
| `frds_ds_config_replication_server2_hostname:`         | `{{ ansible_hostname }}`                                                                                         | `string`  |                 |                   |             |
| `frds_ds_config_replication_server2_admin_password:`   | `{{ frds_default_password }}`                                                                                    | `string`  |                 |                   |             |
| `frds_ds_config_replication_server2_replication_port:` | `8989`                                                                                                           | `int`     |                 |                   |             |
| `frds_ds_config_replication_embedded_server:`          | `false`                                                                                                          | `boolean` |                 |                   |             |
| `frds_ds_config_replication_states:`                   | ```- present```                                                                                                  | `list`    |                 |                   |             |

## Default Credentials

By default the credentials it creates are`cn=Directory Manager`:`Passw0rd`

## Examples

**Note:** There is an assumption in these examples that a JDK has been deployed suitable for the product.

For example

```bash
- hosts: frds
  roles:
    - role: geerlingguy.java
      java_packages:
        - java-1.8.0-openjdk-headless
```

### Single ForgeRock Directory Service instance

This use default values

| Service | Service Name | Port   |
| ------- | ------------ | ------ |
| LDAP    | `ds`         | `1389` |
| LDAPS   | `ds`         | `1636` |
| HTTPS   | `ds`         | `8443` |

```bash
- hosts: frds
  roles:
    - role: forgerock.user
    - role: forgerock.ds
      become: yes
```

### Single ForgeRock Directory Service instance, different Path

```bash
- hosts: frds
  vars:
    frds_install_path: "/opt/forgerock/frds"
    frds_instance_path: "/var/forgerock/frds"
  roles:
    - role: forgerock.user
    - role: forgerock.ds
      become: yes
```

### Single ForgeRock Directory Service instance with DS Config Profiles

```bash
- hosts: frds
  vars:
    frds_install_path: "/opt/forgerock/frds"
    frds_instance_path: "/var/forgerock/frds"
  roles:
    - role: forgerock.user
    - role: forgerock.ds
      become: yes
      frds_ds_config_profiles:
        - profile: "am-identity-store"
          version: "{{ frds_version }}"
          settings:
            - paramName: "backendName"
              value: "amIdentityStore"
            - paramName: "amIdentityStoreAdminPassword"
              value: "{{ frds_default_password }}"
        - profile: "am-config"
          version:"{{ frds_version }}"
          settings:
            - paramName: "backendName"
              value: "cfgStore"
            - paramName: "amConfigAdminPassword"
              value: "{{ frds_default_password }}"
            - paramName: "baseDn"
              value: "ou=am-config"
        - profile: "am-cts"
          version: "{{ frds_version }}"
          settings:
            - paramName: "backendName"
              value: "amCts"
            - paramName: "amCtsAdminPassword"
              value: "{{ frds_default_password }}"
            - paramName: "tokenExpirationPolicy"
              value: "am"
```

### Multiple ForgeRock Directory Service instances

This use default values

| Service | Service Name | Port   |
| ------- | ------------ | ------ |
| LDAP    | `dsmaster`   | `1389` |
| LDAPS   | `dsmaster`   | `1636` |
| HTTPS   | `dsmaster`   | `1443` |
| LDAP    | `dsreplica`  | `2389` |
| LDAPS   | `dsreplica`  | `2636` |
| HTTPS   | `dsreplica`  | `2443` |

```bash
- hosts: frds
  vars:
    frds_install_path: "/opt/forgerock/frds"
    frds_instance_path: "/var/forgerock/frds"
  roles:
    - role: forgerock.user
    - role: forgerock.ds
      become: yes
      frds_ds_service_name: "dsmaster"
      frds_ds_config_base_port: 1000
    - role: forgerock.ds
      become: yes
      frds_ds_service_name: "dsreplica"
      frds_ds_config_base_port: 2000
```

### ForgeRock Directory Service Replication

This use default values

| Service     | Service Name | Port   |
| ----------- | ------------ | ------ |
| LDAP        | `dsmaster`   | `1389` |
| LDAPS       | `dsmaster`   | `1636` |
| HTTPS       | `dsmaster`   | `1443` |
| Replication | `dsmaster`   | `1989` |
| LDAP        | `dsreplica`  | `2389` |
| LDAPS       | `dsreplica`  | `2636` |
| HTTPS       | `dsreplica`  | `2443` |
| Replication | `dsmaster`   | `2989` |

```bash
- hosts: frds
  vars:
    frds_install_path: "/opt/forgerock/frds"
    frds_instance_path: "/var/forgerock/frds"
  roles:
    - role: forgerock.user
    - role: forgerock.ds
      become: yes
      frds_ds_service_name: "dsmaster"
      frds_ds_config_base_port: 1000
    - role: forgerock.ds
      become: yes
      frds_ds_service_name: "dsreplica"
      frds_ds_config_base_port: 2000
    - role: forgerock.ds
      become: yes
      frds_install_operation: "replication"
      frds_ds_service_name: "dsmaster"
      frds_ds_config_replication_embedded_server: true
      frds_ds_config_replication_server1_admin_port: 1444
      frds_ds_config_replication_server1_replication_port: 1989
      frds_ds_config_replication_server2_admin_port: 2444
      frds_ds_config_replication_server2_replication_port: 2989
      frds_ds_config_replication_initialize: true
      frds_ds_config_replication_states:
        - "present"
        - "initialize-all"
```

### Putting it all togethor

```bash
- hosts: frds
  vars:
    frds_install_path: "/opt/forgerock/frds"
    frds_instance_path: "/var/forgerock/frds"
    frds_version: 6.5.0
  roles:
    - role: forgerock.user
    - role: forgerock.ds
      become: yes
      frds_ds_service_name: "dsmaster"
      frds_ds_config_base_port: 1000
      frds_ds_config_profiles:
        - profile: "am-identity-store"
          version: "{{ frds_version }}"
          settings:
            - paramName: "backendName"
              value: "amIdentityStore"
            - paramName: "amIdentityStoreAdminPassword"
              value: "{{ frds_default_password }}"
        - profile: "am-config"
          version: "{{ frds_version }}"
          settings:
            - paramName: "backendName"
              value: "cfgStore"
            - paramName: "amConfigAdminPassword"
              value: "{{ frds_default_password }}"
            - paramName: "baseDn"
              value: "ou=am-config"
        - profile: "am-cts"
          version: "{{ frds_version }}"
          settings:
            - paramName: "backendName"
              value: "amCts"
            - paramName: "amCtsAdminPassword"
              value: "{{ frds_default_password }}"
            - paramName: "tokenExpirationPolicy"
              value: "am"
    - role: forgerock.ds
      become: yes
      frds_ds_service_name: "dsreplica"
      frds_ds_config_base_port: 2000
      frds_ds_config_base_dns:
        - "ou=identities"
        - "ou=am-config"
        - "ou=tokens"
    - role: forgerock.ds
      become: yes
      frds_install_operation: "replication"
      frds_ds_service_name: "dsmaster"
      frds_ds_config_replication_embedded_server: true
      frds_ds_config_replication_server1_admin_port: 1444
      frds_ds_config_replication_server1_replication_port: 1989
      frds_ds_config_replication_server2_admin_port: 2444
      frds_ds_config_replication_server2_replication_port: 2989
      frds_ds_config_replication_initialize: true
      frds_ds_config_base_dns:
        - "ou=identities"
        - "ou=am-config"
        - "ou=tokens"
      frds_ds_config_replication_states:
        - "present"
        - "initialize-all"
```

## License

Copyright © 2019 [DarkEdges](https://bitbucket.org/darkedges).
This project is [Apache License Version 2.0](https://github.com/darkedges/ansible-role-forgerock-ds/blob/master/LICENSE) licensed.
