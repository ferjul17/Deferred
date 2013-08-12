import sys, unittest
sys.path.append('../src')
from callbacks import Callbacks


class TestCallbacks(unittest.TestCase):

	def test_withoutFlags(self):
		val = 0
		nb = 0

		def fn1(v):
			nonlocal val, nb
			val = v
			nb += 1

		def fn2(v):
			nonlocal val, nb
			val = -v
			nb += 1

		def check1(v):
			nonlocal self, val, nb
			self.assertIs(v,val)
			nb += 1

		def check2(v):
			nonlocal self, val, nb
			self.assertIs(-v,val)
			nb += 1

		c = Callbacks()
		c.add(fn1).add(check1)
		c.fire(1)
		c.add(fn2).add(check2)
		c.fire(2)
		c.remove(fn2).remove(check2).add(check1)
		c.fire(3)

		self.assertEqual(nb,9)

if __name__ == '__main__':
    unittest.main(verbosity=2)
