def announce(f):
    def wrapper():
        print("about to run function...")
        f()
        print("done with function")
    return wrapper

@announce
def hello():
    print("Hello, World")

hello()