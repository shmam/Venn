import sys
import requests

# importing the client keys
# MAKE YOUR OWN config.py FILE WITH YOUR CLIENT_ID AND CLIENT SECRET
import config

# Linear Algebra Packages
import numpy
from numpy import array
from numpy import linalg as lin


grant_type = 'client_credentials'
body_params = {'grant_type' : grant_type}



def client_auth():
    url='https://accounts.spotify.com/api/token'

    # probaby redundant doing two of the same request
    req = requests.post(url, data=body_params, auth = (config.client_id, config.client_secret))

    # trying out tuples for the first time becasue why not
    return req.json()["access_token"], req.status_code

def artist_id(token,query,limit):
    url = 'https://api.spotify.com/v1/search?query='+query+'&type=artist&market=US&offset=0&limit=' + limit
    art_id = requests.get(url, headers={"Authorization": 'Bearer ' + token}).json()['artists']['items'][0]['id']
    return art_id

def artist_name(token,query):
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

    search_term = str(sys.argv[1])

    print(" Graph Partiton: " + search_term)
    print(" ---------------------------------------------")


    register = client_auth()
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

        d = []
        for i in range(len(list)):
            row_sum = 0
            for j in range(len(list)):
                 row_sum += Adj[j][i]

            d.append(row_sum)

        sum_D = numpy.sum(d)

        print(" > constructing the probability matrix ... ")

        P = numpy.empty(((len(list),len(list))))

        for i in range(len(list)):
            for j in range(len(list)):
                P[i][j] = (d[i] * d[j]) / sum_D


        M = numpy.subtract(Adj,P)

        print(" > eigen-decomposition of modular matrix ... ")

        w , V = lin.eig(M)

        c1 = []
        c2 = []

        for i in range(len(list)):
            if(V[0][i] < 0):
                c1.append(artist_name(register[0],list[i]))
            else:
                c2.append(artist_name(register[0],list[i]))

        print("G1: ", c1)
        print("G2: ", c2)

if (__name__ == "__main__") : main()
