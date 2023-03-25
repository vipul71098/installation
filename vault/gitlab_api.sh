/bin/bash
PRIVATE_TOKEN='WEW'
curl --request GET --header "PRIVATE-TOKEN: $PRIVATE_TOKEN" "https://<gitlab_domain>/api/v4/projects?per_page=200"  | jq  > example.json
echo "PROJECT ID, PROJECT NAME" > test.csv
cat example.json | jq -c '.[]'  | while read obj; do
   name=$(echo $obj | jq -r '.name')
   id=$(echo $obj | jq -r '.id')
   echo "$id  $name" >> test.csv
done

curl --request GET --header "PRIVATE-TOKEN: $PRIVATE_TOKEN" "https://<gitlab_domain>/api/v4/users?per_page=200" | jq > users.json
echo "USERS ID, USERS NAME"    "USER_EMAIL" > users.csv
cat users.json | jq -c '.[]'  | while read obj; do
   username=$(echo $obj | jq -r '.username')
   user_id=$(echo $obj | jq -r '.id')
   commit_email=$(echo $obj | jq -r '.commit_email')
   echo "$user_id  $username   $commit_email" >> users.csv
done

cat test.csv

cat users.csv
user_name='vipul.shuklas'
json=$(curl --header "PRIVATE-TOKEN: $PRIVATE_TOKEN" "https://<gitlab_domain>/api/v4/users?username=$user_name" \
  | jq '.[] | select(.username == "'$user_name'")')
  commit_email=$(echo $json | jq -r '.email')
echo $commit_email

gitlab_response=$(curl \
  --header "X-Vault-Token: $PRIVATE_TOKEN" \
  --request GET \
  "https://<gitlab_domain>/api/v4/users?username=$user_name" \
  2>/dev/null)

if [ "$gitlab_response" == "[]" ];then
   echo "no user exists in gitlab with username $user_name"
else
   echo "user exists : $user_name"
fi
