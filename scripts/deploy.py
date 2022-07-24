from solcx import compile_standard, install_solc
from web3 import Web3
from json import loads, dump, load

my_address = load(open("keys.json"))['address']
private_key = load(open("keys.json"))['private-key']
# Rinkeby Testnet
network: str = "https://rinkeby.infura.io/v3/a1ab67fb7e55483ca8d406fb6a9a83e9"
chainId: int = 4
solc_version = "0.8.7"

w3 = Web3(Web3.HTTPProvider(network))
if w3.isConnected() == True:
	print("Connected to Rinkeby Testnet")

def getNonce(address):
	return w3.eth.getTransactionCount(my_address)

nonce = getNonce(my_address)

txnParams = {
	"chainId": chainId,
	"gasPrice": w3.eth.gas_price,
	"from": my_address,
	"nonce": getNonce(my_address) + 1,
}

with open("./contracts/SimpleStorage.sol") as file:
	source = file.read()

print("Compiling ./contracts/SimpleStorage.sol")
try:
	# Solidity source code
	compiled = compile_standard(
	    {
	        "language": "Solidity",
	        "sources": {"SimpleStorage.sol": {"content": source}},
	        "settings": {
	            "outputSelection": {
	                "*": {
	                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
	                }
	            }
	        },
	    },
	    solc_version=solc_version,
	)
except:
	print(f"An error occurred during compilation. Error: {e}")

print("Dumping to SimpleStorage.json")
dump(compiled, open("../artifacts/SimpleStorage.json", "w"))

bytecode = compiled["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
"bytecode"]["object"]

abi = loads(
	compiled["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
	)["output"]["abi"]


# Initialize contract
print("Deploying SimpleStorage contract...")
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
# Deploy the contract
txn = contract.constructor().buildTransaction(
	{
		"chainId": chainId,
		"gasPrice": w3.eth.gasPrice,
		"from": my_address,
		"nonce": nonce,
	}
)
print("Signing first transaction...")
# Sign the transaction with private key
signed_txn = w3.eth.account.sign_transaction(txn, private_key = private_key)

print("Sending first transaction...")
# Send transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("Waiting for Txn receipt...")
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print(f"Contract deployed @ {txn_receipt.contractAddress}")

print("Initializing SimpleStorage contract")
SimpleStorage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

print("Calling first function...")
favouriteNumber = SimpleStorage.functions.retrieve().call()
print("Favourite Number: {}".format(favouriteNumber))


# number = 100
# firstTxn = SimpleStorage.functions.store(number).buildTransaction(txnParams)

# firstTxn = w3.eth.account.sign_transaction(firstTxn, private_key=private_key)

# firstTxn = w3.eth.send_raw_transaction(firstTxn.rawTransaction)

# print(f"Updating favouriteNumber to {number}...")
# firstTxn_receipt = w3.eth.wait_for_transaction_receipt(firstTxn)

# favouriteNumber = SimpleStorage.functions.retrieve().call()
# print("Favourite Number: {}".format(favouriteNumber))

person = {
	"name": "Manuel",
	"favouriteNumber": 50
}

txnParams.update({"nonce":txnParams['nonce']+1})
print(txnParams)
secondTxn = SimpleStorage.functions.addPerson(person['name'], person['favouriteNumber']).buildTransaction(txnParams)

secondTxn = w3.eth.account.sign_transaction(secondTxn, private_key=private_key)

secondTxn = w3.eth.send_raw_transaction(secondTxn.rawTransaction)

print(f"Updating people with {person['name']} and {person['favouriteNumber']}...")
secondTxn_receipt = w3.eth.wait_for_transaction_receipt(secondTxn)

people = SimpleStorage.functions.people(0).call()
print(f"People = {people}")