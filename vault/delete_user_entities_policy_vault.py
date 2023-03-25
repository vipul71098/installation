import requests

# Authenticate with Vault using a token or other authentication method
VAULT_TOKEN = '<vault token>'
headers = {'X-Vault-Token': VAULT_TOKEN}

# Query the list of all users and entities in the Vault
list_users_url = 'http://localhost:8200/v1/auth/userpass/users?list=true'
list_entities_url = 'http://localhost:8200/v1/identity/entity/name?list=true'
list_policies_url = 'http://localhost:8200/v1/sys/policy?list=true'

response = requests.get(list_users_url, headers=headers)
users = response.json()['data']['keys']

response = requests.get(list_entities_url, headers=headers)
entities = response.json()['data']['keys']

response = requests.get(list_policies_url, headers=headers)
policies = response.json()['data']['keys']

# Delete all users
for user in users:
    delete_user_url = f'http://localhost:8200/v1/auth/userpass/users/{user}'
    response = requests.delete(delete_user_url, headers=headers)
    if response.status_code == 204:
        print(f"Deleted user: {user}")
    else:
        print(f"Failed to delete user: {user}")

# Delete all entities
for entity in entities:
    delete_entity_url = f'http://localhost:8200/v1/identity/entity/name/{entity}'
    response = requests.delete(delete_entity_url, headers=headers)
    if response.status_code == 204:
        print(f"Deleted entity: {entity}")
    else:
        print(f"Failed to delete entity: {entity}")

# Delete all policies
for policy in policies:
    delete_policy_url = f'http://localhost:8200/v1/sys/policy/{policy}'
    response = requests.delete(delete_policy_url, headers=headers)
    if response.status_code == 204:
        print(f"Deleted policy: {policy}")
    else:
        print(f"Failed to delete policy: {policy}")
