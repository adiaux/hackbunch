import requests
import json
import collections
import re 

from secret import accessToken

headers = {"Authorization": "bearer "+ accessToken }

topic_query = """
        query ($name:String!){
        repositoryOwner(login:$name){
            login 
            ... on User {
            name
            avatarUrl
            pullRequests(last: 100){
                nodes{
                id
                createdAt
                additions
                deletions
                }
            }
            } 
        }
        } 
        """

class pullRequestsData:

    def __init__(self, username):
        self.variables=dict({
            "name":str(username)
        })
        self.data = {}

    def getPRData(self):
        request = requests.post('https://api.github.com/graphql', json={'query': topic_query,"variables":self.variables},headers=headers)
        if(request.status_code == 200):
            result = request.json()           
            if(result['data']['repositoryOwner'] != None):
                self.data['username'] = result['data']['repositoryOwner']['login']
                self.data['name'] = result['data']['repositoryOwner']['name']
                prsdata = {}
                for pr in result['data']['repositoryOwner']['pullRequests']['nodes']:
                    prdata = {}
                    if(re.match(r'^2019-10', pr['createdAt'])):
                        prdata['createdAt'] = pr['createdAt']
                        prdata['additions'] = pr['additions']
                        prdata['deletions'] = pr['deletions']
                        prsdata[pr['id']] = prdata
                self.data['prsdata'] = prsdata
            else:
                self.data['username'] = result['data']['repositoryOwner']

    def displayData(self):
        if(self.data['username'] != None):
            if(self.data['prsdata']):
                print(self.data)
            else:
                print("No PRs for Hacktoberfest")
        else:
            print("User doesn't exist")


if __name__ == "__main__":
    username = input("Enter the GitHub username: ")
    prData = pullRequestsData(username)
    prData.getPRData()
    prData.displayData()