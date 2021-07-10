
def login(password):
    def dectorated(func):
        def check():
            if (password == 1234):
                print("Login Success")
                func()
            else:
                print("Login Fail")
                None
        return check
    return dectorated

@login(password=1234)
def report():
    print("Secrt: Free 6.29")


report()