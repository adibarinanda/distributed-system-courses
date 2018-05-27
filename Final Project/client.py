import Pyro4

def main():
	with Pyro4.core.Proxy("PYRO:dispatcher@192.168.56.101:") as d:
		return "a"

if __name__ == '__main__':
	main()