'''This module implements the Tower of Hanoi python code
Created on Feb 11, 2022

@author: Rubens Gomes
'''


def toh(n, fromStack, toStack, spareStack):

    if n == 1:
        toStack.append(fromStack.pop())
        print ("frontStack: ", fromStack)
        print ("toStack: ", toStack)
        print ("spareStack: ", spareStack)
        print("-------")
        return

    toh(n - 1, fromStack, spareStack, toStack)
    toh(1, fromStack, toStack, spareStack)
    toh(n - 1, spareStack, toStack, fromStack)

    return


if __name__ == '__main__':
    print('toh starting...')
    fromStack = ["0", "1", "2", "3"]
    toStack = []
    spareStack = []

    print ("initial frontStack: ", fromStack)
    print ("initial toStack: ", toStack)
    print ("initial spareStack: ", spareStack)
    print("-------")

    toh(len(fromStack), fromStack, toStack, spareStack)

    print ("final frontStack: ", fromStack)
    print ("final toStack: ", toStack)
    print ("final spareStack: ", spareStack)
