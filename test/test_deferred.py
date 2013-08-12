import sys, unittest
sys.path.append('../src')
from deferred import Deferred


class TestDeferred(unittest.TestCase):

	def test_resolve(self):
		val = 0
		def done(v):
			nonlocal self, val
			val += 1
			self.assertTrue(v)
		def fail():
			nonlocal self
			val += 1
			self.assertTrue(False)
		Deferred().done(done).fail(fail).resolve(True)
		self.assertEqual(val,1)
		Deferred().resolve(True).done(done).fail(fail)
		self.assertEqual(val,2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
