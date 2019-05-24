import blockchain
import json
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import requests


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


# Instantiate the Blockchain
blockchain = blockchain.Blockchain()


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
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        parsed_url = urlparse(node)
        blockchain.register_node(parsed_url.netloc)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': parse_vector(blockchain.nodes),
    }
    return jsonify(response), 200


# MUST FIX CONSENSUS

# @app.route('/nodes/resolve', methods=['GET'])
# def consensus():
#     response = None
#     for node in blockchain.nodes:
#         get_nodes = requests.get('http://' + node + '/chain_ptr')
#         print(get_nodes.json()['chain_ptr']['this'])

#     #     replaced = None
#     #     if get_nodes.status_code == 200:
#     #         chain = get_nodes.json()['chain_ptr']['this']

#     #         replaced = blockchain.resolve_conflicts(chain)

#     #     if replaced:
#     #         response = {
#     #             'message': 'Our chain was replaced',
#     #             'new_chain': parse_vector(blockchain.chain, "chain")
#     #         }
#     #     else:
#     #         response = {
#     #             'message': 'Our chain is authoritative',
#     #             'chain': parse_vector(blockchain.chain, "chain")
#     #         }
#     # return jsonify(response), 200
#     return "done"


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
