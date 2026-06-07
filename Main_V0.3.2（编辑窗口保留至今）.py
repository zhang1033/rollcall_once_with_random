#导入
import threading
import random as rand
import tkinter as tk
import tkinter.font as tkf
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import ctypes as c
import traceback as tb
import os,sys,json
#改变工作路径为当前程序运行目录（工作目录，顾名思义就是“.”，类似于cmd的%cd%）
os.chdir(os.path.dirname(sys.argv[0]))
#创建主窗口
main=tk.Tk()
main.minsize(500,500)#设置最小大小为500x500
main.title("随机抽选-简易版")#标题
main.config(bg="#90f4b3")#设置背景颜色
main.attributes("-alpha",0.8)#设置窗口透明度
name_font=tkf.Font(family="楷体",size=75,weight="bold")#设置姓名显示字体
start_button_font=tkf.Font(family="楷体",size=40)#设置开始按钮显示字体
name=tk.Label(main,text="",font=name_font,wraplength=490,bg="#90f4b3")#设置姓名显示标签，font为在上面的字体样式
name.pack(pady=100)#排放姓名显示标签
name_database=[]#定义一个空姓名数据集
#定义一个布尔值数据，为后面调整显示或隐藏标题栏作铺垫
hide_title_state=tk.BooleanVar()
hide_title_state.set(False)#默认为不隐藏
#随机抽取部分
def name_rand(name_rand_times=0):
    if name_rand_times<=25:#设置抽取频率
        name.config(text=name_database[rand.randint(0,len(name_database)-1)])#用random模块来实现在名单范围内随机（len(name_database)-1是为了防止到最大值时溢出）
        start.config(state="disable")#抽取期间按钮禁用
    else:
        #抽取完成
        if name_rand_times==26:
            start.config(state="normal")#按钮变得可点击
    main.after(60,name_rand,name_rand_times+1)#防止tkintr线程阻塞，界面卡死，隔100ms再进行随机数
start=tk.Button(main,text="随机抽选",relief="groove",command=name_rand,font=start_button_font,bg="#50E885",activebackground="#79DBB2")
start.pack(pady=40,side="bottom",anchor="s")
#创建菜单和标题栏
menu=tk.Frame(main,bg="#50E885")
#随窗口大小变化而变长的菜单栏
def shown_menu(event):#事件的def定义的括号内必须含有event，否则会报错
    menu.place(x=0,y=0,height=35,width=main.winfo_width())
main.bind("<Visibility>",shown_menu)#检测窗口出现（防止菜单栏初始化错误）。这就是事件监听。
#调整窗口大小的控件
resize_tool=ttk.Sizegrip(main)
style=ttk.Style().configure("TSizegrip",background="#90f4b3")#改变控件主底色
def menu_size(event):
    menu.place(width=main.winfo_width())
    name.config(wraplength=main.winfo_width()-10)
    name_font.configure(size=75+int(min(main.winfo_width()-500,main.winfo_height()-500)/5))
    start_button_font.config(size=40+int(min(main.winfo_width()-500,main.winfo_height()-500)/10))
    resize_tool.place(x=main.winfo_width(),y=main.winfo_height(),anchor="se")
    if hide_title_state.get()==True:#判断是否隐藏标题栏
        #隐藏标题栏后的控件设置
        min_window.place(x=main.winfo_width()-70)#最小化
        max_window.place(x=main.winfo_width()-50)#最大化
        exit_button.place(x=main.winfo_width()-30)#退出
main.bind("<Configure>",menu_size)#绑定窗口变化事件
#全屏按钮
fullscr=tk.Label(menu,text="全屏",bg="#50E885",anchor="w")
fullscr.pack(side="right",padx=12)
#设置一个整数值表示全屏状态
fullscreen_state=tk.IntVar()
fullscreen_state.set(0)#默认为不全屏
#全屏后的控件设置
exit_button=tk.Label(menu,text="×",bg="#50E885",font=20)
max_window=tk.Label(menu,text="▢",bg="#50E885",font=20)
min_window=tk.Label(menu,text="-",bg="#50E885",font=30)

###关于全屏的
def fullscr_button(event):
    if fullscreen_state.get()==0:#检测是否没有全屏
        if hide_title_state.get()==True:#检测是否隐藏标题栏
            main.overrideredirect(boolean=False)#这里取消隐藏标题栏是为了防止在全屏时报错或异常
        main.attributes("-fullscreen",True)#全屏
        fullscr.config(text="退出全屏")#改变内容
        fullscr.pack(padx=80)#改变取消全屏的位置（向左）
        max_window.place(x=main.winfo_width()-50,y=16,anchor="w")
        exit_button.place(x=main.winfo_width()-30,y=18,anchor="w")
        min_window.place(x=main.winfo_width()-70,y=17,anchor="w")
        fullscreen_state.set(1)#设置全屏状态数值
    else:
        main.attributes("-fullscreen",False)#取消全屏
        fullscr.config(text="全屏")
        #恢复正常菜单栏
        if hide_title_state.get()==False:
            fullscr.pack(padx=10)#全屏按钮恢复到初始位置
            #隐藏控件
            min_window.place_forget()
            max_window.place_forget()
            exit_button.place_forget()
        fullscreen_state.set(0)
        #还原隐藏标题栏状态
        if hide_title_state.get()==True:
            main.overrideredirect(boolean=True)
fullscr.bind("<Button-1>",fullscr_button)#监听鼠标左键点击“全屏”或“取消全屏”
#按esc键退出全屏
def esc_exit(event):
    if fullscreen_state.get()==1:
        main.attributes("-fullscreen",False)
        fullscr.config(text="全屏")
        fullscr.pack(padx=10)
        fullscreen_state.set(0)
        if hide_title_state.get()==True:
            main.overrideredirect(boolean=True)
main.bind("<Key-Escape>",esc_exit)#监听esc键
#隐藏标题栏的退出按钮命令
def exit_p(event):
    main.destroy()
    sys.exit()
#最大化命令（目的如上同）
#这儿有一点小BUG
become_max=0#设置未最大化的数值（关键在这）
def max_window_1(event):
    global become_max#声明全局变量
    if become_max==0:#判断是否没有最大化
        main.state("zoomed")#最大化
        become_max=1#最大化数值
    else:
        main.state("normal")#窗口变为最大化前的大小
        become_max=0
#最小化命令
#由于我的技术原因，最小化之后变成显示标题栏，这也许是反人类的BUG了
def min_window_1(event):
    global hide_title_state
    if hide_title_state.get()==True:#检测标题栏是否隐藏
        #取消隐藏标题栏
        main.overrideredirect(boolean=False)
        hide_title_state.set(False)
        min_window.place_forget()
        max_window.place_forget()
        exit_button.place_forget()
        fullscr.pack(padx=10)
    main.iconify()#最小化
exit_button.bind("<Button-1>",exit_p)
max_window.bind("<Button-1>",max_window_1)
min_window.bind("<Button-1>",min_window_1)
#隐藏标题栏
def hide_title():
    global hide_title_state
    if hide_title_state.get()==True:
        #隐藏标题栏
        main.overrideredirect(boolean=True)
        fullscr.pack(padx=80)
        max_window.place(x=main.winfo_width()-50,y=16,anchor="w")
        exit_button.place(x=main.winfo_width()-30,y=18,anchor="w")
        min_window.place(x=main.winfo_width()-70,y=17,anchor="w")
    else:
        main.overrideredirect(boolean=False)#取消隐藏标题栏
        if fullscreen_state.get()==0:
            min_window.place_forget()
            max_window.place_forget()
            exit_button.place_forget()
            fullscr.pack(padx=10)
    if hide_title_state.get()==True:
        menu.bind("<Button-1>",replace_xy)
#关于我的弹出子窗口
about_me_window=None
def about_me(exist=None):
    global about_me_window
    try:
        def create():
            window=tk.Toplevel()
            window.title("关于我")
            window.minsize(340,250)
            window.resizable(False,False)
            return(window)
        if exist==None:
            about_me_window=create()
        else:
            about_me_window.deiconify()
    except tk.TclError as e:
        if str(e)==f"bad window path name \"{about_me_window}\"":
            about_me_window=create()
        else:
            raise
def about_program():
    pass
edit_config_window=None
def edit_config(exist=None):
    global edit_config_window
    try:
        def create():
            window=tk.Toplevel()
            window.title("编辑配置文件")
            window.minsize(500,350)
            window.config(bg="#b3c2ff")
            window.attributes("-alpha",0.95)
            window.resizable(False,False)
            window.transient(main)
            window.grab_set()
            edit_frame=tk.Frame(window,bg="#a0a0ff")
            edit_frame.place(x=10,y=50,height=280,width=150)
            name_list_title=tk.Label(edit_frame,text="名称列表",bg="#a0a0ff",fg="#0a0a0a",font=("楷体",16,"bold"))
            name_list_title.pack(padx=5,pady=5,anchor="nw")
            edit_list_frame=tk.Frame(edit_frame,bg="#0a0aff")
            edit_list_frame.pack(fill="both",side="left")
            list_bar=tk.Scrollbar(edit_list_frame)
            list_bar.pack(side="right",fill="y")
            name_list=tk.Listbox(edit_list_frame,yscrollcommand=list_bar.set)
            name_list.pack(fill="both",side="left",expand=True)
            def add_name(name_num=0,ranges=name_database):
                if name_num<=len(name_database)-1:
                    name_list.insert("end",ranges[name_num])
                    window.after(1,add_name,name_num+1)
            window.after(0,add_name)
            name_list.config(bg="#a0a0ff",font=("楷体",16,"bold"),fg="#0a0a0a",selectbackground="#0000e0",activestyle="dotbox",selectmode="slngle",bd=5,relief="flat",highlightbackground="#0a0aff",highlightcolor="#0a0aff")
            control_frame=tk.Frame(window,bg="#a0a0ff")
            control_frame.place(x=170,y=50,height=280,width=320)
            search_label=tk.Label(control_frame,text="搜索名称",bg="#a0a0ff",fg="#0a0a0a",font=("楷体",16,"bold"))
            search_label.place(x=10,y=5)
            search_entry=tk.Entry(control_frame,bg="#8383d3",relief="flat",fg="#fefeff",font=("楷体",18),insertbackground="#fefeff")
            search_entry.place(x=10,y=35,width=300,height=40)
            name_db_temp=list(name_database)
            selected_name=tk.Label(control_frame,bg="#a0a0ff",fg="#0a0a0a",font=("楷体",16,"bold"))
            selected_name.place(x=10,y=80)
            selected_entry=tk.Entry(control_frame,bg="#8383d3",relief="flat",fg="#fefeff",font=("楷体",18),insertbackground="#fefeff")
            selected_entry.place(x=10,y=115,width=300,height=40)
            replace_list=tk.Button(control_frame,text="修改",bg="#8383d3",fg="#fefeff",relief="flat",activebackground="#8080d0",activeforeground="#dedee3",state="disable",font=("楷体",14),wraplength=45)
            replace_list.place(x=15,y=165,height=30,width=50)
            delete_list_t=tk.Button(control_frame,text="删除",bg="#8383d3",fg="#fefeff",relief="flat",activebackground="#8080d0",activeforeground="#dedee3",state="disable",font=("楷体",14),wraplength=45)
            delete_list_t.place(x=70,y=165,height=30,width=50)
            add_list_t=tk.Button(control_frame,text="添加",bg="#8383d3",fg="#fefeff",relief="flat",activebackground="#8080d0",activeforeground="#dedee3",state="disable",font=("楷体",14),wraplength=45)
            add_list_t.place(x=125,y=165,height=30,width=50)
            clean_list=tk.Button(control_frame,text="清空",bg="#8383d3",fg="#fefeff",relief="flat",activebackground="#8080d0",activeforeground="#dedee3",state="disable",font=("楷体",14),wraplength=45)
            clean_list.place(x=180,y=165,height=30,width=50)
            add_del_label=tk.Label(control_frame,text="插入方式",bg="#a0a0ff",fg="#0a0a0a",font=("楷体",14,"bold"))
            add_del_label.place(x=25,y=200)
            add_del_opinion=tk.Menubutton(control_frame,state="disable",bg="#8383d3",fg="#fefeff",relief="flat",activebackground="#5456b0",activeforeground="#b4c1ef",font=("楷体",14),wraplength=210)
            add_del_opinion.place(x=15,y=230,width=215,height=30)
            add_del_opinion_menu=tk.Menu(add_del_opinion,tearoff=False,bg="#8383d3",fg="#fefeff",activebackground="#5454a0",activeforeground="#c0c0e0")
            add_del_opinion.config(menu=add_del_opinion_menu)
            save_list=tk.Button(control_frame,text="保存",bg="#8383d3",fg="#fefeff",relief="flat",activebackground="#8080d0",activeforeground="#dedee3",state="disable",font=("楷体",14),wraplength=68)
            save_list.place(x=235,y=165,height=30,width=70)
            save_list_apply=tk.Button(control_frame,text="直接使用而不保存",bg="#8383d3",fg="#fefeff",relief="flat",activebackground="#8080d0",activeforeground="#dedee3",state="disable",font=("楷体",14),wraplength=68)
            save_list_apply.place(x=235,y=200,height=60,width=70)
            edit_direction=tk.IntVar()
            a=tk.StringVar()
            search_result=[]
            def search_in_namedatabase(key_word):
                #split_key_word=[]
                search_result.clear()
                name_list.delete(0,"end")
                def find_key_word(name_index=0):
                    if name_index<len(name_db_temp):
                        if key_word in name_db_temp[name_index]:
                            search_result.append(name_db_temp[name_index])
                            name_list.insert("end",name_db_temp[name_index])
                        window.after(0,find_key_word,name_index+1)
                find_key_word()
            primary_word=search_entry.get()
            def search_namelist(entered=0):
                nonlocal primary_word
                if not primary_word==search_entry.get():
                    primary_word=search_entry.get()
                    search_in_namedatabase(search_entry.get())
                    entered=1
                else:
                    if (search_entry.get()=="") and (entered==1):
                        name_list.delete(0,"end")
                        add_name()
                        entered=0
                window.after(10,search_namelist,entered)
            search_namelist()
            def check_name_database_none():
                if name_database==[]:
                    start.config(state="disable")
                else:
                    start.config(state="normal")
            def save_list_command(done=1):
                def save_list_choice(is_save):
                    nonlocal done
                    name_database.clear()
                    for names in name_db_temp:
                        name_database.append(names)
                    if is_save==1:
                        if os.path.isdir("./namelist.json")==True:
                            msg.showerror("编辑配置文件",f"配置文件\"namelist.json\"为目录，请在保存之前删除此目录。",parent=window)
                        else:
                            try:
                                with open("./namelist.json","w",encoding="utf-8") as save_list_file:
                                    save_list_file.write(json.dumps(name_db_temp,ensure_ascii=False))
                                save_list.config(state="disable")
                            except PermissionError as e:
                                msg.showerror("编辑配置文件",f"配置文件\"namelist.json\"被拒绝访问，原因：\n{e}",parent=window)
                            except Exception as e:
                                msg.showerror("编辑配置文件",f"未知错误：\n{str(tb.format_exc())}",parent=window)
                        save_list_apply.config(state="disable")
                    else:
                        save_list_apply.config(state="disable")
                    check_name_database_none()
                    save_list_command(0)
                if done==0:
                    if not name_database==name_db_temp:
                        save_list.config(state="normal",command=lambda:save_list_choice(1))
                        save_list_apply.config(state="normal",command=lambda:save_list_choice(0))
                        save_list_command(1)
                else:
                    pass
                if done==0:
                    window.after(100,save_list_command,done)
            save_list_command(0)
            def add_del_opinions(selected=0,behind=1,pre_set=1):
                opinions=[["插入在最前面","插入在最后面"],["插入在前面","插入在后面"]]
                add_del_opinion.config(text=opinions[selected][behind])
                def set_a_opinion(behind_i):
                    add_del_opinion.config(text=opinions[selected][behind_i])
                    edit_direction.set(behind_i)
                if pre_set==0:
                    edit_direction.set(behind)
                    for i in range(0,len(opinions[selected]),1):
                        add_del_opinion_menu.add_command(label=opinions[selected][i],command=lambda i=i:set_a_opinion(i))
                else:
                    for i in range(0,len(opinions[selected]),1):
                        add_del_opinion_menu.entryconfig(i,label=opinions[selected][i],command=lambda i=i:set_a_opinion(i))
            add_del_opinions(pre_set=0)
            def entry_type(selected=0,name=""):
                if name_db_temp==[]:
                    selected_name.config(text="列表为空，请添加一项。")
                    delete_list_t.config(state="disable")
                    clean_list.config(state="disable")
                    add_del_opinion.config(state="disable")
                    add_list_t.config(command=lambda:add_t(0))
                else:
                    if selected==1:
                        selected_name.config(text=f"修改已选择：{name}")
                        add_del_opinions(selected=1,behind=edit_direction.get())
                        delete_list_t.config(state="normal")
                    else:
                        selected_name.config(text="未选择")
                        add_del_opinions(selected=0,behind=edit_direction.get())
                        delete_list_t.config(state="disable")
                        add_list_t.config(command=lambda:add_t(0))
                    clean_list.config(state="normal")
                    add_del_opinion.config(state="normal")
                def check_entry():
                    is_selected=(not name_list.curselection()==())
                    if selected_entry.get()=="":
                        replace_list.config(state="disable")
                        add_list_t.config(state="disable")
                    else:
                        add_list_t.config(state="normal")
                        if is_selected==True:
                            replace_list.config(state="normal")
                        else:
                            replace_list.config(state="disable")
                    window.after(100,check_entry)
                check_entry()
            entry_type()
            def cancel_selection(event=None):
                name_list.selection_clear(0,"end")
                entry_type(selected=0)
            selected_name.bind("<Button-1>",cancel_selection)
            def add_t(selected,name_index=None):
                if selected_entry.get() in name_db_temp:
                    msg.showerror("编辑配置文件",f"\"{selected_entry.get()}\"已在列表中存在。",parent=window)
                else:
                    if selected==1:
                        name_db_temp.insert(name_index+edit_direction.get(),selected_entry.get())
                        name_list.insert(name_index+edit_direction.get(),selected_entry.get())
                        name_list.see(name_index)
                    else:
                        if ((edit_direction.get()==0) or (name_db_temp==[])):
                            name_db_temp.insert(0,selected_entry.get())
                            name_list.insert(0,selected_entry.get())
                            name_list.see(0)
                        else:
                            name_db_temp.insert(len(name_db_temp),selected_entry.get())
                            name_list.insert(len(name_db_temp),selected_entry.get())
                            name_list.see("end")
                    selected_entry.delete(0,len(selected_entry.get()))
                    if not name_index==None:
                        name_list.see(name_index+edit_direction.get()+(-1)**edit_direction.get())
                        entry_type(selected=1,name=name_db_temp[name_index+edit_direction.get()+(-1)**edit_direction.get()])
                    else:
                        entry_type(0)
            def delete_t(name_index):
                def state_add_del_opinion():
                    if name_db_temp==[]:
                        delete_list_t.config(state="disable")
                        add_del_opinion.config(state="disable")
                        return False
                    else:
                        return True
                if name_list.get(name_list.size()-1)==name_list.get(name_index):
                    name_list.delete(name_list.size()-1)
                    name_list.selection_set(name_list.size()-1)
                    name_list.see(name_list.size()-1)
                    del name_db_temp[-1]
                    if state_add_del_opinion():
                        entry_type(selected=1,name=name_db_temp[-1])
                    else:
                        entry_type(selected=0)
                else:
                    name_list.delete(name_index)
                    name_list.selection_set(name_index)
                    name_list.see(name_index)
                    name_db_temp.pop(name_index)
                    entry_type(selected=1,name=name_db_temp[name_index])
             ##推到重做吧（已完善一些输入机制）
            def replace_name(name_index=None):
                if selected_entry.get() in name_db_temp:
                    msg.showerror("编辑配置文件",f"\"{selected_entry.get()}\"已在列表中存在。",parent=window)
                else:
                    name_db_temp[name_index]=selected_entry.get()
                    name_list.insert(name_index,selected_entry.get())
                    name_list.delete(name_index+1)
                    selected_entry.delete(0,len(selected_entry.get()))
                    name_list.selection_set(name_index)
                    entry_type(selected=1,name=name_db_temp[name_list.curselection()[0]])
                    replace_list.config(state="disable")
            def clean_name_list():
                name_db_temp.clear()
                name_list.delete(0,"end")
                entry_type()
            clean_list.config(command=clean_name_list)
            def selected_action(event):
                if name_list.curselection()==():
                    entry_type(selected=0)
                else:
                    if search_entry.get()=="":
                        entry_type(selected=1,name=name_db_temp[name_list.curselection()[0]])
                    else:
                        entry_type(selected=1,name=search_result[name_list.curselection()[0]])
                    delete_list_t.config(command=lambda:delete_t(name_list.curselection()[0]))
                    replace_list.config(command=lambda:replace_name(name_index=name_list.curselection()[0]))
                    add_list_t.config(command=lambda:add_t(1,name_list.curselection()[0]))
            name_list.bind("<<ListboxSelect>>",selected_action)
            list_bar.config(command=name_list.yview)
            list_bar.config(activebackground="#a0a0ff")
            return(window)
        if exist==None:
            edit_config_window=create()
        else:
            edit_config_window.deiconify()
    except tk.TclError as e:
        if str(e)==f"bad window path name \"{edit_config_window}\"":
            edit_config_window=create()
        else:
            raise
    
##设置菜单项
#设置菜单栏命令
settings=tk.Menubutton(menu,text="文件",bg="#50E885",anchor="e",activebackground="#50d385")#创建菜单按钮
settings.pack(padx=10,side="left")
about=tk.Menubutton(menu,text="关于",bg="#50E885",anchor="e",activebackground="#50d385")
about.pack(side="left")
#创建菜单
set_menu=tk.Menu(settings,tearoff=False,bg="#50E885",activebackground="#73d3A0",activeforeground="#102305")#设置菜单，active前缀的配置为点击后显示的颜色，bg为正常显示的背景色，fg为正常显示的字体颜色（前景色）
settings.config(menu=set_menu)#菜单绑定在菜单按钮上，点击后展开
set_menu.add_checkbutton(label="隐藏标题栏",command=hide_title,variable=hide_title_state)#设置可勾选菜单项，variable为显示或控制变量
reload=tk.Menu(set_menu,tearoff=False,bg="#50E885",activebackground="#73d3A0",activeforeground="#102305")#设置子菜单，foreground结尾为字体颜色，background结尾为背景颜色
set_menu.add_cascade(label="重新加载",menu=reload)#把子菜单绑定在一个主菜单项上
set_menu.add_command(label="编辑配置文件",command=lambda:edit_config(exist=edit_config_window))
about_menu=tk.Menu(about,tearoff=False,bg="#50E885",activebackground="#73d3A0",activeforeground="#102305")
about.config(menu=about_menu)
about_menu.add_command(label="关于我",command=lambda:about_me(exist=about_me_window))
about_menu.add_command(label="关于此程序",command=about_program)
#重新加载UTF-8编码
def reload_utf_8():
    start.config(state="normal")#开始按钮变得可点击
    json_config(encoding="utf-8")#传参编码utf-8（小写）
#重新加载utf-8-bom编码（我在这里踩过坑）
def reload_utf_8_bom():
    start.config(state="normal")
    json_config(encoding="utf-8-sig")#uff-8-bom编码名称
reload.add_command(label="以UTF-8编码重新加载",command=reload_utf_8)#设置菜单项
reload.add_command(label="以UTF-8-BOM编码重新加载（针对windows10早期版本）",command=reload_utf_8_bom)

##无标题栏状态下的移动窗口
def replace_xy(event):
    def replace_xy1(event):
        if hide_title_state.get()==True:
            #获取移动后的窗口位置（event.x和event.y持续获取，并分别与primary_x和primary_y来作差值表示移动距离，最后再分别与main.winfo_x()和main.winfo_y()相加来获取新窗口位置。）
            window_x=str(main.winfo_x()+(event.x-primary_x))
            window_y=str(main.winfo_y()+(event.y-primary_y))
            main.geometry(f"+{window_x}+{window_y}")#设置移动后窗口位置，这里只能用符号“+”来表示窗口位置，否则会报错
    menu.bind("<B1-Motion>",replace_xy1)#按下左键在菜单栏上移动时移动窗口
    #获取当前鼠标点击位置（为移动窗口作铺垫）
    primary_x=event.x
    primary_y=event.y
is_error_empty=0

##加载配置文件namelist.json
def json_config(encoding=None):#encoding默认值为空
    global name_database#声明全局变量
    global is_error_empty
    #捕捉异常
    try:
        #检查配置文件是否存在
        if os.path.isfile("./namelist.json")==True:
            bom=None#预留变量，并设置为空
            #自动检测编码
            if encoding==None:
                with open("./namelist.json","rb") as encodes:#用二进制形式打开文件，用with语句是为了能够完全打开或关闭文件
                    bom=encodes.read(3)#读配置文件的前三个字节
                if bom==b"\xef\xbb\xbf":#判断文件前3个字节是否有utf-8-bom的特征
                    encoding="utf-8-sig"#使用utf-8-bom编码
                else:
                    encoding="utf-8"#使用utf-8编码
            #用文本形式打开配置文件
            with open("./namelist.json","r",encoding=encoding) as namelist:
                names=json.load(namelist)#加载配置文件
                name_database=names
            if name_database==[]:#检查是否为空列表
                c.windll.user32.MessageBoxW(main.winfo_id(),"json配置为空，请在当前目录下的\"namelist.json\"中写入一个列表。","随机抽取-json配置为空",0x10)#弹窗报错
                #MessageBoxW(Owner,Text,Title,Style)
                #Owner-窗口所有者，仅弹窗用None，相当于c语言的Null。如果设置了窗口的id，则被设置的窗口将无法操作，并且会发出默认响声。当前Tkinter窗口的id可用上面代码获取
                #Text-弹窗文本，如果用英文双引号或者会破坏字符串结构的字符要在其前面加上转义符"\"，多行文本可用三引号字符串或者单引号时在要换行的部分加上"\n"，有变量在字符串里的要在字符串代码前面加上f
                #Title-弹窗标题，文本结构与上面一样
                #Style-弹出样式，为16进制数值（例如0x10）。在"x"后面的数字中，最后一个数为弹窗按钮组合方式，其余的为弹窗的类型，例如前面的数字1代表是错误窗口，后面的数字0为只有确定按钮。不同组合其带来的返回值可能不同，请用print来观察并用if 语句做判断。
                #具体使用方式请自行在网上搜索MessageBoxW函数，其排列方式与上面一样。
                #这个只能在Windows上使用，不能在其它系统使用。请注意看"c.windll"，这个是调用windows的dll的，MessageBoxW是win32函数。

                
                #多行文本 三引号："""Text1
                #                    Text2
                #                    Text3"""
                #换行符："Text1\nText2\nText3"
                #字符串代码前面的f：
                #   f"""text1 {变量}
                #       text2
                #       text3 {"字符串"}"""
                #   f"text1 {变量}\ntext2\ntext3 {"字符串"}"
                #外面的引号必须全为英语双引号或单引号
                #三引号字符串有时还可以当注释，只不过兼容性差一点

                
                start.config(state="disable")#禁用开始按钮
            else:
                is_error_empty=1#设置为非空列表
        else:
            if os.path.isdir("./namelist.json")==True:#检测配置是否为文件夹
                c.windll.user32.MessageBoxW(main.winfo_id(),"json配置为目录，请在当前目录下的\"namelist.json\"文件夹删除，然后再创建此文件","随机抽取-找不到json配置",0x10)
                start.config(state="disable")
            else:
                c.windll.user32.MessageBoxW(main.winfo_id(),"未找到json配置，请在当前目录下新建\"namelist.json\"文件","随机抽取-找不到json配置",0x10)
                start.config(state="disable")
    except json.decoder.JSONDecodeError as json_error:#检查json语法是否正确
        c.windll.user32.MessageBoxW(main.winfo_id(),"json语法不正确，原因：\n"+str(json_error),"随机抽取-json配置错误",0x10)
        if is_error_empty==0:#检查是否为异常配置文件
            start.config(state="disable")
    except FileNotFoundError as json_error:#检查文件存在性（基本被上面的if-else代码优先执行）
        c.windll.user32.MessageBoxW(main.winfo_id(),"找不到json文件，原因：\n"+str(json_error),"随机抽取-找不到json配置",0x10)
        if is_error_empty==0:
            start.config(state="disable")
    except PermissionError as json_error:#检查是否被拒绝访问
        c.windll.user32.MessageBoxW(main.winfo_id(),"json文件被拒绝读取，原因：\n"+str(json_error),"随机抽取-json配置读取失败",0x10)
        if is_error_empty==0:
            start.config(state="disable")
    except Exception as json_error:#检测其它异常来输出详细信息
        c.windll.user32.MessageBoxW(main.winfo_id(),"未知错误：\n"+str(tb.format_exc()),"随机抽取-错误",0x10)
        if is_error_empty==0:
            start.config(state="disable")
#延迟执行json_config的代码，主要是为了防止在加载界面时提前弹出错误窗口
main.after(300,json_config)
#防止主窗口消失
main.mainloop()


######我因为了急事而匆忙写代码，却忘记加注释。#######
######我在这里打了很久注释，大部分很详细。###########
######肝了比较久，终于把注释打完了(^ v ^)############
######以后还会再加新功能，这个比较简陋，下次要更肝了#
######作者：一名即将升入高一的毕业生，内向但坚定#####
