import Pyro4

def main():
	with Pyro4.core.Proxy("PYRO:dispatcher@192.168.56.101:39501") as d:
		# print("Test")
		d.init()

if __name__ == '__main__':
	main()