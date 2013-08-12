from inspect import isfunction
from callbacks import Callbacks

class Deferred:

	def __init__ (self, beforeStart=None):
		self._resolvedCallbacks = Callbacks(once=True, memory=True)
		self._rejectedCallbacks = Callbacks(once=True, memory=True)
		self._progressCallbacks = Callbacks(memory=True)
		self._states = ['pending','rejected','resolved']
		self._state = self._states[0]
		if beforeStart is not None:
			beforeStart(self)

	def reject (self, *args, **kwargs):
		if self.pending():
			self._rejectedCallbacks.fire(*args, **kwargs)
		return self

	def resolve (self, *args, **kwargs):
		if self.pending():
			self._resolvedCallbacks.fire(*args, **kwargs)
		return self

	def notify (self, *args, **kwargs):
		if self.pending():
			self._progressCallbacks.fire(*args, **kwargs)
		return self

	def _addListener (self, callbacks, fn, *args):
		for arg in args:
			if isfunction(arg):
				callbacks.add(arg)
			elif isinstance(arg, Deferred):
				callbacks.add(lambda *args, **kwargs:getattr(arg, fn)(*args,**kwargs))
		return self

	def progress (self, *args):
		return self._addListener(self._progressCallbacks, 'notify', *args)

	def done (self, *args):
		return self._addListener(self._resolvedCallbacks, 'resolve', *args)

	def fail (self, *args):
		return self._addListener(self._rejectedCallbacks, 'reject', *args)

	def always (self, *args):
		return self.done(*args).fail(*args)

	def pending (self):
		return self._state is self._states[0]

	def rejected (self):
		return self._state is self._states[1]

	def resolved (self):
		return self._state is self._states[2]