# 对 FastAPI 同步写法进行压测

[压力测试样例代码](/test/stress_test_fastapi_async_sync.py)

压力测试结果：

```console
wuwenxiangs-MacBook-Pro:test wuwenxiang$ ab -n 100 -c 100 http://localhost:8000/a
Document Path:          /a
Document Length:        85 bytes
Time taken for tests:   100.468 seconds
Requests per second:    1.00 [#/sec] (mean)
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3   0.6      3       5
Processing:  1010 68796 32755.3  99455   99456
Waiting:     1005 49741 29127.1  50231   99453
Total:       1011 68799 32755.0  99458   99458

wuwenxiangs-MacBook-Pro:test wuwenxiang$ ab -n 100 -c 100 http://localhost:8000/b
Document Path:          /b
Document Length:        43 bytes
Time taken for tests:   8.053 seconds
Time per request:       80.534 [ms] (mean, across all concurrent requests)
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3   1.2      3       5
Processing:  1011 3611 1812.5   4032    7042
Waiting:     1005 3610 1812.5   4029    7041
Total:       1011 3614 1811.3   4035    7043

wuwenxiangs-MacBook-Pro:test wuwenxiang$ ab -n 100 -c 100 http://localhost:8000/c
Document Path:          /c
Document Length:        55 bytes
Time taken for tests:   2.056 seconds
Time per request:       20.556 [ms] (mean, across all concurrent requests)
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3   1.4      3       6
Processing:  1009 1034  11.4   1030    1046
Waiting:     1003 1027  10.8   1027    1044
Total:       1010 1037  10.2   1034    1047

wuwenxiangs-MacBook-Pro:test wuwenxiang$ ab -n 100 -c 100 http://localhost:8000/d
Document Path:          /d
Document Length:        84 bytes
Time taken for tests:   4.082 seconds
Time per request:       40.817 [ms] (mean, across all concurrent requests)
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    3   1.1      3       5
Processing:  1015 1831 753.0   2054    3067
Waiting:     1010 1828 753.4   2048    3067
Total:       1015 1833 752.5   2055    3070
```

可以看到 c 最好，d 还行，放大到 2000 次，200 并发，大约 5 倍差距。

```console
wuwenxiangs-MacBook-Pro:test wuwenxiang$ ab -n 2000 -c 200 http://localhost:8000/d
Concurrency Level:      200
Time taken for tests:   51.398 seconds
Complete requests:      2000
Failed requests:        0
Time per request:       5139.765 [ms] (mean)
Time per request:       25.699 [ms] (mean, across all concurrent requests)
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.7      0       9
Processing:  1003 4832 12321.6   1017   50382
Waiting:     1003 4831 12321.7   1016   50382
Total:       1003 4833 12322.7   1017   50389
Percentage of the requests served within a certain time (ms)
  50%   1017
  66%   1913
  75%   1977
  80%   2004
  90%   2075
  95%  48354
  98%  49381
  99%  50364
 100%  50389 (longest request)

wuwenxiangs-MacBook-Pro:test wuwenxiang$ ab -n 2000 -c 200 http://localhost:8000/c
Concurrency Level:      200
Time taken for tests:   11.584 seconds
Complete requests:      2000
Failed requests:        0
Time per request:       1158.397 [ms] (mean)
Time per request:       5.792 [ms] (mean, across all concurrent requests)
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.6      1       9
Processing:  1002 1042  30.2   1037    1105
Waiting:     1001 1037  26.7   1033    1098
Total:       1002 1043  30.9   1040    1106
Percentage of the requests served within a certain time (ms)
  50%   1040
  66%   1054
  75%   1071
  80%   1078
  90%   1091
  95%   1096
  98%   1097
  99%   1097
 100%   1106 (longest request)
```
