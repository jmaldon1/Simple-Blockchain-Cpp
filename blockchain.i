%module blockchain
%{
	#include "src/blockchain.h"
	#include "src/sha256.h"
	#include <time.h>
%}

%include <std_string.i>
%include <std_vector.i>
%include "src/blockchain.h"

typedef long time_t;

namespace std {
    %template(vectorblock) vector<block>;
    %template(vectortransaction) vector<transaction>;
    %template(vectornodes) vector<std::string>;
};