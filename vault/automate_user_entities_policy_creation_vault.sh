#!/bin/bash
parent_file="testfile.txt"
VAULT_TOKEN='<VAULT_TOKEN>'
VAULT_ADDR='http://localhost:8200'
while read user_name user_Project
do  

gitlab_response=$(curl \
  --header "X-Vault-Token: glpat-kuTis3vXZkVzYygKoGo6" \
  --request GET \
  "https://<GITLAB_DOMAIN>/api/v4/users?username=$user_name" \
  2>/dev/null)

if [ "$gitlab_response" == "[]" ];then
   echo "no user exists in gitlab with username $user_name"
else
   ####################Create Policy########################################################################
    my_list=()
    for secret_path in ${user_Project//,/ }
        do  
        my_list+=("$secret_path")
        done  
    python3 policy.py "${my_list[@]}"
    curl --header "X-Vault-Token: $VAULT_TOKEN" --request POST --data @vault-policy.json "$VAULT_ADDR/v1/sys/policy/$user_name-policy"

########################END OF POLICY CREATION##################################################################

########################CREATE USER###########################################################################

response=$(curl \
  --header "X-Vault-Token: $VAULT_TOKEN" \
  --request GET \
  "$VAULT_ADDR/v1/auth/userpass/users/$user_name" \
  2>/dev/null)

# Check response status code
status=$(echo "$response" | jq -r  '.errors')
if [ "$status" != "null" ]; then
    chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    num=$(awk 'BEGIN{srand();print int(rand()*1000000000000)}')
    password=$(echo $chars$num | sed 's/\(.\)/\1\n/g' | sort -R | tr -d '\n' | head -c 12)
    PASSWORD=$user_name@$password
    json=$(curl --header "PRIVATE-TOKEN: glpat-kuTis3vXZkVzYygKoGo6" "https://<GITLAB_DOMAIN>/api/v4/users?username=$user_name" | jq '.[] | select(.username == "'$user_name'")')
    user_email=$(echo $json | jq -r '.email')
    #python3 send_mail.py "$user_name" "$PASSWORD" "$user_email"
    echo "$user_name       $PASSWORD           $user_email" >> password.json

    curl --header "X-Vault-Token: $VAULT_TOKEN" \
    --request POST \
    --data '{"password": "'$PASSWORD'"}' \
    $VAULT_ADDR/v1/auth/userpass/users/$user_name

    curl --header "X-Vault-Token: $VAULT_TOKEN" \
    $VAULT_ADDR/v1/sys/auth | jq -r '.data | .["userpass/"].accessor' > accessor_test.txt
fi


########################END OF CREATE USER###########################################################################


############ ENTITY CREATION ######################################################## 

echo '{
  "name": "'$user_name-entity'",
  "policies": ["'$user_name-policy'"]
}' >> payload-entity.json



curl --header "X-Vault-Token: $VAULT_TOKEN" \
   --request POST \
   --data @payload-entity.json \
    $VAULT_ADDR/v1/identity/entity | jq -r ".data.id" > entity_id.txt

############END OF  ENTITY CREATION ######################################################## 

#####################  ALIAS CREATION ########################################################

echo '{
  "name": "'$user_name'",
  "canonical_id": "'$(cat entity_id.txt)'",
  "mount_accessor": "'$(cat accessor_test.txt)'"
}' >> payload-alias.json 


curl --header "X-Vault-Token: $VAULT_TOKEN" \
   --request POST \
   --data @payload-alias.json \
   $VAULT_ADDR/v1/identity/entity-alias | jq -r ".data"

######################END OF ALIAS CREATION############################################  
fi
rm -rf payload-entity.json
rm -rf payload-alias.json
rm -rf entity_id.txt
rm -rf accessor_test.txt
rm -rf vault-policy.json

done < "$parent_file"

