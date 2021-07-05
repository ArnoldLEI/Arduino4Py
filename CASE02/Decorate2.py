#裝飾器 1

def make_dress(func):
    def dress():
        print("Wear cloth")
        func()
    return dress()


def out():
    print("Go Out")

if __name__ == '__main__':
    john = make_dress(out)
    john