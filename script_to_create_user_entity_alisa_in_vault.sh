#/bin/bash
USER='bob'
PASSWORD=$USER@1234
POLICY='carlogic-node-backend-dev-policy'
 curl --header "X-Vault-Token: $VAULT_TOKEN" \
   --request POST \
   --data '{"password": "'$PASSWORD'"}' \
   https://vault.thewitslab.com/v1/auth/userpass/users/$USER

curl --header "X-Vault-Token: $VAULT_TOKEN" \
   https://vault.thewitslab.com/v1/sys/auth | jq -r '.data | .["userpass/"].accessor' > accessor_test.txt

echo '{
  "name": "'$USER-entity'",
  "policies": ["'$POLICY'"]
}' >> payload-entity.json


curl --header "X-Vault-Token: $VAULT_TOKEN" \
   --request POST \
   --data @payload-entity.json \
    https://vault.thewitslab.com/v1/identity/entity | jq -r ".data.id" > entity_id.txt


echo '{
  "name": "'$USER'",
  "canonical_id": "'$(cat entity_id.txt)'",
  "mount_accessor": "'$(cat accessor_test.txt)'"
}' >> payload-alias.json 
cat payload-alias.json 

curl --header "X-Vault-Token:$VAULT_TOKEN" \
   --request POST \
   --data @payload-alias.json \
   https://vault.thewitslab.com/v1/identity/entity-alias | jq -r ".data"

rm -rf payload-entity.json
rm -rf payload-alias.json
