# Ansible Role: ForgeRock Directory Service

## Default Credentials

By default the credentials it creates are `cn=Directory Manager`:`Passw0rd`

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

## License

Copyright © 2019 [DarkEdges](https://bitbucket.org/darkedges).  
This project is [Apache License Version 2.0](https://bitbucket.org/darkedges/ansible-role-forgerock-ds/src/master/LICENSE) licensed.
