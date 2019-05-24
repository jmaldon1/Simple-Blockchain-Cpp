#ifndef BLOCKCHAIN_H_
#define BLOCKCHAIN_H_

#include <vector>
#include <string>

struct transaction {
    std::string sender;
    std::string recipient;
    double amount;
};

struct block {
  int index;
  time_t timestamp;
  std::vector<transaction> transactions;
  unsigned long int proof;
  std::string prev_hash;
};


class Blockchain 
{ 
    // Access specifier 
    public: 
  
    // Data Members
    std::vector<block> chain;
    std::vector<transaction> current_transactions;
    std::vector<std::string> nodes;
    
    // Constructor
    Blockchain();
  
    // Member Functions() 
    block new_block(unsigned long int proof, const std::string& prev_hash);
    int new_transaction(const std::string& sender, const std::string& recipient, double amount);
    std::string hash(block *block);
    unsigned long int proof_of_work(unsigned long int last_proof);
    bool valid_proof(unsigned long int last_proof, unsigned long int proof);
    block last_block();
    void register_node(const std::string& address);
    bool valid_chain(const std::vector<block> &passed_chain);
    bool resolve_conflicts(const std::vector<block> &passed_chain);
}; 

#endif  // BLOCKCHAIN_H_