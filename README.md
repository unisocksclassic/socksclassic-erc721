# Socksclassic ERC721 token

Socksclassic is a ERC721 compatible non fungible token.

## Requirements
* python3

## Installation

1. Clone this repo

2. Setup environment
```
python3 -m venv env
source env/bin/activate
```

3. Install dependencies  

This should work:

```
pip install -r requirements.txt
```  
  
But you might need to specify the compilers on macOS: 

```
env CC=clang CXX=clang++ pip install -r requirements.txt
```

## Testing
```
pytest -v test/
```
