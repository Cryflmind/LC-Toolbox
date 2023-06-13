import os
from tkinter.messagebox import * #用于弹出错误提示框


def attribset(fileName,pattern=1): #初始化属性
    if (pattern == 1):
        os.system("attrib +h +s " + fileName) #添加隐藏、系统属性
    elif (pattern == 2):
        os.system("attrib -h -s " + fileName)  # 去除隐藏、系统属性



def exitset(temp,pattern,filename=None): #补写退出代码
    if (pattern == 1):
        temp.write(r"exit") #退出
    if (pattern == 2):
        temp.write(r"attrib -h -s -r -a %0"+"\n")
        temp.write(r"del \F \Q "+filename+" && exit"+"\n") #自销毁并退出
    return temp



def Init(): #初始化
    if os.path.exists(r".\clean.bat"): #如果文件已经存在，则跳过此文件的初始化
        pass
    else:
        #初始化垃圾清理程序
        temp = open("clean.bat","w")
        temp.close()
        #给文件加一次隐藏属性
        attribset("clean.bat",1)
        temp = open("clean.bat","a")
        temp.write(r"@echo off" + "\n")
        temp.write(r"color 0a" + "\n")
        temp.write(r"title Junk Cleaning" + "\n")
        temp.write(r"echo 正在为您清除系统垃圾，请稍等...... (此过程持续时间较长，清理完成后将自动关闭。）"+"\n")
        temp.write(r"del /f /s /q %systemdrive%\*.tmp "+"\n")
        temp.write(r"del /f /s /q %systemdrive%\*._mp " + "\n")
        temp.write(r"del /f /s /q %systemdrive%\*.log " + "\n")
        temp.write(r"del /f /s /q %systemdrive%\*.gid  " + "\n")
        temp.write(r"del /f /s /q %systemdrive%\*.chk " + "\n")
        temp.write(r"del /f /s /q %systemdrive%\*.old " + "\n")
        temp.write(r"del /f /s /q %systemdrive%\recycled\*.* " + "\n")
        temp.write(r"del /f /s /q %windir%\*.bak " + "\n")
        temp.write(r"del /f /s /q %windir%\prefetch\*.* " + "\n")
        temp.write(r"rd /s /q %windir%\temp & md %windir%\temp " + "\n")
        temp.write(r"del /f /q %userprofile%\cookies\*.* " + "\n")
        temp.write(r"del /f /q %userprofile%\recent\*.* " + "\n")
        temp.write(r'del /f /s /q "%userprofile%\Local Settings\Temporary Internet Files\*.*" ' + "\n")
        temp.write(r'del /f /s /q "%userprofile%\Local Settings\Temp\*.*" ' + "\n")
        temp.write(r'del /f /s /q "%userprofile%\recent\*.*" ' + "\n")
        temp = exitset(temp,1)
        temp.close()
    if os.path.exists(r".\taskkiller.bat"):  # 如果文件已经存在，则跳过此文件的初始化
        pass
    else:
        #初始化进程关闭程序(注意此文件需要随时修改执行,固需要先进行一次复制)
        temp = open("taskkiller.bat", "w")
        temp.close()
        # 给文件加一次隐藏属性
        attribset("taskkiller.bat",1)
        temp = open("taskkiller.bat", "a")
        temp.write(r"@echo off" + "\n")
        temp.write(r"color 0a" + "\n")
        temp.write(r"title Taskkiller" + "\n")
        temp.close()
    if os.path.exists(r".\renamer.bat"):  # 如果文件已经存在，则跳过此文件的初始化
        pass
    else:
        #初始化后缀批量修改程序(注意此文件需要随时修改执行,固需要先进行一次复制)
        temp = open("renamer.bat", "w")
        temp.close()
        # 给文件加一次隐藏属性
        attribset("renamer.bat",1)
        temp = open("renamer.bat", "a")
        temp.write(r"@echo off" + "\n")
        temp.write(r"color 0a" + "\n")
        temp.write(r"title renamer" + "\n")
        temp.close()



def computerCleaning(): #垃圾清理
    os.system("start clean.bat")



def taskkiller(processName): #进程结束代码生成器
    if processName==None:
        showerror("错误", "喵！你还没有选择进程名称呢！xwx")
        return None
    attribset("taskkiller.bat",2) #解除占用
    os.system("copy taskkiller.bat taskkillerTEMP.bat") #复制一份副本
    attribset("taskkiller.bat", 1) #重新隐藏
    attribset("taskkillerTEMP.bat",1) #将新的副本隐藏,准备添加核心代码
    temp = open("taskkillerTEMP.bat","a")
    temp.write("taskkill /F /IM "+processName+"\n")
    temp = exitset(temp,2,"taskkillerTEMP.bat")
    temp.close()
    os.system("start taskkillerTEMP.bat")



def renamer(pattern,fileDir,rend=""): #重命名代码生成器
    if fileDir == "": #未选择路径就点击了执行
        showerror("错误", "喵！你还没有选择或填写目录路径呢！xwx")
        return;
    attribset("renamer.bat",2) #解除占用
    os.system("copy renamer.bat renamerTEMP.bat") #复制一份副本
    attribset("renamer.bat", 1) #重新隐藏
    attribset("renamerTEMP.bat",1) #将新的副本隐藏,准备添加核心代码
    temp = open("renamerTEMP.bat","a")
    if (pattern == 1): #群体根目录全处理模式（适用于所有格式全部统一的情况）
        temp.write("for /F \"delims=?\" %%a in ('dir /s /a /b ^\""+fileDir.replace("(","^(").replace(")","^)")+"^\"')"+' do ren "%%a" *.'+rend+"\n")
    elif (pattern == 2): #编号模式(先改名再改后缀！！！)
        count = 1
        for names in os.listdir(fileDir):
            temp.write('ren "'+fileDir+"\\"+names+'" "'+str(count)+'-'+names+'"'+"\n")
            count+=1
        if(rend==""):
            ans=askyesno("警告","嗯？你似乎只选择了编号，而没有填写需要修改的后缀呢？\n喵……如果继续所有文件的后缀都将会被清除！\n是否继续？\n【如果选择\"No\"，程序将会保留你的文件后缀，只会进行文件编号】")
            if(ans):
                temp.write("for /F \"delims=?\" %%a in ('dir /a /b ^\"" + fileDir.replace("(","^(").replace(")","^)")+ "^\"')" + ' do ren "'+fileDir+"\\"+'%%a" *.' + rend + "\n")
    temp = exitset(temp,2,"renamerTEMP.bat")
    temp.close()
    os.system("start renamerTEMP.bat")
