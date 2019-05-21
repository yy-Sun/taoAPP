if __name__ == '__main__':
    key = 'yyy'
    value = '123456'
    mymap = {}
    mymap[key] = value
    key2 = 'yyy'
    value2 = 'yyy'
    if key2 not in mymap:
        mymap[key2] = value2
    print(mymap)
