# Venn


[![Build Status](https://travis-ci.com/shmam/Spotify-Graph-Partition.svg?branch=master)](https://travis-ci.com/shmam/Spotify-Graph-Partition)



## About

The Spotify Web API is a great resource for pulling data about musical artists, especially a list of related artists. While this is helpful for discovering new music, it can also be used to identify seperate factions of artists within this inital grouping. 

![GitHub Logo](/img/demo.gif)

First a grouping of artists is treated like a digraph, where an arc spans from artist **a** to artist **b** if Spotify says artist **b** is in artist's **a**'s related artists list. Using this Graph **G**, we then partition this into two distinct subgraphs (**G1** and **G2**) where the number of edges kept is maximized. 

![digraph](https://qph.fs.quoracdn.net/main-qimg-0563516a0d43b1653e59ce5c838d9b46)

The method for determining this graph partition was initally found by M. Newman in his paper *[Finding community structure in networks using the eigenvectors of matrices.](https://arxiv.org/pdf/physics/0605087v3.pdf)* This is a very extensive process that has been reduced to a functional algorithm: 
1. Find adjanceny matrix (A) of G, and degree vector (d) of A
2. Find the probability matrix (P) where p(i,j) ≈ (d[i] * d[j]) / ∑d
3. Compute the modular matrix M: M = A - P
4. Find eigenvectors V from the eigen decomposition of M
5. Looking at the first column in V, if the value is *negative* that row is in one group and if *positive* that row is in the other group

## Usage

Run this tool through the command line in a virtual env, with the inital artist's name in single quotes 
```shell
$ python request.py '<artist_name>'
```

### Auto Installation

Make use of cool pip features, and automatically install relevant dependencies with `pip install -r requirements.txt`

Then run the create and run the virtual enviroment
```shell
$ virtualenv -p python3 myvenv
$ source myvenv/bin/activate
```

### Manual Installation:

1. Make sure you have installed virtualen, or if not then run `pip install virtualenv`
2. Creating the python three virtual enviroment
 `virtualenv -p python3 myvenv`[]
3. Start the enviroment `source myvenv/bin/activate`
4. Install the pyton requests package `pip install requests`
5. Install numpy `pip install numpy`

## Credit 
- Shoutout to the @Spotify team for an awesome public API :musical_note: :cake:
- Shoutout to [requests](https://github.com/requests) for a great HTTP tool for humans :tada:
- Thank you to [Dr. Hoon Hong](http://www4.ncsu.edu/~hong/) for covering this method in [MA305](http://www4.ncsu.edu/~hong/MA305/syllabus.html) :books:
- Thank you to M. Newman for the inital paper, *[Finding community structure in networks using the eigenvectors of matrices](https://arxiv.org/pdf/physics/0605087v3.pdf)*
