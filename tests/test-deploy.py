import json
from web3 import Web3
import unittest

my_address = load(open("keys.json"))['address']
private_key = load(open("keys.json"))['private-key']

# Rinkeby Testnet
network = "https://rinkeby.infura.io/v3/a1ab67fb7e55483ca8d406fb6a9a83e9"
chainId = 4

w3 = Web3(Web3.HTTPProvider(network))

def getNonce(address):
	return w3.eth.getTransactionCount(my_address)

nonce = getNonce(my_address)

params = {
	"chainId": chainId,
	"gasPrice": w3.eth.gasPrice,
	"from": my_address,
	"nonce": getNonce(nonce),
}

try:
	compiled = json.load(open("./artifacts/SimpleStorage.json"))
except FileNotFoundError:
	raise Exception("Did you run scripts/deploy.py correctly?")

class SimpleStorageTest(unittest.TestCase):
	"""Tests for SimpleStorage"""

	def test_a(self):
		self.assertEqual(w3.isConnected(), True)

	def test_b(self):
		"""Test for contract compilation"""
		global txn_receipt, abi
		
		bytecode = compiled["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
			"bytecode"]["object"]

		abi = json.loads(
			compiled["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
			)["output"]["abi"]

		contract = w3.eth.contract(abi=abi, bytecode=bytecode);
		txn = contract.constructor().buildTransaction(params)
		signed_txn = w3.eth.account.sign_transaction(txn, private_key = private_key)
		txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
		txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
		assert txn_receipt.contractAddress.startswith("0x") == True, "Contract address must begin with 0x prefix"

	def test_c(self):
		"""Test for contract deployment"""
		SimpleStorage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)
		favouriteNumber = SimpleStorage.functions.retrieve().call()

		self.assertEqual(favouriteNumber, 0, "Should start with a favourite number")

	def test_d(self):
		"""Test for store() function"""
		global txn_receipt, abi

		number = 100
		SimpleStorage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

		params.update({"nonce":params['nonce']+1})
		txn = SimpleStorage.functions.store(number).buildTransaction(params)
		txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
		txn_hash = w3.eth.send_raw_transaction(txn.rawTransaction)
		txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
		favouriteNum = SimpleStorage.functions.retrieve().call()

		self.assertEqual(favouriteNum, number, "Favourite number should update when we call store")

	def test_e(self):
		"""Test for addPeople() function"""
		global txn_receipt, abi

		SimpleStorage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

		person = {
			"name": "Manuel",
			"favouriteNumber": 50
		}

		params.update({"nonce":params['nonce']+1})
		txn = SimpleStorage.functions.addPerson(person['name'], person['favouriteNumber'])
		txn = txn.buildTransaction(params)
		txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
		txn = w3.eth.send_raw_transaction(txn.rawTransaction)
		txn_receipt = w3.eth.wait_for_transaction_receipt(txn)
		people = SimpleStorage.functions.people(0).call()
	
		with self.subTest():
			self.assertEqual(people[0], person['favouriteNumber'], "Incorrect favourite number")
		with self.subTest():
			self.assertEqual(people[1], person['name'], "Incorrect name")

if __name__ == "__main__":
    unittest.main(verbosity=2)