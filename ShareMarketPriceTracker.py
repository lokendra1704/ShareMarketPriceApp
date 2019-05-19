from tkinter import *
from tkinter import ttk
import tkinter.messagebox

import mysql.connector

mydb = mysql.connector.connect(user='root', password='toor',
                              host='localhost',
                              database='python')
cursor = mydb.cursor()

def open():
    global rootm
    rootm = Tk()
    rootm.geometry('200x100')
    Label(rootm,text="WELCOME").grid(row=1)
    Button(rootm,text="Signup",command=Signup).grid(row = 5,column=5,sticky = W)
    Button(rootm,text="Loginup",command=Login).grid(row = 7,column=5,sticky = W)
    rootm.mainloop()

def Signup():
    global pwordE
    global namE
    global nameE
    global roots
    #rootm.destroy()
    roots = Tk()
    roots.title('Signup')
    instruction = Label(roots,text='Please Enter new Credientials\n')
    instruction.grid(row=0, column=0,sticky=E)
    name = Label(roots, text='Enter Name:')
    nameL = Label(roots, text='New Username:')
    pwordL = Label(roots,text='New Password:')
    name.grid(row=1,column=0,sticky=W)
    nameL.grid(row=2,column=0,sticky=W)
    pwordL.grid(row=3,column=0,sticky=W)
    namE = Entry(roots)
    nameE = Entry(roots)
    pwordE = Entry(roots)
    namE.grid(row=1,column=1)
    nameE.grid(row=2,column=1)
    pwordE.grid(row=3,column=1)
    c = Checkbutton(roots,text='keep me logged in')
    c.grid(columnspan=2)
    button_1 = Button(roots,text='Signup',command=forsignup)
    button_1.grid(columnspan = 2,sticky=W)
    roots.mainloop()


def forsignup():
        tkinter.messagebox.showinfo('successfully signed up','successfully signed up')
        sql = "INSERT INTO USERS (NAME, USERNAME, PASSWORD) VALUES (%s, %s, %s)"
        val = (namE.get(), nameE.get(),pwordE.get())
        cursor.execute(sql, val)
        mydb.commit()
        Login()


def Login():
    global rootL
    global nameEL
    global pwordEL
    rootm.destroy()
    #roots.destroy()
    rootL = Tk()
    rootL.title('Login')
    instruction = Label(rootL,text='Please Enter your Credientials\n')
    instruction.grid(row=0, column=0,sticky=E)

    label_1 = Label(rootL, text=' Username:')
    label_2 = Label(rootL,text=' Password:')
    label_1.grid(row=1,column=0,sticky=W)
    label_2.grid(row=2,column=0,sticky=W)
    nameEL = Entry(rootL)
    pwordEL = Entry(rootL)
    nameEL.grid(row=1,column=1)
    pwordEL.grid(row=2,column=1)
    button_1 = Button(rootL,text='LOGIN',command=loggedin)
    button_1.grid(columnspan = 2,sticky=W)
    rootL.mainloop()

def loggedin():
        global id
        global row
        sql = "select * from users where username = %s and password = %s"
        val = (nameEL.get(), pwordEL.get())
        cursor.execute(sql, val)
        row = cursor.fetchone()
        if row is not None:
            id = row[0]
            tkinter.messagebox.showinfo('loggedin','successfully log in.....'+str(row[0]))
            USER(id)
        else:
            tkinter.messagebox.showinfo('failed','invalid password or username')
            Login()

def AddShares():
    Welcome.destroy()
    global AddSh
    AddSh = Tk()
    AddSh.geometry("200x200")
    AddSh.title("Add Shares")
    sql = "select share_id, share_name from shares where share_name <> all(select share_name from sub,shares where sub.share_id = shares.share_id and user_id = "+str(id)+" )"
    cursor.execute(sql)
    datax = cursor.fetchall()
    row_Index = 0
    ShareS = []
    for each in datax:
        ShareS.append(each[0])
    for each in ShareS:
        print(each)
    buttons = []
    i=ShareS[0]
    j=0
    for n in datax:
        button = Button(AddSh,text=n[1],command=lambda i=i: AddShClick(i))
        button.grid(row = row_Index, sticky = W)
        row_Index = row_Index + 1
        i = ShareS[j]
        j = j+1
        buttons.append(button)

def AddShClick(Share_id):
    print(Share_id)
    sql = "insert into sub values("+str(id)+","+str(Share_id)+")"
    
    cursor.execute(sql)
    mydb.commit()
    USER(id)
    AddSh.destroy()

def Logout():
    Welcome.destroy()
    id = 0
    open()
    

def USER(id):
    #rootL.destroy()
    global Welcome
    Welcome = Tk()
    Welcome.title("Share Market Price Tracker")
    Welcome.geometry("300x300")
    label_1 = Label(Welcome, text="Hello "+str(row[1]))
    label_1.grid(row=1,column=0,sticky=W)
    label2 = Label(Welcome, text="----------------------")
    label2.grid(row=2,columnspan=8,sticky=W)
    label3 = Label(Welcome, text="Your Subscribed Shares are:")
    label3.grid(row = 3,)
    sql = "Select share_name, close from sub, shares where sub.share_id = shares.share_id and user_id = "+str(id)
    cursor.execute(sql)
    data = cursor.fetchall()
    x=4
    for each in data:
        label = Label(Welcome, text=each[0])
        label.grid(row = x,column = 0)
        label2 = Label(Welcome, text=str(each[1]))
        label2.grid(row = x,column = 1)
        x = x+1
    button_1 = Button(Welcome,text='                   +                  ',command=AddShares,bg="green",fg="white")
    button_1.grid(row = x, columnspan = 2, sticky=W)
    logout = Button(Welcome,text = "LOGOUT" ,command=Logout).grid(row = x+1)
    

if __name__ == '__main__':
    global rootm
    open()    
