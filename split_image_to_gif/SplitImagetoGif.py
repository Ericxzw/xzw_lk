'''
切分长图，将切分后的图片组成动图
'''
import argparse
from PIL import Image
import os


class StaticTransDynamic:
    '''
    将长图分割成一张张图片，然后将分割成的图片变成动图
    '''

    def __init__(self):
        '''
        构造方法
        '''
        # os.path.abspath：获取文件的绝对路径；os.path.split：切分文件路径与文件名称。
        self.dir_name = os.path.split(os.path.abspath(__file__))[0]  # 获取文件所在的目录名称
        self.image_path = args.image_path  # 图片路径
        self.split_times = args.split_times  # 切分次数
        self.change_time = args.change_time  # 图片更换时间
        self.path, self.file = os.path.split(self.image_path)  # 获取图片的路径以及名称
        self.image = self.check_image_file()  # 检测图片文件，获取图片
        self.pictures = []  # 图片列表

    def check_image_file(self):
        '''
        检测图片文件
        :return:
        '''
        # 定义图片类型的私有变量
        __image_type = ['.jpg', '.png', '.bmp']

        if not os.path.isfile(self.image_path):  # 如果图片路径不是一个文件
            raise IOError("图片路径错误，请检查图片路径：", self.image_path)
        # os.path.splitext：切分得到文件的路径以及后缀
        elif os.path.splitext(self.file)[1].lower() not in __image_type:  # 如果图片类型不在定义的类型列表中
            raise TypeError("图片类型错误，请选择如下类型：", __image_type)
        else:  # 打开图片
            return Image.open(self.image_path)

    def split_long_image(self):
        '''
        切分长图并保存
        :return:
        '''
        os.chdir(self.path)  # 将工作目录更改为图片的目录路径
        try:
            os.makedirs('images')  # 新建目录images
        except FileExistsError:  # 定义文件存在的异常
            pass

        width, height = self.image.size  # 获取文件的宽和高
        __split_height = height / self.split_times  # 获取每次切分的高度

        for image in range(self.split_times):  # 获取图片并保存
            # 划定每张图片的大小
            __crop_box = (0, __split_height * image, width * 0.8, __split_height * (image + 1))
            # 得到每张图片
            __per_picture = self.image.crop(__crop_box)
            __picture_name = os.path.join(self.path, 'images', "image%d.png" % (image + 1))
            self.pictures.append(__picture_name)
            __per_picture.save(__picture_name)

    def get_gif(self):
        '''
        静图转换成动图
        :return:
        '''
        images = []
        file = Image.open(self.pictures[0])
        for image in self.pictures[1:]:
            images.append(Image.open(image))
        gif_name = os.path.join(self.path, "result.gif")
        file.save(gif_name, save_all=True, loop=True, append_images=images, duration=self.change_time * 1000)


if __name__ == '__main__':
    # 创建一个解析对象
    parser = argparse.ArgumentParser()
    # 向创建的解析对象中添加命令行参数和选项
    parser.add_argument('-i', '--image_path', help="需要进行分割操作的图片路径")
    parser.add_argument('-s', '--split_times', type=int, help="图片分隔次数")
    parser.add_argument('-c', '--change_time', type=float, help="GIF动图切换时长")
    # 解析
    args = parser.parse_args()

    if None in args.__dict__.values():
        parser.print_help()
    else:
        std = StaticTransDynamic()
        std.split_long_image()
        std.get_gif()
