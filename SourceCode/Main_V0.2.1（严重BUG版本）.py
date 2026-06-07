import random as rand
import tkinter as tk
import tkinter.font as tkf
import tkinter.ttk as ttk
import ctypes as c
import traceback as tb
import os,sys,json,time
os.chdir(os.path.dirname(sys.argv[0]))
main=tk.Tk()
main.minsize(500,500)
main.title("随机抽选-简易版")
main.config(bg="#90f4b3")
main.attributes("-alpha",0.8)
name_font=tkf.Font(family="楷体",size=75,weight="bold")
start_button_font=tkf.Font(family="楷体",size=40)
name=tk.Label(main,text="",font=name_font,wraplength=490,bg="#90f4b3")
name.pack(pady=100)
name_database=[]
a=0
def name_rand(name_rand_times=0):
    if name_rand_times<=15:
        name.config(text=name_database[rand.randint(0,len(name_database)-1)])
        start.config(state="disable")
    else:
        if name_rand_times==16:
            start.config(state="normal")
    main.after(100,name_rand,name_rand_times+1)
start=tk.Button(main,text="随机抽选",relief="groove",command=name_rand,font=start_button_font,bg="#50E885",activebackground="#79DBB2")
start.pack(pady=40,side="bottom")
menu=tk.Frame(main,bg="#50E885")
def shown_menu(event):
    menu.place(x=0,y=0,height=35,width=main.winfo_width())
main.bind("<Visibility>",shown_menu)
resize_tool=ttk.Sizegrip(main)
style=ttk.Style().configure("TSizegrip",background="#90f4b3")
hide_title_state=False
def menu_size(event):
    menu.place(width=main.winfo_width())
    name.config(wraplength=main.winfo_width()-10)
    name_font.configure(size=75+(min(main.winfo_width()-500,main.winfo_height()-500)/5))
    start_button_font.config(size=40+int(min(main.winfo_width()-500,main.winfo_height()-500)/10))
    resize_tool.place(x=main.winfo_width(),y=main.winfo_height(),anchor="se")
    if hide_title_state==True:
        min_window.place(x=main.winfo_width()-70)
        max_window.place(x=main.winfo_width()-50)
        exit_button.place(x=main.winfo_width()-30)
main.bind("<Configure>",menu_size)
fullscr=tk.Label(menu,text="全屏",bg="#50E885",anchor="w")
fullscr.pack(side="right",padx=12)
fullscreen_state=tk.IntVar()
fullscreen_state.set(0)
exit_button=tk.Label(menu,text="×",bg="#50E885",font=20)
max_window=tk.Label(menu,text="▢",bg="#50E885",font=20)
min_window=tk.Label(menu,text="-",bg="#50E885",font=30)
def fullscr_button(event):
    if fullscreen_state.get()==0:
        if hide_title_state==True:
            main.overrideredirect(boolean=False)
        main.attributes("-fullscreen",True)
        fullscr.config(text="退出全屏")
        fullscr.pack(padx=80)
        max_window.place(x=main.winfo_width()-50,y=16,anchor="w")
        exit_button.place(x=main.winfo_width()-30,y=18,anchor="w")
        min_window.place(x=main.winfo_width()-70,y=17,anchor="w")
        fullscreen_state.set(1)
    else:
        main.attributes("-fullscreen",False)
        fullscr.config(text="全屏")
        if hide_title_state==0:
            fullscr.pack(padx=10)
            min_window.place_forget()
            max_window.place_forget()
            exit_button.place_forget()
        fullscreen_state.set(0)
        if hide_title_state==True:
            main.overrideredirect(boolean=True)
fullscr.bind("<Button-1>",fullscr_button)
def esc_exit(event):
    if fullscreen_state.get()==1:
        main.attributes("-fullscreen",False)
        fullscr.config(text="全屏")
        fullscreen_state.set(0)
        if hide_title_state==True:
            main.overrideredirect(boolean=True)
main.bind("<Key-Escape>",esc_exit)
def exit_p(event):
    main.destroy()
    sys.exit()
become_max=0
def max_window_1(event):
    global become_max
    if become_max==0:
        main.state("zoomed")
        become_max=1
    else:
        main.state("normal")
        become_max=0
def min_window_1(event):
    global hide_title_state
    if hide_title_state==True:
        main.overrideredirect(boolean=False)
        hide_title_state=False
        min_window.place_forget()
        max_window.place_forget()
        exit_button.place_forget()
        fullscr.pack(padx=10)
    main.iconify()
exit_button.bind("<Button-1>",exit_p)
max_window.bind("<Button-1>",max_window_1)
min_window.bind("<Button-1>",min_window_1)
settings=tk.Menubutton(menu,text="选项",bg="#50E885",anchor="e",activebackground="#50d385")
settings.pack(padx=10,side="left")
set_menu=tk.Menu(settings,tearoff=False,bg="#50E885",activebackground="#73d3A0",activeforeground="#102305")
settings.config(menu=set_menu)
def hide_title():
    global hide_title_state
    if hide_title_state==0:
        main.overrideredirect(boolean=True)
        fullscr.pack(padx=80)
        max_window.place(x=main.winfo_width()-50,y=16,anchor="w")
        exit_button.place(x=main.winfo_width()-30,y=18,anchor="w")
        min_window.place(x=main.winfo_width()-70,y=17,anchor="w")
        hide_title_state=True
    else:
        main.overrideredirect(boolean=False)
        if fullscreen_state.get()==0:
            min_window.place_forget()
            max_window.place_forget()
            exit_button.place_forget()
            fullscr.pack(padx=10)
            hide_title_state=False
    if hide_title_state==True:
        menu.bind("<Button-1>",replace_xy)
set_menu.add_command(label="显示/隐藏标题栏",command=hide_title)
def replace_xy(event):
    def replace_xy1(event):
        if hide_title_state==True:
            window_x=str(main.winfo_x()+(event.x-primary_x))
            window_y=str(main.winfo_y()+(event.y-primary_y))
            main.geometry(f"+{window_x}+{window_y}")
    menu.bind("<B1-Motion>",replace_xy1)
    primary_x=event.x
    primary_y=event.y
def json_config():
    global name_database
    try:
        if os.path.isfile("./namelist.json")==True:
            with open("./namelist.json","r",encoding="utf-8-sig") as namelist:
                names=json.load(namelist)
                name_database=names
            if name_database==[]:
                c.windll.user32.MessageBoxW(main.winfo_id(),"json配置为空，请在当前目录下的\"namelist.json\"中写入一个列表。","随机抽取-json配置为空",0x10)
                start.config(state="disable")
        else:
            if os.path.isdir("./namelist.json")==True:
                c.windll.user32.MessageBoxW(main.winfo_id(),"json配置为目录，请在当前目录下的\"namelist.json\"文件夹删除，然后再创建此文件","随机抽取-找不到json配置",0x10)
                start.config(state="disable")
            else:
                c.windll.user32.MessageBoxW(main.winfo_id(),"未找到json配置，请在当前目录下新建\"namelist.json\"文件","随机抽取-找不到json配置",0x10)
                start.config(state="disable")
    except json.decoder.JSONDecodeError as json_error:
        c.windll.user32.MessageBoxW(main.winfo_id(),"json语法不正确，原因：\n"+str(json_error),"随机抽取-json配置错误",0x10)
        start.config(state="disable")
    except FileNotFoundError as json_error:
        c.windll.user32.MessageBoxW(main.winfo_id(),"找不到json文件，原因：\n"+str(json_error),"随机抽取-找不到json配置",0x10)
        start.config(state="disable")
    except PermissionError as json_error:
        c.windll.user32.MessageBoxW(main.winfo_id(),"json文件被拒绝读取，原因：\n"+str(json_error),"随机抽取-json配置读取失败",0x10)
        start.config(state="disable")
    except Exception as json_error:
        c.windll.user32.MessageBoxW(main.winfo_id(),"未知错误：\n"+str(tb.format_exc()),"随机抽取-错误",0x10)
        start.config(state="disable")
main.after(300,json_config)
main.mainloop()
