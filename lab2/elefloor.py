import time

print('幸福大廈共有1~7層樓')
print('進電梯')
nowFloor = 1

while True:

    target = int(input('您現在在 {} 樓。請問要去哪一樓(輸入 0 可離開電梯)？\n>> '
                       .format(nowFloor)))
    try:
        target = int(target)
    except ValueError:
        print('ERROR\n')
        continue

    if target == 0 :
        break

    if target == nowFloor:
        continue

    if target > 7 or target < 1:
        print('請輸入介於 1-7 的整數')
        continue

    if target > nowFloor:
        print('電梯上樓')
        for i in range(nowFloor, target+1):
            print('{}'.format(i))
            time.sleep(1)
        nowFloor = target
    else :
        print('電梯下樓')
        for i in range(nowFloor,target-1,-1):
            print('{}'.format(i))
            time.sleep(1)
        nowFloor = target

print('出電梯')


