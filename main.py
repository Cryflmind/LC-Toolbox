#作者：Cryflmind
#QQ:3244118528
import Lcmd
import pygame
import random
import os
import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory #导入路径选择框
import threading
from threading import Thread
import webbrowser
import psutil


#初始化变量和控件
pygame.mixer.init()
SEARCHENGINE = ["360","百度","必应","学科网"]
print("")
config={}
music_list = []
music_address=''
pressedF1 = False
music_is_playing = True
index = 0
index_copy = 0
#此处采用2个index用于解决args的迭代器要求
process_list = []

def get_process():
    #获取当前所有的进程
    pids = psutil.pids()
    global process_list
    for pid in pids:
        try:
            p = psutil.Process(pid)
            process_list.append(p.name())
        except:
            pass


def flushindex(): #刷新index
    global index
    global index_copy
    index = index_copy

def readConfig(): #读取config.ini
    try:
        if(os.path.exists('config.ini')):
            config_file = open('config.ini','r')
            config_list = config_file.read().split('=')
            for i in range(0,len(config_list),2):
                config[config_list[i]]=config_list[i+1].replace('\n','')
            config_file.close()
        else:
            print("No config.ini found!")
    except:
        pass

def loadConfig():
    readConfig()
    try:
        background_music = ''
        background_music = config['[musicLoadingAddress]']
    except:
        config['[musicLoadingAddress]'] = r".\datas\example music"
    try:
        global music_address
        music_address=config['[musicLoadingAddress]']
        for file in os.listdir(music_address):
            if os.path.splitext(file)[1] == '.mp3':
                music_list.append(file)
    except:
        pass


loadConfig()

def thread_music(index,is_worked):
    global music_is_playing
    if is_worked:
        lock = threading.Lock() #设置线程锁，锁定index更换数据
        if pygame.mixer.music.get_busy():
            if pressedF1:
                pygame.mixer.music.stop()
                lock.acquire()
                music_is_playing = change_the_music()
                lock.release()
            else:
                pass
        else:
            if music_is_playing:
                lock.acquire()
                global index_copy
                index_copy=change_the_index()
                music_name = music_list[index_copy]
                lock.release()
                flushindex() #利用index_copy刷新index的值，防止发生异步
                play_background_music(music_name)
    else:
        pygame.mixer.music.stop()



"""
def startGame(index):
    #Hello World!
    if (index == 1): #废弃功能
        gamethread = Thread(target=epidemic_controler.main)
        gamethread.start()
        gamethread.join() #堵塞主线程，防止同时执行

"""



def play_background_music(music_name): #音乐主函数
    try:
        pygame.mixer.music.load(music_address+"\\"+music_name)
        pygame.mixer.music.play(1,0,0)
    except pygame.error:
        print("\nOh no,音频文件似乎丢失了！虽然这并不影响使用，但会影响使用体验哦~所以快去联系作者获取完整的数据文件吧！这样才能获得最佳体验~awa")
        sys.exit()
    except:
        pygame.mixer.music.load(music_address+"\\"+music_name)
        pygame.mixer.music.play(1,0,0)



def change_the_music(index=1): #修改音乐
    global pressedF1
    pressedF1 = False
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        is_playing = False
    else:
        play_background_music(music_list[change_the_index()])
        is_playing = True
        time.sleep(0.5)  # 防止按键重复检测
    return is_playing



def change_the_index(): #修改音乐ID
    global index
    temp = random.SystemRandom.randint(random,0,len(music_list)-1)
    """if index > 10:
        index = 1"""
    while temp == index:
        temp = random.SystemRandom.randint(random,0, len(music_list)-1)
    index = temp
    return index

def changepress(event):
    global pressedF1
    pressedF1 = True

def INIT(): #初始化
    print("正在初始化……")
    mainWindow = tk.Tk()
    mainWindow.title("龙喵工具箱")
    Lcmd.Init()
    return mainWindow


def musicPlaying(index,is_worked): #控制函数
    while True:
        music_control = Thread(target=thread_music, args=(music_list[index], is_worked),daemon=True)  # 将音乐相关模块交给另一个线程
        music_control.setDaemon(True)  # 设置为守护进程，防止关闭Tk窗口时仍在播放音乐
        music_control.start()
        #time.sleep(3)
        for i in range(0, 12):
            if pressedF1:
                break
            time.sleep(0.25) #设长一点防止长按F1导致的程序异步



def main(): #主窗体
    Mainwindow = INIT() #程序整体初始化
    Mainwindow.bind("<F1>",changepress)
    skip_background=0
    is_worked = True
    music_controler = Thread(target=musicPlaying, args=(index,is_worked),daemon=True)
    music_controler.setDaemon(True)  # 设置为守护进程，防止关闭Tk窗口时仍在播放音乐
    music_controler.start()
    width = 344
    height = 105
    screenwidth = Mainwindow.winfo_screenwidth() #屏幕宽度
    screenheight = Mainwindow.winfo_screenheight() #屏幕高度
    Mainwindow.geometry("%dx%d+%d+%d" % (width, height, (screenwidth-width)/2, (screenheight-height)/2)) #差值居中-格式化输入
    Mainwindow.resizable(0,0) #锁定窗口大小，禁止拉伸
    try:
        background_photo = tk.PhotoImage(file=".\\datas\\Mainbackground.png")
        Mainbackground = tk.Canvas(Mainwindow)
        Mainbackground.create_image(172,50,image=background_photo)
    except:
        print("背景图片似乎丢失了哦owo，快去联系作者以获取最佳体验吧！w~")
        skip_background=1
    TEXT1 = tk.Label(Mainwindow,text="欢迎使用龙喵工具箱~")
    TEXT1.grid(row=0,column=1)
    TEXT2 = tk.Label(Mainwindow,text="Tips:按下F1可以切换背景音乐哦w~")
    TEXT2.grid(row=6, column=1)
    global list1 #全局化下拉框，方便读取选项
    list1 = ttk.Combobox(Mainwindow,state='readonly',values=SEARCHENGINE,width=5)
    list1.current(1)
    list1.grid(row=4,column=0)
    cleaningButton = tk.Button(Mainwindow,text="垃圾清理",command=Lcmd.computerCleaning)
    taskkillerButton = tk.Button(Mainwindow, text="结束指定进程", command=FtaskkillerWindow)
    renameButton = tk.Button(Mainwindow, text="文件格式化", command=FrenameWindow)
    searchButton = tk.Button(Mainwindow, text="搜索喵", command=Fsearcher,height=1,width=5)
    global entry1 #全局化文本框，方便进行数据读取
    entry1 = tk.Entry(Mainwindow,exportselection=0,width=30)
    entry1.grid(row=4,column=1)
    cleaningButton.grid(row=2,column=0)
    taskkillerButton.grid(row=2,column=1)
    renameButton.grid(row=2,column=2)
    searchButton.grid(row=4,column=2)
    if(not skip_background):
        Mainbackground.place(x=0,y=0)
    Mainwindow.mainloop()


proname=None
def flushEntry(process_list_gui):
    global proname
    proname=process_list_gui.widget.get(process_list_gui.widget.curselection())

def FtaskkillerWindow(): #结束进程窗体
    taskkillerWindow = tk.Toplevel()
    taskkillerWindow.title("结束指定进程")
    width = 355
    height = 182
    TEXT = tk.Label(taskkillerWindow, text="待关闭进程名称：")
    TEXT.place(x=0,y=3)
    #nameEntry = tk.Entry(taskkillerWindow, width=15,textvariable=proname) #进程名称
    #nameEntry.place(x=160,y=5)
    startButton = tk.Button(taskkillerWindow, text="点击关闭",command=lambda: Lcmd.taskkiller(proname),width=8)  # 关闭按钮
    startButton.place(x=280,y=0)
    get_process()
    process_list_gui = tk.Listbox(taskkillerWindow,selectbackground='blue',width=50,height=8)
    for t in process_list:
        process_list_gui.insert('end',t)
    process_list_gui.place(x=0, y=30)
    screenwidth = taskkillerWindow.winfo_screenwidth()  # 屏幕宽度
    screenheight = taskkillerWindow.winfo_screenheight()  # 屏幕高度
    taskkillerWindow.geometry("%dx%d+%d+%d" % (width, height, (screenwidth - width) / 4, (screenheight - height) / 4))  # 差值左上-格式化输入
    taskkillerWindow.resizable(0, 0)  # 锁定窗口大小，禁止拉伸
    process_list_gui.bind('<<ListboxSelect>>',flushEntry)



def FchooseDir(): #选择路径
    temp = askdirectory()
    global Dir
    Dir.set(temp)



def rewindow(): #文本框文字刷新
    global dirEntry
    dirEntry["text"] = Dir



def reState(): #选中状态刷新
    global Ischosed
    Ischosed.set(Ischosed.get() == 0)



def FrenameWindow(): #文件格式化窗体
    global Dir
    Dir = tk.StringVar() #初始化字符串数据
    renameWindow = tk.Toplevel()
    renameWindow.title("文件格式化")
    GTEXT = tk.Label(renameWindow, text="待处理文件所在目录路径(如无需编号请选择根目录路径)：")
    GTEXT.grid(row=0, column=0)
    global dirEntry
    dirEntry = tk.Entry(renameWindow, width=48,textvariable=Dir) #路径文本框
    dirEntry.place(x=5,y=25)
    renameWindow.after(0,rewindow()) #强制刷新文字
    renameWindow.update()
    chooseDir  = tk.Button(renameWindow, text="···", command=FchooseDir,width=5,height=1) #路径选择按钮
    chooseDir.place(x=350,y=20)
    global Ischosed
    Ischosed = tk.IntVar()
    Ischosed.set(1)
    renameWindow.after(0, reState())  # 强制刷新数据
    renameWindow.update()
    Clickindex = tk.Checkbutton(renameWindow,text="需要对该目录下文件进行编号",variable=Ischosed)
    Clickindex.place(x=0,y=50)
    STEXT = tk.Label(renameWindow, text="将后缀统一成：")
    STEXT.place(x=0,y=75)
    nameEntry = tk.Entry(renameWindow, width=5)  # 格式文本框
    nameEntry.place(x=86, y=77)
    startButton = tk.Button(renameWindow, text="开始处理", command=lambda : Lcmd.renamer(Ischosed.get()+1,dirEntry.get().replace("/","\\"),\
                                                                                    nameEntry.get()), width=10, height=1)  # 开始按钮(文件路径要先进行转义再使用)
    startButton.place(x=155, y=100)
    width = 400
    height = 140
    screenwidth = renameWindow.winfo_screenwidth()  # 屏幕宽度
    screenheight = renameWindow.winfo_screenheight()  # 屏幕高度
    renameWindow.geometry("%dx%d+%d+%d" % (width, height, (screenwidth - width) / 4, (screenheight - height) / 4))  # 差值左上-格式化输入
    renameWindow.resizable(0, 0)  # 锁定窗口大小，禁止拉伸



def Fsearcher(): #搜索功能（GET请求）
    pattern = list1.get()
    key = entry1.get()
    if (pattern == "360"):
        webbrowser.open("https://www.so.com/s?ie=utf-8&q="+key)
    elif (pattern == "百度"):
        webbrowser.open("https://www.baidu.com/s?ie=utf-8&wd="+key)
    elif (pattern == "必应"):
        webbrowser.open("https://cn.bing.com/search?q="+key)
    elif (pattern == "学科网"):
        webbrowser.open("https://search.zxxk.com/books/?kw="+key)



if __name__ == '__main__': #主程序
    main()
