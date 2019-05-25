# Simple-Blockchain-C++

This is a simple blockchain that is written in C++ and wrapped in Python

## Installation
Create the wrapper for the C++ code:
```

swig -c++ -python blockchain.i

python3 setup.py build_ext --inplace

```

## Usage
How to start server:
```
python3 app.py
```

#### Methods:
##### GET (http://localhost:5000):
**/chain**

Returns the blockchain

Example Response:
```
{
    "chain": [
        {
            "index": 1,
            "prev_hash": "1",
            "proof": 100,
            "timestamp": 1558719591,
            "transactions": []
        },
        {
            "index": 2,
            "prev_hash": "92fdf2867591fc60267390781a5283ca196017d626a04a829b7e772f1c9e7735",
            "proof": 35293,
            "timestamp": 1558720246,
            "transactions": [
                {
                    "amount": 10,
                    "recipient": "you",
                    "sender": "me"
                },
                {
                    "amount": 11,
                    "recipient": "Tim",
                    "sender": "John"
                },
                {
                    "amount": 1,
                    "recipient": "7c912978f80a4c1c98efce6c9f38538f",
                    "sender": "0"
                }
            ]
        }
    ],
    "length": 2
}
```
**/mine**

mines a new block

Example Response:
```
{
    "index": 2,
    "message": "New Block Forged",
    "previous_hash": "92fdf2867591fc60267390781a5283ca196017d626a04a829b7e772f1c9e7735",
    "proof": 35293,
    "transactions": [
        {
            "amount": 10,
            "recipient": "you",
            "sender": "me"
        },
        {
            "amount": 11,
            "recipient": "Tim",
            "sender": "John"
        },
        {
            "amount": 1,
            "recipient": "7c912978f80a4c1c98efce6c9f38538f",
            "sender": "0"
        }
    ]
}
```
**/nodes/resolve**

Resolve conflicts by checking all registered nodes and replaces our chain with the longest valid chain.

Example Response:
```
{
    "message": "Our chain is authoritative",
    "chain": [
        {
            "index": 1,
            "prev_hash": "1",
            "proof": 100,
            "timestamp": 1558816247,
            "transactions": []
        },
        {
            "index": 2,
            "prev_hash": "b38d0a7fb53745125ce277c7b368b92b9cc8b1d2e01571244c6bd739d4873613",
            "proof": 35293,
            "timestamp": 1558816351,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "f331df47a8254fa5a1359722695db213",
                    "sender": "0"
                }
            ]
        },
        {
            "index": 3,
            "prev_hash": "8bf8ac14adb529fd67ddbc0b745b5331a79c8e21c93c56ca1c3b7dfb44ddb2c7",
            "proof": 35089,
            "timestamp": 1558816353,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "f331df47a8254fa5a1359722695db213",
                    "sender": "0"
                }
            ]
        }
    ]
}
```
##### POST (http://localhost:5000):
**/transactions/new**

Create a new transaction

Example send:

&nbsp;&nbsp;&nbsp;&nbsp;sender: string

&nbsp;&nbsp;&nbsp;&nbsp;recipient: string

&nbsp;&nbsp;&nbsp;&nbsp;amount: int

```
{
	"sender": "John",
	"recipient": "Tim",
	"amount": 11
}
```
Example Response:
```
{
    "message": "Transaction will be added to Block 2"
}
```

**/nodes/register**

Register a node

Example send:

&nbsp;&nbsp;&nbsp;&nbsp;nodes: array of strings

```
{
	"nodes":["http://127.0.0.1:5000"]
}
```
Example Response:
```
{
    "message": "New nodes have been added",
    "total_nodes": [
        "127.0.0.1:5000"
    ]
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Credits
[Learn blockchains by building one](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)