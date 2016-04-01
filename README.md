# httptimer
Execute Timing Attacks on Web Applications

## Prerequisites 
Python requests module
```shell
$ pip install requests
```

## How To Run
To view the required arguments, run the following command.

```shell
$ python -h httptimer.py
```

The following options must be specified:
* Target URL
* Number of requests to send (per guess)
* Message that displays on the page when there is a failed login
* The username to use when logging in
* The characterset to use
* The variable names of the input fields in the HTML form for the username and password field (POST request username and password fields, defaults to 'username' and 'password')

Additionally, a known correct password can be specified (--poc-password). The timing attack will run until each character matches the known password. If a character does not match, the test will restart from the first character.

## Sample Execution
```shell
$ python httptimer.py --url http://localhost:3000/login -n 2000 -F 'Invalid username/password combination' -u test --poc-password 'abc'
```
