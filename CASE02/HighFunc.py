

def add(x):
    return x+1
def sub(x):
    return x-1
def oper(func, x):
    if(x>0):
        return func(x)
    else:
        return x

if __name__ == '__main__':
    x = 1
    x = add(x)
    print(x)
    x = sub(x)
    print(x)
    # ----------------------
    y = 3
    y = oper(sub, y)
    print(y)