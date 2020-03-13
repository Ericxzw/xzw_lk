'''
解压缩软件
'''

# 导入所需要的库
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
import tkinter.messagebox
import zipfile
import os
import tkinter.filedialog
import base64
from compressed_software.icon import img
from PIL import Image, ImageTk

def get_image(imagename, width, height):
    '''
    打开指定的图片文件，缩放至指定尺寸
    :param imagename: 图片名称
    :param width: 图片尺寸——宽
    :param height: 图片尺寸——高
    :return: 返回得到的图片
    '''
    image = Image.open(imagename).resize((width, height))
    return ImageTk.PhotoImage(image)

def choose_compress_file():
    '''
    选择需要压缩的文件
    :return:
    '''
    compress_file_path_name.set(askdirectory())

def choose_uncompress_file():
    '''
    选择需要解压的文件
    :return:
    '''
    uncompress_file_path = askopenfilename()
    uncompress_file_path.replace("/", "\\\\")  # 字符转义
    uncompress_file_path_name.set(uncompress_file_path)

def choose_uncompress_dir():
    '''
    选择解压到的目录
    :return:
    '''
    uncompress_file_terminal_path_name.set(askdirectory())

def compress_file_success_message():
    '''
    压缩文件成功后，弹出信息框
    :return:
    '''
    tkinter.messagebox.askokcancel(title='success', message='压缩成功！')

def uncompress_file_success_message():
    '''
    解压文件成功后，弹出信息框
    :return:
    '''
    tkinter.messagebox.askokcancel(title='success', message='解压成功！')

def uncompress_file_failure_message():
    '''
    解压失败弹出框
    :return:
    '''
    tkinter.messagebox.askokcancel(title='failed', message='这不是zip压缩文件！')

def compress_file():
    '''
    压缩文件
    :return:
    '''
    # 给压缩文件加上.zip
    compress_file_name = compress_file_path_name.get() + '.zip'

    # 写入
    zip = zipfile.ZipFile(compress_file_name, 'w', zipfile.ZIP_DEFLATED)

    # 遍历目录路径、目录名、文件名
    for dirpath, dirnames, filenames in os.walk(compress_file_path_name.get()):
        fpath = dirpath.replace(compress_file_path_name.get(), '')
        fpath = fpath and fpath + os.sep or ''

        # 迭代文件名
        for filename in filenames:
            zip.write(os.path.join(dirpath, filename), fpath + filename)  # 写入
        zip.close()

        # 压缩成功，弹出信息框
        compress_file_success_message()

def upcompress_file():
    '''
    解压缩文件
    :return:
    '''
    # 判断是否为压缩文件，以文件后缀是否为.zip为判断依据
    is_true = zipfile.is_zipfile(uncompress_file_path_name.get())

    if is_true:
        # 读取压缩文件
        unzip = zipfile.ZipFile(uncompress_file_path_name.get(), 'r')
        # 遍历文件
        for file in unzip.namelist():
            # 输出文件
            unzip.extract(file, uncompress_file_terminal_path_name.get())

        # 解压成功，弹出信息框
        uncompress_file_success_message()
    else:
        # 解压失败，弹出信息框
        uncompress_file_failure_message()

def graphical_user_interface():
    '''
    图形用户界面
    :return:
    '''
    # label：row代表label是放在第几行，column是放在第几列
    Label(root, text='压缩文件路径：').grid(row=0, column=0)

    # entry：获取输入
    Entry(root, textvariable=compress_file_path_name).grid(row=0, column=1)

    # 操作按钮
    Button(root, text='选择压缩文件', command=choose_compress_file).grid(row=0, column=2)

    # label标签
    Label(root, text='解压文件路径：').grid(row=1, column=0)

    # 获取输入
    Entry(root, textvariable=uncompress_file_path_name).grid(row=1, column=1)

    # 操作按钮
    Button(root, text='选择解压文件', command=choose_uncompress_file).grid(row=1, column=2)

    # label标签
    Label(root, text='解压到：').grid(row=2, column=0)

    # 获取输入
    Entry(root, textvariable=uncompress_file_terminal_path_name).grid(row=2, column=1)

    # 操作按钮
    Button(root, text='选择解压路径', command=choose_uncompress_dir).grid(row=2, column=2)

    # 操作按钮
    Button(root, text='点击压缩', command=compress_file).grid(row=3, column=0)

    # 操作按钮
    Button(root, text='点击解压', command=upcompress_file).grid(row=3, column=2)

    # 操作按钮
    Button(root, text='退出', command=root.quit).grid(row=4, column=1)

    # 显示操作界面
    root.mainloop()

if __name__ == '__main__':

    # # base64转码，将转码后的文件存入icon.py中，为了节省资源，此块代码运行一次即可
    # open_icon = open("xzw.ico", "rb")
    # b64str = base64.b64encode(open_icon.read())
    # open_icon.close()
    # write_data = "img = %s" % b64str
    # f = open("icon.py", "w+")
    # f.write(write_data)
    # f.close()

    # 初始化，并设置文件名称
    root = Tk(className='轻压-极简版')

    # 设置root大小不变
    root.resizable(width=False, height=False)

    # 设置标题，与root = Tk(className='轻压-极简版')有异曲同工之妙
    # root.title('轻压')

    # 设置压缩屏幕大小
    root.geometry('800x600')

    # # 创建画布，设置要显示的图片，把画布添加至应用程序窗口
    # canvas = tkinter.Canvas(root)
    # im_root = get_image('favicon.ico', 800, 600)
    # canvas.create_image(800, 600, image=im_root)
    # canvas.pack()

    # 读取base64转码后的数据，并设置压缩图标
    picture = open("picture.ico", "wb+")
    picture.write(base64.b64decode(img))
    picture.close()
    root.iconbitmap('picture.ico')
    os.remove("picture.ico")

    # 设置压缩图标，此方法打包exe后不可用，因为相应路径下没有图片，故使用base64进行转码
    # root.iconbitmap(default='xzw.ico')

    # 显示需要压缩的文件路径名
    compress_file_path_name = StringVar()

    # 显示需要解压的文件路径名
    uncompress_file_path_name = StringVar()

    # 显示文件想要解压到的路径名
    uncompress_file_terminal_path_name = StringVar()

    # 函数调用，显示图形用户界面
    graphical_user_interface()
