import cv2
import numpy as np


# 去除汗孔
def remove_pore(im, pore_size_max):
    '''
    :param im: 需要去除汗孔的图像
    :param pore_size_max: 汗孔面积的最大值（经验值）
    :return: 处理后图像
    '''
    # cv2.RETR_EXTERNAL：只检测外轮廓
    # cv2.CHAIN_APPROX_NON：存储所有的轮廓点
    image, contours, hierarchy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area <= pore_size_max:
            cv2.drawContours(image, [contours[i]], 0, 0, -1)
    return image


def preprocess(num):
    '''
    对图像进行处理，彩色图变为二值图，移除汗孔，细节处理
    :param num: 要处理的图像编号
    :return: 处理后的图像，图像编号
    '''
    # 读入
    im = cv2.imread('./im/' + str(num) + '.bmp')
    # 变为灰度图
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # 均值滤波：去除椒盐噪声
    im_median = cv2.medianBlur(im_gray, 5)
    # 高斯滤波：去除高斯噪声
    im_gauss = cv2.GaussianBlur(im_median, (3, 3), 0)
    # 二值化：OTSU方法
    ret, im_thresh = cv2.threshold(im_gauss, 0, 255, cv2.THRESH_OTSU)

    # 移除汗孔
    im_rp1 = remove_pore(im=im_thresh, pore_size_max=36)
    cv2.imshow('rp', im_rp1)
    # 形态学变换
    closing = cv2.morphologyEx(im_rp1, cv2.MORPH_CLOSE, kernel=np.ones((3, 3), np.uint8), iterations=1)
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(im_rp1, kernel, iterations=2)
    ero = cv2.erode(dilation, kernel, iterations=2)
    im_final = closing
    cv2.imshow('closing', closing)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return im_final, num


def img_write(image, num):
    '''
    将处理后的图像写入
    :param image:处理后图像
    :param num:图像编号
    :return:成功信息
    '''
    cv2.imwrite('./im_process/result_' + str(num) + '.bmp', image)
    return "Picture {} .".format(num)


if __name__ == '__main__':
    img_list = [7, 17, 27]
    for img in img_list:
        final, num = preprocess(img)
        img_write(final, num=num)
