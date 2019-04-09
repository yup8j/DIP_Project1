import cv2
import numpy as np


def remove_pore(im, pore_size_max):
    image, contours, hierarchy = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area <= pore_size_max:
            cv2.drawContours(image, [contours[i]], 0, 0, -1)
    return image


def preprocess(num):
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
    # 形态学变换
    closing = cv2.morphologyEx(im_rp1, cv2.MORPH_CLOSE, kernel=np.ones((3, 3), np.uint8))
    im_final = closing
    return im_final, num


def img_write(image, num):
    cv2.imwrite('./im_process/result_' + str(num) + '.bmp', image)
    return "Picture {} .".format(num)


img_list = [7, 17, 27]
for img in img_list:
    final, num = preprocess(img)
    img_write(final, num=num)
