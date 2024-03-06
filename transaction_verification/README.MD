# OVERVIEW:
- Transaction verification microservice is used to verify a transaction.
- There are several different methods to verify a transaction. Including regular expressions in card numbers (it should be 16 digits) or the date of card expire data and the expression of CVV (it should be 3 digits).
- if all these checks are successful, the transaction is pretty much verified. The logic should be improved in the future.