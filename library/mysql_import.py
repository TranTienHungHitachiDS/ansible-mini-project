#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import mysql.connector

def import_data(host, user, password):
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")

    cursor.execute("USE test_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ansible_table (
            Name VARCHAR(255) PRIMARY KEY,
            Value VARCHAR(255)
        )
    """)

    print("Database and table created successfully.")

    cursor.close()
    conn.close()

def run_module():
    module_args = dict(
        host=dict(type='str', default="localhost", required=False),
        user=dict(type='str', required=True),
        password=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=module_args)

    host = module.params['host']
    user = module.params['user']
    password = module.params['password']

    try:
        import_data(host, user, password)

        # Report success to Ansible
        module.exit_json(changed=True, msg="Import data to database successfully")

    except Exception as e:
        # Report failure to Ansible
        module.fail_json(msg=str(e))


if __name__ == '__main__':
    run_module()
