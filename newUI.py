import tkinter.messagebox
from tkinter import *
import ttkbootstrap


class CreateWindow:
    def __init__(self, root):
        self.root = root
        ttkbootstrap.Style()
        self.root.title("CC登录")
        self.width = 380
        self.height = 300
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d' % (
            self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2))
        self.root.resizable(width=False, height=False)

        self.uname_label = Label(self.root, text="账号：", font=32)
        self.uname_label.place(relx=0.23, rely=0.2)
        self.uname_input = Entry(self.root)
        self.uname_input.place(relx=0.43, rely=0.21)
        self.pwd_label = Label(self.root, text="密码：", font=32)
        self.pwd_label.place(relx=0.23, rely=0.3)
        self.pwd_input = Entry(self.root, show='*')
        self.pwd_input.place(relx=0.43, rely=0.31)

        self.radio_label = Label(self.root, text="请选择你的套餐：", font=32)
        self.radio_label.place(relx=0.23, rely=0.45)
        self.res_type = StringVar()
        self.radio_dx = Radiobutton(self.root, text="电信", font=32, variable=self.res_type, value="电信")
        self.radio_dx.place(relx=0.23, rely=0.55, )
        self.radio_yd = Radiobutton(self.root, text='移动', font=32, variable=self.res_type, value="移动")
        self.radio_yd.place(relx=0.53, rely=0.55)
        self.res_type.set("电信")

        self.ok = Button(self.root, text="确认", command=self.write_file)
        self.ok.place(relx=0.23, rely=0.75, relwidth=0.2, relheight=0.1)
        self.cancel = Button(self.root, text="取消", command=self.quit_exe)
        self.cancel.place(relx=0.63, rely=0.75, relwidth=0.2, relheight=0.1)
        self.root.mainloop()

    def quit_exe(self):
        self.root.destroy()

    def write_file(self):
        if self.uname_input.get() == '' or self.pwd_input.get() == '':
            tkinter.messagebox.showinfo('提示', '账号和密码不能为空')
            return
        with open('user.txt', 'w', encoding='utf-8') as f:
            f.write(f"username {self.uname_input.get()}\n")
            f.write(f"password {self.pwd_input.get()}\n")
            f.write(f"package {self.res_type.get()}\n")
        self.quit_exe()
