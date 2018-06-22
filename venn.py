import sys
import os.path
import requests


# Linear Algebra Packages
import numpy
from numpy import array
from numpy import linalg as lin

from graph_modules.partition import newman_partiton


grant_type = 'client_credentials'
body_params = {'grant_type' : grant_type}


def client_auth(ci,cs):
    url='https://accounts.spotify.com/api/token'
    req = requests.post(url, data=body_params, auth = (ci, cs))

    # trying out tuples for the first time becasue why not
    return req.json()["access_token"], req.status_code

def artist_id(token,query,limit):
    url = 'https://api.spotify.com/v1/search?query='+query+'&type=artist&market=US&offset=0&limit=' + limit
    art_id = requests.get(url, headers={"Authorization": 'Bearer ' + token}).json()['artists']['items'][0]['id']
    return art_id

def artist_name(token,query):

    if(query == '' or query == None):
        return 'ERROR: INVALID QUERY'

    if(token == '' or token == None):
        return 'ERROR: INVALID TOKEN'

    url = 'https://api.spotify.com/v1/artists/' + query
    return requests.get(url,headers={"Authorization": 'Bearer ' + token}).json()['name']


def network(token,query):
    url = 'https://api.spotify.com/v1/artists/'+query+'/related-artists'
    data = requests.get(url, headers={"Authorization": 'Bearer ' + token}).json()['artists']
    a = [query]
    for x in data:
        # print(x['name'], x['id'])
        a.append(x['id'])

    return a



def main():

    if(os.path.exists('./config.py')):
        # importing the client keys
        # MAKE YOUR OWN config.py FILE WITH YOUR CLIENT_ID AND CLIENT SECRET

        import config
        ci = config.client_id
        cs = config.client_secret
    else:

        # credentials used by Travis CI
        ci = CLIENTID
        cs = CLIENTSECRET


    # Taking the argument value in parenthesis to be the inital artist
    search_term = str(sys.argv[1])

    print(" Graph Partiton: " + search_term)
    print(" ---------------------------------------------")


    register = client_auth(ci,cs)
    print(" > auth with Spotify API ... ")
    if(register[1] == 200):
        list = network(register[0],artist_id(register[0],search_term,"5"))
        print(" > query for " + search_term + " and related artists ... ")


        Adj = numpy.empty(((len(list),len(list))))

        print(" > constructing adjacency matrix ... ")

        for i in range(len(list)):
            sublist = network(register[0],list[i])
            for j in range(len(list)):
                if(sublist.count(list[j]) > 0):
                    Adj[i][j] = 1
                else:
                    Adj[i][j] = 0




        groups = newman_partiton(list, Adj)

        g1 = []
        g2 = []

        for i in range(len(groups[0])):
            g1.append(artist_name(register[0],groups[0][i]))
        for i in range(len(groups[1])):
            g2.append(artist_name(register[0],groups[1][i]))

        print("\nG1: ", g1)
        print("\nG2: ", g2)
        print("\n")


if (__name__ == "__main__") : main()
