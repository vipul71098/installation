import sys
policy=''
for arg in sys.argv[1:]:
    arg=arg.strip()
    policy += '\\npath \\"dev/data/'+arg+'\\" { capabilities = [\\"read\\",\\"update\\",\\"list\\"]}'
finalPolicy='{"policy": "path \\"dev/*\\" { capabilities = [\\"list\\", \\"create\\"] } \\npath \\"cubbyhole/*\\" { capabilities = [\\"deny\\"]} '+policy+'"}'
vault_policy_file=open("vault-policy.json","w")
t1=vault_policy_file.write(finalPolicy)
vault_policy_file.close()
