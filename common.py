def arrAdd(a, b) -> list:
    res = []
    for i in range(0,len(a)):
        res.append(a[i] + b[i])
    return res

def posAdd(a,b) -> list:
    res = []
    for i in b:
        res.append(arrAdd(a,i))
    return res

def linePrint(str):
    print('\033[1A', end='\x1b[2K')
    print(str)

def clamp(num,floor,roof):
    return max(floor, min(num,roof))

if __name__ == '__main__':
    print(arrAdd([2,2,3],[3,2,6]))
    print(posAdd((4,5),[[0,1],[-1,0]]))
    print(clamp(10,0,20))
    print(clamp(100,0,20))
    print(clamp(-10,0,20))