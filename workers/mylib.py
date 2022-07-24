
import os
import shutil
import requests


def down_git_branch(lname,pname,rname,foldrep,branch):
    if os.path.exists(foldrep):
        shutil.rmtree(foldrep)
    os.system("git clone https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git "+foldrep)
    os.system("cd "+foldrep+"&& git fetch --all")
    os.system("cd "+foldrep+"&&git checkout "+branch+" || git checkout -b "+branch+" origin/clean")

def save_repo_branch_commit(lname,pname,rname,foldrep,branch,commit):
    os.system("cd "+foldrep+"&&git remote remove origin")
    os.system("cd "+foldrep+"&&git config --global user.name \""+lname+"\"")
    os.system("cd "+foldrep+"&&git config --global user.email "+lname+"@github.com")
    os.system("cd "+foldrep+"&&git remote add -f origin https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git")
    os.system("cd "+foldrep+"&&git checkout "+branch+" || git checkout -b "+branch+" origin/clean")
    os.system("cd "+foldrep+"&&git add -A")
    os.system("cd "+foldrep+"&&git commit -m \""+commit+"\"")
    os.system("cd "+foldrep+"&&git push origin "+branch)



def installCodeql():
    dataVersion = requests.get('https://github.com/github/codeql-cli-binaries/releases/latest')
    dataVerIns = dataVersion.text.split('<title>Release v')[1].split(' · github/codeql-cli-binaries')[0]
    
    os.system("cd /opt/&&sudo mkdir codeqlmy&&cd codeqlmy&&sudo git clone https://github.com/github/codeql.git codeql-repo") 
    os.system("cd /opt/codeqlmy&&sudo wget https://github.com/github/codeql-cli-binaries/releases/download/v"+dataVerIns+"/codeql-linux64.zip&&sudo unzip codeql-linux64.zip&&sudo rm codeql-linux64.zip")