#include <iostream>
#include <ctime>
#include <algorithm>

#include "blockchain.h"
#include "sha256.h"

// Constructor
Blockchain::Blockchain(){
    // Genesis block
    new_block(100, "1");
};


/**
    Creates a new block, clears all current transactions, adds the block to the chain

    @param proof: Senders address
    @param prev_hash: hash of the previous block, default will find the previous blocks hash automatically
    @return: Newest block
*/
block Blockchain::new_block(unsigned long int proof, const std::string& prev_hash = ""){
    std::string temp_prev_hash;
    block last;

    // If a hash is provided, use that hash, else get the hash of the last block.
    if(!prev_hash.empty()){
        temp_prev_hash = prev_hash;
    }else{
        last = last_block();
        temp_prev_hash = hash(&last);
    }
    
    // Create a new block
    block newly_create_block = {chain.size() + 1, time(NULL), current_transactions, proof, temp_prev_hash};
    
    // Clear all transactions so the next block will get all new transactions
    current_transactions.clear();
    
    // Append to chain
    chain.push_back(newly_create_block);
    
    return newly_create_block;
};


/**
    Returns the last block in the chain

    @return: Last block in the chain
*/
block Blockchain::last_block(){
    return chain.back();
};


/**
    Creates a new transaction and adds it to the current_transaction vector

    @param sender: Senders address
    @param recipient: Recipients address
    @param amount: Amount to send
    @return: Index of the new transaction
*/
int Blockchain::new_transaction(const std::string& sender, const std::string& recipient, double amount)
{ 
    transaction new_transaction = {sender, recipient, amount};

    // Add the transaction to the current_transactions vector
    current_transactions.push_back(new_transaction);
    
    return last_block().index + 1;
};


/**
    Creates a SHA-256 hash of a Block.

    @param block: The block struct to be hashed
    @return: SHA-256 hash in hex format
*/
std::string Blockchain::hash(block *block)
{
    std::string input;

    input = std::to_string(block->index) + 
            std::to_string(block->timestamp) +
            std::to_string(block->proof) +
            block->prev_hash;
    std::string hash = sha256(input);

    return hash;
}

/**
    Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        @param last_proof: Previous Proof
        @param proof: Current Proof
        @return: True if correct, False if not.
*/
bool Blockchain::valid_proof(unsigned long int last_proof, unsigned long int proof)
{
    std::string guess = std::to_string(last_proof) + std::to_string(proof);
    std::string guess_hash = sha256(guess);
    std::string difficulty = "0000";

    // Check if the first characters in guess_hash are equal to the difficulty
    return guess_hash.compare(0, difficulty.size(), difficulty) == 0;
}

/**
    Simple proof of work algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof

    @param last_proof: Proof of the previous block
    @return: New proof
*/
unsigned long int Blockchain::proof_of_work(unsigned long int last_proof)
{
    unsigned long int proof = 0;

    while(!valid_proof(last_proof, proof)){
        proof += 1;
    }
    return proof;
}

/**
    Add a new node to the list of nodes

    @param address: Address of node. Eg. 'http://192.168.0.5:5000'
*/
void Blockchain::register_node(const std::string& address)
{
    // Checks if the address already exists in the vector
    if(!(std::find(nodes.begin(), nodes.end(), address) != nodes.end())) {
        // If the address does not exist, add it
        nodes.push_back(address);
    }
}

/**
    Deterimine if a given blockchain is valid

    @param chain: A blockchain
    @return: True if valid, False if not
*/
bool Blockchain::valid_chain(const std::vector<block> &passed_chain)
{
    // Point to the previous block
    block prev_block = passed_chain[0];
    int current_index = 1;

    while((unsigned long)current_index < passed_chain.size()){
        // Point to the current block
        block cur_block = passed_chain[current_index];
        // If the prev_hash of the current block is not equal to the hash of the prev_block, return false 
        if(cur_block.prev_hash != hash(&prev_block)){
            return false;
        }
        // Validate the proof of the previous block and the current block, if invalid return false
        if(!valid_proof(prev_block.proof, cur_block.proof)){
            return false;
        }

        // Point previous block to current block
        prev_block = cur_block;
        current_index += 1;

    }
    return true;
}

/**
    This is our Consensus Algorithm, it resolves conflicts
    by replacing our chain with the longest one in the network.

    @return: True if our chain was replaced, False if not
*/
bool Blockchain::resolve_conflicts(const std::vector<block> &passed_chain)
{
    // We're only looking for chains longer than ours
    size_t max_length = chain.size();

    // Check if the passed chain is longer than the current chain and that the chain is valid
    if(passed_chain.size() > max_length && valid_chain(passed_chain)){
        max_length = passed_chain.size();
        // Replace the current chain with the passed chain
        chain = passed_chain;
        return true;
    }
    return false;

}

int main()
{
    Blockchain oldchain;
    // oldchain.new_block(35293);
    // badchain.new_block(250, "135135");

    Blockchain obj;
    // std::cout << obj.proof_of_work(100) << std::endl;
    // obj.new_block(35293);
    // std::cout << oldchain.resolve_conflicts(obj.chain) << std::endl;
    // std::cout << obj.chain[1].prev_hash << std::endl;
    // std::cout << obj.valid_chain(badchain.chain) << std::endl;


    // obj.proof_of_work(100);

    return 0;
}
