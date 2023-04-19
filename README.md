Video Series Example Source Code
---------------------------------

Sample code used in the Algorand Developers video series

https://www.youtube.com/@algodevs/playlists


# Setup 

1. Install [algokit](https://github.com/algorandfoundation/algokit-cli) 
2. Run Docker
3. Launch Algorand localnet with `algokit localnet start`

For a detailed setup guide, watch [Development Environment Setup video](https://youtube.com/playlist?list=PLwRyHoehE434xvOtN6iwwGDHcZuyad0SN)

## Python

```sh
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the scripts like: 

```sh
python accounts/create_account.py
```

## JavaScript

```sh
cd javascript
npm install
```

Then run the scripts like:

```sh
npm run create-account
```

## Smart Contracts

### Master Beaker

Open project folders individually.

```sh
algokit bootstrap all
```

Then run deploy scripts like:

```sh
python3 deploy.py
```

### Master PyTeal

Open vscode at `master-pyteal` folder level.

```sh
cd smart-contracts/master-pyteal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the scripts like: 
```sh
python3 what_is_pyteal/counter.py
```

# Video Playlists


- [Master PyTeal Playlist](https://www.youtube.com/watch?v=yEFUv760I8A&list=PLwRyHoehE435ttTjvFZA-DyqHYIYc26K_&ab_channel=AlgorandDevelopers)

    - [Code](smart-contracts/pyteal) 


- [Transactions Explained Playlist](https://www.youtube.com/watch?v=V-tuqNx8GRI&list=PLwRyHoehE4341Vctov5Uj6Z3Dko1_MRBF&ab_channel=AlgorandDevelopers)

    - [JavaScript](javascript/src/transactions)
    - [Python](python/transactions)

- [Accounts Explained Playlist](https://www.youtube.com/watch?v=TnpGO0P0BA0&list=PLwRyHoehE437YMCUb0oiPI-lIKKIND3xZ&ab_channel=AlgorandDevelopers)

    - [JavaScript](javascript/src/accounts)
    - [Python](python/accounts)
