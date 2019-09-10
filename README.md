# NuBank Test Code

This is the project described at `Exercise.md`

It receives a small batch transactions in JSON format file from Stdin.

It reads every transaction, line by line, validates each one against Account() entity by Validator() and,
if validation passes, the transaction is committed by AccountManager().

The result of each transactions are shown at the terminal as an JSON format,
according to the `Exercise.md` requirement.

## Software Architecture
I decide to use *Chain of Responsibility* design pattern for validations.

Each validation(referred as a Constraint type object), is added to a chain. When a
transaction needs to be validated, the event is passed thru the whole chain by a
Validator() class.

This pattern allows the code to be more decoupled, simple and maintainable.

I also used the latest *Python 3* programming language for this test, as Python is one
of the cleanest and easiest to read languages available nowadays.

## Running it locally

#### 1 - Build the Docker image
`docker-compose build`

#### 2- Execute locally
`docker-compose run app python3 main.py < operations.json`

## Running unit tests
`docker-compose run app python3 -m unittest discover`
