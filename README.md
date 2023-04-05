Video Series Example Source Code
---------------------------------

Sample code used in the Algorand Developers video series

https://www.youtube.com/@algodevs/playlists


# Setup 

Make sure you've installed [algokit](https://github.com/algorandfoundation/algokit-cli) and have the local network running.

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



# Video Playlists


- [Master PyTeal Playlist](https://www.youtube.com/watch?v=yEFUv760I8A&list=PLwRyHoehE435ttTjvFZA-DyqHYIYc26K_&ab_channel=AlgorandDevelopers)

    - [Code](smart-contracts/pyteal) 


- [Transactions Explained Playlist](https://www.youtube.com/watch?v=V-tuqNx8GRI&list=PLwRyHoehE4341Vctov5Uj6Z3Dko1_MRBF&ab_channel=AlgorandDevelopers)

    - [JavaScript](javascript/src/transactions)
    - [Python](python/transactions)

- [Accounts Explained Playlist](https://www.youtube.com/watch?v=TnpGO0P0BA0&list=PLwRyHoehE437YMCUb0oiPI-lIKKIND3xZ&ab_channel=AlgorandDevelopers)

    - [JavaScript](javascript/src/accounts)
    - [Python](python/accounts)
