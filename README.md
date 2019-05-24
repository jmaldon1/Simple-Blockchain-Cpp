# Simple-Blockchain-C

This is a simple blockchain that is written in C and wrapped in Python

## Installation
Create the wrapper for the C code:
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
##### POST (http://localhost:5000):
**/transactions/new**

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