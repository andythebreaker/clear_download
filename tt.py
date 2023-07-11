class MyContextManager:
    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting the context")

    def __init__(self):
        print("Initializing the object")
    
    def wt(self):
        print("wht")

with MyContextManager() as obj:
    obj.wt()
    print("Inside the context")

# Output:
# Initializing the object
# Entering the context
# Inside the context
# Exiting the context
