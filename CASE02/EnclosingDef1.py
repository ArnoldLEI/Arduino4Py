

def mssage(text):
    text = text + " By Gjun"
    def print_message():
        print(text)

    return print_message


if __name__ == '__main__':
    m1 = mssage("Hello")
    m1()