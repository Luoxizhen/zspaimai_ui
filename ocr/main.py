
from PIL import Image,ImageFilter
import pytesseract
import os


def img_to_words(img_path):
    img = Image.open(img_path)

    print("{}和{}和{}".format(img.width,img.height,img.size))
    img1 = img.crop((0,0,img.width,img.height/2))
    img1.show()

    words = pytesseract.image_to_string(img1,lang="chi_sim+eng+chi_tra")
    print(words)
    # print("{}-{}".format(words[words.find("Block")+6:words.find("Block")+9],words[words.find("S/N")+4:words.find("Block")]))

    return words




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path = "/Users/yuanyuanhe/Desktop/img/2103-1.jpeg"
    # file_path = "/Users/yuanyuanhe/Desktop/img/1152-1.jpeg"
    # file_path = "https://online-1303141635.cos.ap-guangzhou.myqcloud.com/picture/2021-11-18/893-1.jpg"
    img_to_words(file_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
