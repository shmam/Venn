from graph_modules.partition import newman_partiton
from venn import *
import os
import numpy


if(os.path.exists('./config.py')):
    # importing the client keys for local test
    import config
    ci = config.client_id
    cs = config.client_secret
else:
    # credentials used by Travis CI
    ci = os.environ['CLIENTID']
    cs = os.environ['CLIENTSECRET']


# Testing the initial response code and making sure there is
# a token returned
def test_clientCredentials():
    response = client_auth(ci,cs)

    assert response[1] == 200
    assert response[0] != None


def test_artistName_ECP():
    response = client_auth(ci,cs)

    assert artist_name(response[0],'5aIqB5nVVvmFsvSdExz408') == 'Johann Sebastian Bach'
    assert artist_name(response[0], '6oMuImdp5ZcFhWP0ESe6mG') == 'Migos'


def test_artistName_DT1():
    response = client_auth(ci,cs)
    assert artist_name(response[0], '') == 'ERROR: INVALID QUERY'


def test_artistName_DT2():
    response = client_auth(ci,cs)
    assert artist_name(None, '3TVXtAsR1Inumwj472S9r') == 'ERROR: INVALID TOKEN'


def test_newman_ECP1():
    labels = ['1','2','3','4','5']
    G = [
            [0,0,0,1,1],
            [0,0,1,0,0],
            [0,1,0,1,0],
            [1,0,1,0,1],
            [1,0,0,1,0],
        ]
    assert newman_partiton(labels,G) == (['2','3','4'],['1','5'])


def test_newman_ECP2():
    labels = ['1','2','3','4','5']
    G = [
            [0,1,0,0,1],
            [1,0,1,0,0],
            [0,1,0,1,0],
            [0,0,1,0,0],
            [1,0,0,0,0],
        ]
    assert newman_partiton(labels,G) == (['1','2','3','4'],['5'])

def test_newman_ECP3():
    labels = ['1','2','3','4','5']
    G = [
            [0,1,1,1,1],
            [1,0,1,1,1],
            [1,1,0,1,1],
            [1,1,1,0,1],
            [1,1,1,1,0],
        ]

    print(newman_partiton(labels,G))
    assert newman_partiton(labels,G) == (['1'], ['2', '3', '4', '5'])

