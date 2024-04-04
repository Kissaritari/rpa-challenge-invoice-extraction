import cv2, re, pandas
import pytesseract


data = [ {'ID' : '8ravyyin4m94x5czswwiw4', 'InvoiceNo':'284212'}, {'ID':'48flfotndlhuq6nims619','InvoiceNo':'284213'}, {'ID':'48flfotndlhuq6nims619','InvoiceNo':'284228'}]
data2 = [ {'ID' : '1ravyyin43g5h5czswwiw4', 'InvoiceNo':'182412'}, {'ID':'28flfotdnfgnfdq6nims619','InvoiceNo':'265413'}, {'ID':'38flfotn2j5rtgs619','InvoiceNo':'384228'},{'piski':'koira'}]
df =pandas.DataFrame(data)
df2 = pandas.DataFrame(data2)
df3 = pandas.concat([df,df2],axis=0)
print(df3)