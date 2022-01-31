**data**

The repository contain a file named : bitcoin_mempool_data
The Data contain transactions that for each:
TXID - unique id of transaction
Size - size of bytes for each transaction
Fee - fee paid for the bytes in Satoshi(1e-8 biycoin)
Time - the time for each transaction entered to the memory pool
Removed Time- only for confirmed transactions,the time stemp of the transaction

**Part A**

A2 - A3 - implementation of greedy knapsack, the function chooses the transaction according to Satoshi per byte until no more transactions can be added.

A4 - implementation of VCG auction mechanism

**part B**

B in this part you are the bidder, your target is to get your transactions into blockchain as fast as possible, while paying the minimal possible fee to the miners.
in this part there is an implementation of two types of bidders, 'simple agent', 'forward agent'
