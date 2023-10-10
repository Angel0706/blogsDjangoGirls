import xlsxwriter

son = {'name':'aaa'}
dic = {'name':'Sol','age':43,'son':son}
print(dic)

def esPar(num):
    if (num % 2) == 0:
        print('Par')
    else:
        print("Impar")

def recorrer(lis, num):
    for i in lis[num]:
        print(i)

def get_excel():
    workbook = xlsxwriter.Workbook('demo.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    bold = workbook.add_format({'bold':True})
    worksheet.write('A1', 'A')
    worksheet(A2,'AA')
    worksheet.write(2,0,123)
    worksheet.write(3,0,321)
    workbook.close()

get_excel()

"""
esPar(7)
li = [[1,2,3],[4,5,6],[7,8,9]]
recorrer(li,0)
"""