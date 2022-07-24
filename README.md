# Basic Sample Web3py Project 

This project demonstrates a basic Web3py usecase. It comes with a sample contract, a test for that contract, a sample script that deploys the contract, and an example of task implementation which simply lists the available contracts.


## Quickstart

Start by cloning the repository:

```
git clone https://github.com/manuelinfosec/web3py-simple-storage-fcc
cd web3py-simple-storage-fcc
```

Open `keys.json` and fill in your address and its corresponding private key:
```json
{
    "address": "0xE882D838eF07e796bf6b19636931F143e3eC4Dc3",
    "private-key": ""
}
```

## Deploy
Run `scripts/deploy.py` from the project directory:
```
python3 scripts/deploy.py
```

### Deployment to a testnet or mainnet
A custom network deployment is possible by changing the HTTP provider and chain ID. The script defaults to Rinkeby testnet with chain ID, 4. Do so by editing `deploy.py` :

```python
# imports

my_address = load(open("keys.json"))['address']
private_key = load(open("keys.json"))['private-key']
# Rinkeby Testnet
network: str = "<node-url>"
chainId: int = None
solc_version = "0.8.7"

# deploy.py continues
```

Replacing `network` and `chainId` with its a node url and its chain ID, respectively. You could create a node address alongside an API key with [Infura](https://infura.io).

## Testing contracts
Next, run `tests/test-deploy.py` from the project directory:
```
python3 tests/test-deploy.py
```

## Connect with me
If you appreciate this, feel free to follow me on:

[![Manuel Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/manuelinfoec)
[![Manuel Infosec YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/c/ManuelInfosec)
[![Chiemezie Njoku Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/manuelinfosec/)
[![Manuel Medium](https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white)](https://manuelinfosec.medium.com/)

## Appreciation
You could also donate (send funds):

Ethereum/Binance Smart Chain/Polygon/Avalanche/etc address: 0xE882D838eF07e796bf6b19636931F143e3eC4Dc3
