import mysql.connector as mysql
#global variables
username=''
mycon=''
passwd=""

def mysqlcheck():
    global username
    global mycon
    global passwd
    username=input("\nenter mysqls username: ")
    passwd=input("\nenter mysql password : ")
    try:
      mycon=mysql.connect(host="localhost",user=username,passwd=passwd,auth_plugin='mysql_native_password')
    except mysql.Error:
      print("Something went wrong please check your password and username")
      
    if mycon:
        print("\nConnection was sucssesfull")
        cur=mycon.cursor()
        cur.execute("show databases;")
        r=cur.fetchall()
        l=("bank",)
        if l in r:
           return mycon
        else:
            cur.execute("create database bank")
            cur.execute("commit")
            cur.close()
            return mycon
#for established mysql connection

def mysqlcon():
    global username
    global mycon
    global passwd
    mycon=mysql.connect(host="localhost",user=username,passwd=passwd,database="bank",auth_plugin="mysql_native_password")
    if mycon:
        pass
    else:
        print("could not  establish connection")

#customer module
def newcustomer():
    global cid
    if mycon:

        cur=mycon.cursor()
        cur.execute("show tables;")
        r=cur.fetchall()
        l=("cus",)
        if l in r:
             print("ENTER INFORMATION CAREFULLY")
             cid=input("enter customer id: ")
             cname=input('enter customer name: ')
             address=input('enter address: ')
             phone=input('enter cust contact no.: ')
             sql="insert into cus(cid,cname,address,phone) values(%s,%s,%s,%s);"
             values=(cid,cname,address,phone)
             cur.execute(sql,values)
             cur.execute('commit')
             cur.close()
             print("customer added succesfully")
        else:
            create="create table cus(cid varchar(10) primary key,cname char(20) not null,address varchar(100) not null,phone varchar(12))"
            cur.execute(create)
            print("ENTER INFORMATION CAREFULLY")
            cid=input("enter customer id: ")
            cname=input('enter customer name: ')
            address=input('enter address: ')
            phone=input('enter cust contact no.: ')
            sql="insert into cus(cid,cname,address,phone) values(%s,%s,%s,%s);"
            values=(cid,cname,address,phone)
            cur.execute(sql,values)
            cur.execute('commit')
            cur.close()
            print("customer added succesfully")
    else:
        print("error in mysql connection")
#display cust table
def displaycust():
    if mycon:
        cur=mycon.cursor()
        cur.execute("select * from cus")
        r=cur.fetchall()
        if r:
          print("**********CUS DETAILS********")
          k=['CID','CNAME','ADDRESS','CONTACT']
          for i in k:
            print('{:<11}'.format(i),end="")
          print()
          for i in r:
            for j in i:
                k=str(j)
                print('{:<13}'.format(k),end="")
            print()
        else:
            print("no data available")
    else:
        print("error in mysql connection")
             
#serachcust
def serachcust():
    if mycon:
        cur=mycon.cursor()
        a=input('enter customer id to be found')
        sql="select * from cus where cid=%s"
        values=(a,)
        cur.execute(sql,values)
        r=cur.fetchall()
        if r:
          k=['CID','CNAME','ADDRESS','CONTACT']
          for i in k:
            print('{:<11}'.format(i),end="")
          print()
          for i in r:
             for j in i:
                k=str(j)
                print('{:<13}'.format(k),end="")
             print()
        else:
            print("customer not found")
    else:
        print("error in mysql connection")

#acoountcreate
def newaccount():
    if mycon:
        cur=mycon.cursor()
        cur.execute("show tables;")
        r=cur.fetchall()
        l=("acc",)
        if l in r:
             cid=input('enter customer id')
             sql="select * from cus where cid=%s"
             val=(cid,)
             cur.execute(sql,val)
             r=cur.fetchall()
             if r:
               accno=int(input("enter account number: "))
               acctype=input("enter account type(savings/current): ")
               amt=int(input("enter amount : "))
               pin=int(input("enter pin : "))
               sql='insert into acc(cid,accno,acc_type,amt,pin) values(%s,%s,%s,%s,%s)'
               val=(cid,accno,acctype,amt,pin)
               cur.execute(sql,val)
               cur.execute("commit")
               print("new account opened succesfully")
        else:
           sql="create table acc(cid varchar(10),accno int primary key,acc_type char(20) not null,amt int not null,pin int not null unique)"
           cur.execute(sql)
           cid=input('enter customer id')
           sql="select * from cus where cid=%s"
           val=(cid,)
           cur.execute(sql,val)
           r=cur.fetchall()
           if r:
              accno=int(input("enter account number: "))
              acctype=input("enter account type(savings/current): ")
              amt=int(input("enter amount : "))
              pin=int(input("enter pin : "))
              sql='insert into acc(cid,accno,acc_type,amt,pin) values(%s,%s,%s,%s,%s)'
              val=(cid,accno,acctype,amt,pin)
              cur.execute(sql,val)
              cur.execute("commit")
              print("new account opened succesfully")
           else:
             print("customer not found")
    else:
        print("something went wrong")
#display account table
def displayacc():
    if mycon:
        cur=mycon.cursor()
        cur.execute("select * from acc")
        r=cur.fetchall()
        if r:
          print("*******Account Details******")
          k=[ 'CID','ACCNO','ACC_TYPE','AMT','PIN']
          for i in k:
            print('{:<11}'.format(i),end="")
          print()
          for i in r:
            for j in i:
                k=str(j)
                print('{:<13}'.format(k),end="")
            print()
        else:
            print("no data available")
    else:
        print("Something went wrong")
#serach account
def serachaccount():
    global cid
    if mycon:
        cur=mycon.cursor()
        cid=input("enter custiomer id:")
        accno=int(input("enter account number:"))
        sql="select * from acc where cid=%s and accno=%s"
        values=(cid,accno)
        cur.execute(sql,values)
        r=cur.fetchall()
        if r:
            print("*******Customer deatils****")
            k=[ 'CID','ACCNO','ACC_TYPE','AMT','PIN']
            for i in k:
               print('{:<11}'.format(i),end="")
            print()
            for i in r:
               for j in i:
                     k=str(j)
                     print('{:<13}'.format(k),end="")
               print()
        else:
            print("no data available")
    else:
        print("Something went wrong")
#atm module
def withdraw():
    c=3
    if mycon:
        cur=mycon.cursor()
        accno=int(input("enter account number :"))
        sql="select * from acc where accno=%s"
        values=(accno,)
        cur.execute(sql,values)
        data=cur.fetchall()
        if data:
            while True:
                pin=int(input("enter atm pin(3 attempts) :"))
                sql='select * from acc where pin=%s and accno=%s'
                values=(pin,accno)
                cur.execute(sql,values)
                data=cur.fetchall()
                for i in data:
                    d=i[3]
                if data:
                    amt=int(input("enter amount to withdraw: "))
                    if amt>d:
                        print("insufficent balance")
                        break
                    else:
                      sql="update acc set amt=amt-%s where accno=%s and pin=%s"
                      cur.execute(sql,(amt,accno,pin,))
                      cur.execute("commit")
                      sql='select * from acc where pin=%s and accno=%s'
                      values=(pin,accno)
                      cur.execute(sql,values)
                      data=cur.fetchall()
                      for i in data:
                               d=i[3]
                      print("****Transcation completed***")
                      print("balance amount in your account is",d)
                      print("thank you for using our atm ")
                      break
                else:
                  print("Invalid pin!please enter valid pin")
                  c=c-1
                if c==0:
                    print("Card has been blocked due t0 many unsucessfull attempts")
                    print("please visit our nearest branch for help")
                    break

        else:
            print("account not found")
con=mysqlcheck()
if con:
    mysqlcon()
    y="y"
    
    while y=="y":
      print("****************MENU*****************")
      print("**1.**Add new customer            ***")
      print('**2.**display exsisting customers ***')
      print('**3.**serach a customer           ***')
      print("**4.**open a new account          ***")
      print('**5.**display exsisting accounts  ***')
      print('**6.**serach a account            ***')
      print("**7.**withdraw money              ***")
      print('*************************************')
      a=int(input("enter your choice :"))
      if a==1:
        newcustomer()
        y=input("do you want to continue: ")
      elif a==2:
        displaycust()
        y=input("do you want to continue: ")
      elif a==3:
        serachcust()
        y=input("do you want to continue: ")
      elif a==4:
        newaccount()
        y=input("do you want to continue: ")
      elif a==5:
        displayacc()
        y=input("do you want to continue: ")
      elif a==6:
        serachaccount()
        y=input("do you want to continue: ")
      elif a==7:
        withdraw()
        y=input("do you want to continue: ")
      else:
        print('INVALID INPUT!!!!')

        

    
            
   
        
    
    
