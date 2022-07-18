from tkinter import *
import Face_recognition as fr
import os

def btnevent():
    name = e.get()
    id = ep.get()
    e.delete(0, END)
    ep.delete(0, END)
    fileList = os.listdir("./faces")
    fileList.remove('all_face.xml')
    filename = fileList[0]
    fileList = filename.split("_")
    if name == fileList[0] and id == fileList[1]:
        n = fr.start_Face_Recognition()
        if n == 1:
            after_login()



def login():
    root.title("로그인")

    txt.grid(row=1, column=0, padx=5, pady=10)

    e.grid(row=1, column=1, padx=5, pady=10)

    btn.configure(command=lambda: btnevent())
    btn.grid(row=1, column=2, padx=5, pady=10, rowspan=2)

    ###########################################

    txtp.grid(row=2, column=0, padx=5, pady=10)

    ep.grid(row=2, column=1, padx=5, pady=10)

    ##########################################
    txt2.configure(text="로그인")
    txt2.grid(row=0, column=1)

    make_id_button.grid_forget()


def after_login():
    txt.grid_forget()
    txt2.grid_forget()
    e.grid_forget()
    btn.grid_forget()
    txtp.grid_forget()
    ep.grid_forget()
    make_id_button.grid_forget()

    aTxt = Label(root, text="로그인 되었습니다.")
    aTxt.grid(row=1, column=1, padx=140, pady=20)
    root.title("로그인 성공")

def make_face():
    name = e.get()
    id = ep.get()
    e.delete(0, END)
    ep.delete(0, END)
    fr.taPic(name, id)
    fr.trainModel()


    txt.grid_forget()
    e.grid_forget()
    btn.grid_forget()
    txtp.grid_forget()
    ep.grid_forget()
    txt2.configure(text="회원가입 성공")
    txt2.grid(row=0, column=2, padx=90, pady=20)
    make_id_button.configure(text="로그인 화면으로 돌아가기")
    make_id_button.configure(command=login)
    make_id_button.configure(width=30)
    make_id_button.grid(row=3, column=2, padx=90, pady=20)



def make_id():
    make_id_button.grid_forget()
    txt2.configure(text="회원가입")
    btn.configure(command=make_face)
    root.title("회원가입")






root = Tk()
root.resizable(False,False)
root.geometry("400x200+500+300")

root.title("로그인")

txt = Label(root, width=10, borderwidth = 1,text="이름")
txt.grid(row=1, column=0, padx=5, pady=10)

e = Entry(root, width=30)
e.grid(row=1, column=1, padx=5, pady=10)

btn = Button(root, width=10, height=5,text="제출", command=btnevent)
btn.grid(row=1, column=2, padx=5, pady=10, rowspan=2)

###########################################

txtp = Label(root, width=10, borderwidth = 1,text="생년월일")
txtp.grid(row=2, column=0, padx=5, pady=10)

ep = Entry(root, width=30)
ep.grid(row=2, column=1, padx=5, pady=10)

##########################################

txt2 = Label(root, text="로그인")
txt2.grid(row=0, column=1)

make_id_button = Button(root, width=10,text="회원가입", command=make_id)
make_id_button.grid(row=3, column=1)

root.mainloop()