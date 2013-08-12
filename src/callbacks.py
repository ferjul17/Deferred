class Callbacks:	

	def __init__ (self, unique=False, once=False, memory=False, stopOnFalse=False):
		self._unique = unique
		self._once = once
		self._memory = memory
		self._stopOnFalse = stopOnFalse
		self._list = []
		self._fired = False
		self._disabled = False
		self._locked = False
		self._lastArgs = None
		self._lastKwargs = None

	def disable (self):
		self._disabled = True

	def lock (self):
		self._locked = True

	def add (self, fn):
		if not self._disabled:
			if not self._unique or fn not in self._list:
				self._list.append(fn)
				if self._memory and self._fired:
					fn(*(self._lastArgs),**(self._lastKwargs))
		return self

	def fire (self, *args, **kwargs):
		if not self._disabled and not self._locked:
			self._lastArgs = args
			self._lastKwargs = kwargs
			if not self._once or not self._fired:
				for key, fn in enumerate(self._list):
					res = fn(*(self._lastArgs),**(self._lastKwargs))
					if self._stopOnFalse and res is False:
						break
				self._fired = True
		return self

	def remove (self, fn):
		if not self._disabled:
			if fn in self._list:
				self._list.remove(fn)
		return self

	def empty (self):
		if not self._disabled:
			self._list.clear()
		return self

	def fired (self):
		return not not self._fired

	def has (self, fn):
		return fn in self._list

	def disabled (self, fn):
		return not not self._disabled

	def locked (self, fn):
		return not not self._locked