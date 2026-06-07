import random as rand
import tkinter as tk
import ctypes as c
import traceback as tb
import os,sys,json
os.chdir(os.path.dirname(sys.argv[0]))
main=tk.Tk()
main.minsize(500,500)
main.title("随机抽选")
#main.attributes("-fullscreen",True)
name=tk.Label(main,text="张",font=("楷体",40,"bold"),wraplength=490)
name.pack(pady=100)
start=tk.Button(main,text="随机抽选",relief="groove")
start.pack()
name_database=""
name_dict={}
using_name_dict={}
def json_config():
    try:
        if os.path.isfile("./namelist.json")==True:
            with open("./namelist.json","r",encoding="utf-8") as namelist:
                names=json.load(namelist)
                name_database=names
                if str(type(names))=="<class \'list\'>":
                    return
                else:
                    def subdict_p(range_list):
                        for class_name in list(range_list):
                            #print(range_list)
                            if isinstance(range_list,list)==True:
                                continue
                            else:
                                if isinstance(range_list[class_name],list)==True:
                                    name_dict[class_name]=""
                                elif isinstance(range_list[class_name],dict)==True:
                                    for sub_class_name in range_list:
                                        #sub_name_dict.append(sub_class_name)
                                        subdict_p(range_list[sub_class_name])
                                else:
                                    continue
                    subdict_p(name_database)
        else:
            c.windll.user32.MessageBoxW(main.winfo_id(),"json配置为目录，请创建一个","随机抽取-找不到json配置",0x10)
    except json.decoder.JSONDecodeError as json_error:
        c.windll.user32.MessageBoxW(main.winfo_id(),"json语法不正确，原因：\n"+str(json_error),"随机抽取-json配置错误",0x10)
    except FileNotFoundError as json_error:
        c.windll.user32.MessageBoxW(main.winfo_id(),"找不到json文件，原因：\n"+str(json_error),"随机抽取-找不到json配置",0x10)
    except PermissionError as json_error:
        c.windll.user32.MessageBoxW(main.winfo_id(),"json文件被拒绝读取，原因：\n"+str(json_error),"随机抽取-json配置读取失败",0x10)
    except Exception as json_error:
        c.windll.user32.MessageBoxW(main.winfo_id(),"未知错误：\n"+str(tb.format_exc()),"随机抽取-错误",0x10)
main.after(300,json_config)
print(name_dict)
main.mainloop()
