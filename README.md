

### File layout

```
.
├── Dockerfile                                      # Dockerfile for kv store app
├── Dockerfile.agent                                # Dockerfile for Jenkins agent
├── Jenkinsfile                                     # Jenksinfile with build pipeline steps
├── kv_cli.py                                       # CLI to interact with the kv store
├── LICENSE                                         # MIT license. You can copy, distribute code with me non liable but give me credit.  
├── README.md                                       # The doc you are currently reading :P
├── src
│   ├── api
│   │   ├── helpers
│   │   │   ├── __init__.py
│   │   │   └── redis_client.py   # Redis helper module
│   │   └── __init__.py
│   ├── requirements.txt                      # Python app dependencies
│   ├── run.py                                # Entrypoint file
│   └── tests
│       ├── functional
│       │   ├── __init__.py
│       │   └── test_app.py             # Functional test  - uses flask test client 
│       ├── __init__.py
│       └── unit
│           ├── __init__.py
│           └── test_redis_client.py         #  Unit test for Redis client
└── watch.png                                      # Pic showing the watch functionality
```

### Python environment
- Tested with python 3.7 version.

General invocation of code is install dependencies using `pip3 install -r requirements.txt` and then do `python3 src/run.py .py`.
- Uses Redis as key value store backend. This is handled as part of redilite python package.
- Redislite package instructions at https://github.com/yahoo/redislite 

### CLI Usage
```shell
$ ./kv_cli.py 
usage: kv_cli.py [-h] {get,set,watch} ...

positional arguments:
  {get,set,watch}
    get            Use get <KEY> to fetch the value of that key from kv store.
    set            Use set <KEY> <VALUE> to create/update the key with given
                   value in kv store.
    watch          Use watch to watch updates to any keys in kv store.

optional arguments:
  -h, --help       show this help message and exit
```

### Run tests
```shell
:~/work/grofers-test$ pytest src/tests/ -v
================================================================ test session starts =================================================================
platform linux -- Python 3.7.9, pytest-6.2.1, py-1.10.0, pluggy-0.13.1 -- /usr/bin/python3.7
cachedir: .pytest_cache
rootdir: ~/work/grofers-test
collected 6 items                                                                                                                                    

src/tests/functional/test_app.py::test_get_key PASSED                                                                                          [ 16%]
src/tests/functional/test_app.py::test_set_key PASSED                                                                                          [ 33%]
src/tests/functional/test_app.py::test_delete_key PASSED                                                                                       [ 50%]
src/tests/unit/test_redis_client.py::TestRedisClient::test_get_key PASSED                                                                      [ 66%]
src/tests/unit/test_redis_client.py::TestRedisClient::test_set_key PASSED                                                                      [ 83%]
src/tests/unit/test_redis_client.py::TestRedisClient::test_remove_key PASSED                                                                   [100%]

```

