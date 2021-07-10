def multi(n):
    if n == 0:
        return None

    def multi(x):
        return n*x

    return multi

if __name__ == '__main__':
    n3 = multi(3)
    n5 = multi(5)
    x=6
    print(n3(6))
    print(n3(n5(x)))