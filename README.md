Deferred
========

Python Callbacks &amp; Deferreds
--------------------------------

Python implementation of the jQuery Callbacks et Deferred objects

Callbacks
---------
```python
from callbacks import Callbacks

def fn1(v):
  print('fn1 says: %s' % v)
def fn2(v):
  print('fn2 says: %s' % v)

c = Callbacks(memory=True)
c.add(fn1).fire('hello')
c.add(fn2)
c.fire('hi')
```
```
fn1 says: hello
fn2 says: hello
fn1 says: hi
fn2 says: hi
```

Deferred
--------
```python
from threading import Thread
from sys import exc_info
from urllib import request
from deferred import Deferred

deferred = Deferred()

def sendRequest (readFn, deferred):
  try:
		res = readFn()
		deferred.resolve(res)
	except:
		deferrred.reject(exc_info()[1])

try:
	req = request.Request(url='http://thiswebsitedoesnotexistatall.org/')
	kwargs = {'readFn':request.urlopen(req).read,'deferred':deferred}
	Thread(target=sendRequest,kwargs=kwargs).start()
except:
	deferred.reject(exc_info()[1])

deferred.done(lambda res:print('Success !\n%s' % res)).fail(lambda e:print('Fail ! %s' % e))
```
```
Fail ! <urlopen error [Errno 11001] getaddrinfo failed>
```
