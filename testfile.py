POS = 65
gameString= ''
if gameString == '':
        Fpos = POS
#POS = int(9-POS%10 + 90-(POS-POS%10))
POS = int((int(9-POS%10 + 90-(POS-POS%10))%10)*10 + (int(9-POS%10 + 90-(POS-POS%10))-int(9-POS%10 + 90-(POS-POS%10))%10)/10)
print(POS)
print(Fpos)
#65