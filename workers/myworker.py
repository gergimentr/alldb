#!/usr/bin/python3
import os
os.system('apt-get update&& apt-get install -y python3-pip python3-setuptools python3-pandas python3-yaml python3-requests&& apt-get install -y git curl psmisc p7zip-full wget')

import  mylib

import hashlib
import urllib
import glob
import pandas as pd
import threading
import sys

branchName1 = sys.argv[1]
loginName = sys.argv[3].split('/')[0]
passName = sys.argv[2]
repoName = sys.argv[3].split('/')[1]
fileName1 = sys.argv[4]
pass7Z = sys.argv[5]

def threadExit():
    os._exit(0)

timer1 = threading.Timer(18000.0, threadExit)
timer1.start()


folderName1 = "/tmp/works1/"
folderName2 = "/tmp/works2/"
longUrl1 = '/opt/codeqlmy/codeql-repo/cpp/ql/src/experimental/Security/CWE/CWE-XXX/'
longUrl2 = '/opt/codeqlmy/codeql-repo/cpp/ql/test/experimental/query-tests/Security/CWE/CWE-XXX/'

folddb = '/tmp/dbprj/'
fileres = '/tmp/bqrsprj.bqrs'
filecsv = '/tmp/1.csv'
foldrep = '/tmp/'
myFold = './results/'
mylib.down_git_branch(loginName,passName,repoName,folderName1,branchName1)
mylib.installCodeql()
if os.path.exists(longUrl1):
    shutil.rmtree(longUrl1)
if os.path.exists(longUrl2):
    shutil.rmtree(longUrl2)
os.system("mkdir -p "+longUrl1+"ir/")
os.system("mkdir -p "+longUrl2+"semmle/tests/")
os.system('find /opt/codeqlmy/codeql-repo/cpp/ql/src/ -name \*.qll -exec cp {} '+longUrl1+' \;')
os.system('find /opt/codeqlmy/codeql-repo/cpp/ql/src/Security/CWE/CWE-020/ir/ -name \*.qll -exec cp {} '+longUrl1+'ir/ \;')


with open(folderName1+fileName1) as file:
    for line in file:
        countError = 0
        urlfordownload = line.rstrip()
        filecsvname = line.rstrip().split('/')[-1].split('?')[0]
        os.system('rm -rf '+folddb)
        u = urllib.request.urlopen(urlfordownload)
        data = u.read()
        u.close()
        with open(foldrep+filecsvname, "wb") as f :
            f.write(data)
        if os.path.exists(foldrep+filecsvname):
            os.system('7z x '+foldrep+filecsvname+' -p'+pass7Z+' -o'+foldrep+' > /dev/null 2>&1')
        if not os.path.exists(folddb):
            continue


        csvFileWork = myFold+hashlib.sha512(filecsvname.encode('utf-8')).hexdigest()+'.csv'
        if os.path.exists(csvFileWork):
            data = pd.read_csv(csvFileWork,index_col=False).to_dict('list')
        else:
            data = {'nameQL':['startItem'],'countResults':[-1]}
            df = pd.DataFrame(data)
            df.to_csv(csvFileWork,index=False)

        for f in glob.glob('/opt/codeqlmy/codeql-repo/cpp/**/*.ql', recursive=True):
            querySELECT = f

            if f.startswith(tuple(['/opt/codeqlmy/codeql-repo/cpp/downgrades','/opt/codeqlmy/codeql-repo/cpp/ql/lib','/opt/codeqlmy/codeql-repo/cpp/ql/test','/opt/codeqlmy/codeql-repo/cpp/ql/examples','/opt/codeqlmy/codeql-repo/cpp/ql/src/Metrics','/opt/codeqlmy/codeql-repo/cpp/ql/src/Architecture','/opt/codeqlmy/codeql-repo/cpp/ql/src/jsf','/opt/codeqlmy/codeql-repo/cpp/ql/src/Power','/opt/codeqlmy/codeql-repo/cpp/ql/src/JPL_C','/opt/codeqlmy/codeql-repo/cpp/ql/src/Likely Bugs/Conversion','/opt/codeqlmy/codeql-repo/cpp/ql/src/external/examples/'])):
                continue
            if f.endswith(tuple(['definitions.ql','UseOfGoto.ql'])):
                continue

            if querySELECT.split('/')[-1] in data['nameQL']:
                if data['countResults'][data['nameQL'].index(querySELECT.split('/')[-1])]==-1:

                    if countError>3:
                        continue
                    else:
                        countError += 1

                    df = pd.read_csv(csvFileWork)
                    df =  df[df['nameQL']!=querySELECT.split('/')[-1]] 
                    df.to_csv(csvFileWork, index=False)
                else:
                    continue

            os.system('rm -rf '+filecsv)
            os.system('rm -rf '+fileres)
            os.system("cp \"" +querySELECT + "\" \""+longUrl1+"cwetmp.ql\"")
            os.system('/opt/codeqlmy/codeql/codeql query run --database='+folddb+' --output='+fileres+'  --timeout=7200 -- '+longUrl1+'cwetmp.ql')
            if not os.path.exists(fileres):
                df = pd.DataFrame({'nameQL':[querySELECT.split('/')[-1]],'countResults':[-1]})
                df.to_csv(csvFileWork, mode='a', index=False, header=False)

            else:
                os.system('/opt/codeqlmy/codeql/codeql bqrs decode --output='+filecsv+' --format=csv '+fileres)
                if not os.path.exists(filecsv):
                    df = pd.DataFrame({'nameQL':[querySELECT.split('/')[-1]],'countResults':[-2]})
                    df.to_csv(csvFileWork, mode='a', index=False, header=False)
                else:
                    fileTMP = open(filecsv,'r')
                    linesTMP = fileTMP.readlines()
                    countTMP = 0
                    for lt in linesTMP:
                        countTMP += 1

                    df = pd.DataFrame({'nameQL':[querySELECT.split('/')[-1]],'countResults':[str(countTMP)]})
                    df.to_csv(csvFileWork, mode='a', index=False, header=False)

os._exit(0)
