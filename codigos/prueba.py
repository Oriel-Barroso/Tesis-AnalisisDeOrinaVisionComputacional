lista = ['1','2','3']
dic = {'a1':1, 'a': 2, 'b2': 3, 'ggg5': 4}
dic2 = {}
for k,v in dic.items():
    print(k[-1])
    if k[-1] in lista:
        dic2[k] = v

print(dic2)