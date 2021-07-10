#裝飾器 1

def make_dress(func):
    def dress():
        print("Wear cloth")
        func()
    return dress

def make_shoes(func):
    def dress():
        print("Wear shoes")
        func()
    return dress

@make_dress
@make_shoes
def out():
    print("Go Out")

if __name__ == '__main__':
    john = out
    john()