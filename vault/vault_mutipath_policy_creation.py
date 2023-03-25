import sys
mystr=''
for arg in sys.argv[1:]:
    arg=arg.strip()
    mystr += '\\npath \\"dev/data/'+arg+'\\" { capabilities = [\\"read\\", \\"create\\",\\"update\\",\\"list\\"]}'
str2='{"rules": "path \\"dev/*\\" { capabilities = [\\"list\\"] } \\npath \\"dev/cubbyhole/*\\" { capabilities = [\\"deny\\"]} '+mystr+'"}'
test=open("vault-policy.json","w")
t1=test.write(str2)
test.close()
