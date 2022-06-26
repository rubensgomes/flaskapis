'''This module implements the Tower of Hanoi python code
Created on Feb 11, 2022

@author: Rubens Gomes
'''


def toh(n, fromStack, toStack, spareStack):
    """
    Inputs: n, positive integer containing number of disks
            fromStack, array containing disks to be moved from
            toStack, array to where disks should be moved to
            spareStack, array to keep temporary spare disks during moves
    Returns None
    """
    # recursive base case
    if n == 1:
        toStack.append(fromStack.pop())
        print ("fromStack: ", fromStack)
        print ("toStack: ", toStack)
        print ("spareStack: ", spareStack)
        print("-------")
        return None

    # notice these are recursive calls
    toh(n - 1, fromStack, spareStack, toStack)
    toh(1, fromStack, toStack, spareStack)
    toh(n - 1, spareStack, toStack, fromStack)

    return None


if __name__ == '__main__':
    print('toh starting...')
    _fromStack = ["0", "1", "2", "3"]
    _toStack = []
    _spareStack = []

    print ("initial fromStack: ", _fromStack)
    print ("initial toStack: ", _toStack)
    print ("initial spareStack: ", _spareStack)
    print("-------")

    toh(len(_fromStack), _fromStack, _toStack, _spareStack)

    print ("final fromStack: ", _fromStack)
    print ("final toStack: ", _toStack)
    print ("final spareStack: ", _spareStack)
