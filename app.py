from blockchain import block, transaction, Blockchain, vectorblock, vectortransaction, vectornodes
# from blockchain import *
import json
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import requests
import argparse


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block()
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transactions': parse_vector(block.transactions, "transactions"),
        'proof': block.proof,
        'previous_hash': block.prev_hash,
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': 'Transaction will be added to Block ' + str(index)}

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': parse_vector(blockchain.chain, "chain"),
        'length': blockchain.chain.size(),
    }
    py_to_cpp(response['chain'], "chain")
    # py_to_cpp([{"sender": "me", "recipient": "you", "amount": 1}, {"sender": "him", "recipient": "her", "amount": 2}], "transactions")
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        parsed_node = urlparse(node).netloc
        blockchain.register_node(parsed_node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': parse_vector(blockchain.nodes),
    }
    return jsonify(response), 200


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    response = None
    for node in blockchain.nodes:
        get_nodes = requests.get('http://' + node + '/chain')

        replaced = None
        if get_nodes.status_code == 200:
            chain = get_nodes.json()['chain']

            replaced = blockchain.resolve_conflicts(py_to_cpp(chain, "chain"))

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': parse_vector(blockchain.chain, "chain")
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': parse_vector(blockchain.chain, "chain")
            }
    return jsonify(response), 200


def parse_vector(vector, vector_type="normal"):
    vector_list = []
    if vector_type == "chain":
        for i in range(vector.size()):
            block_dict = {}
            block_dict['index'] = vector[i].index
            block_dict['timestamp'] = vector[i].timestamp
            block_dict['transactions'] = parse_vector(vector[i].transactions, "transactions")
            block_dict['proof'] = vector[i].proof
            block_dict['prev_hash'] = vector[i].prev_hash
            vector_list.append(block_dict)
            block_dict = {}

    elif vector_type == "transactions":
        for i in range(vector.size()):
            transaction_dict = {}
            transaction_dict['sender'] = vector[i].sender
            transaction_dict['recipient'] = vector[i].recipient
            transaction_dict['amount'] = vector[i].amount
            vector_list.append(transaction_dict)
            transaction_dict = {}

    elif vector_type == "normal":
        for i in range(vector.size()):
            vector_list.append(vector[i])

    return vector_list


def py_to_cpp(obj_to_covert, obj_to_covert_type):
    if obj_to_covert_type == "chain":
        # Create a vector of blocks
        chain_vector = vectorblock()
        chain = obj_to_covert
        for each_block in chain:
            # Create a c++ block struct
            block_struct = block()
            block_struct.index = each_block['index']
            block_struct.prev_hash = each_block['prev_hash']
            block_struct.proof = each_block['proof']
            block_struct.timestamp = each_block['timestamp']
            block_struct.transactions = py_to_cpp(each_block['transactions'], "transactions")
            chain_vector.push_back(block_struct)
        return chain_vector

    if obj_to_covert_type == "transactions":
        # Create a vector of transactions
        transaction_vector = vectortransaction()
        transactions = obj_to_covert
        for each_transaction in transactions:
            # Create a c++ transaction struct
            transaction_struct = transaction()
            transaction_struct.sender = each_transaction['sender']
            transaction_struct.recipient = each_transaction['recipient']
            transaction_struct.amount = each_transaction['amount']
            transaction_vector.push_back(transaction_struct)
        return transaction_vector


# check if argparse value is positive
def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--port', default='5000', help='pass a port to start server on', type=check_positive)
    arguments = argument_parser.parse_args()

    app.run(host='0.0.0.0', port=arguments.port, debug=True)
