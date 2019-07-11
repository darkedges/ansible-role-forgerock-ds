# Ansible Role: ForgeRock Directory Service

## Examples

### Single Directory Server instances

```bash
- hosts: frds
  roles:
    - role: forgerock.ds
      frds_ds_service_name: "dsmaster"
      frds_ds_config_start_server: true
```

## License

Copyright © 2019 [DarkEdges](https://bitbucket.org/darkedges).  
This project is [Apache License Version 2.0](https://bitbucket.org/darkedges/ansible-role-forgerock-ds/src/master/LICENSE) licensed.
