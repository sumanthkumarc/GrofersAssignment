
```shell
curl -XPOST localhost:8080/key -H 'Content-Type: application/json' -d '{"name":"foo", "value":"bat"}'
```


```shell
:~/work/grofers-test$ pytest src/tests/ -v
================================================================ test session starts =================================================================
platform linux -- Python 3.7.9, pytest-6.2.1, py-1.10.0, pluggy-0.13.1 -- /usr/bin/python3.7
cachedir: .pytest_cache
rootdir: /home/vasavi/work/grofers-test
collected 6 items                                                                                                                                    

src/tests/functional/test_app.py::test_get_key PASSED                                                                                          [ 16%]
src/tests/functional/test_app.py::test_set_key PASSED                                                                                          [ 33%]
src/tests/functional/test_app.py::test_delete_key PASSED                                                                                       [ 50%]
src/tests/unit/test_redis_client.py::TestRedisClient::test_get_key PASSED                                                                      [ 66%]
src/tests/unit/test_redis_client.py::TestRedisClient::test_set_key PASSED                                                                      [ 83%]
src/tests/unit/test_redis_client.py::TestRedisClient::test_remove_key PASSED                                                                   [100%]

```