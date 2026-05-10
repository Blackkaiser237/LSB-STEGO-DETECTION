import random

import numpy as np
import cv2 as cv
import numpy
from cryptography.fernet import Fernet
from tkinter import simpledialog

# hi=cv.imread('test.png')
cover = cv.imread("3.jpg")
end = '...'
initial = cover.shape
end_byte = b'\x00\x00\x01\x00\x01\x01\x01\x00'
end_byte1 = b'\x00\x00\x01\x00\x00\x01\x00\x00'
end_byte2 = b'\x00\x00\x01\x00\x01\x00\x01\x01'
packet = 0


def test(img):
    if type(img) == bytes:
        return [format(i, "08b") for i in img]
    elif type(img) == numpy.ndarray:
        return [bin(i)[2:] for i in img.flatten('F')]
    elif type(img) == str:
        return ''.join([format(ord(i), "08b") for i in img])
    elif type(img) == int or type(img) == numpy.uint8:
        return format(img, "08b")


# test=test(hit)
# decode=''
# for i in test:
#     decode+=chr(int(i,2))
# inter=decode.encode()

def segment(message, cover):
    packet = 0
    if type(message) == numpy.ndarray:
        mBytes = len(message)
        cBtyes = cover.shape[0] * cover.shape[1] * 24
    else:
        mBytes = len(message)
        cBtyes = cover.shape[0] * cover.shape[1] * 24
    print(mBytes, cBtyes)
    if mBytes <= cBtyes:
        if 10 < len(message) < 100000:
            packet = random.randint(10, 45)
        if 100000 < len(message) < 10000000:
            packet = random.randint(20, 50)
        elif 10000000 < len(message) < 100000000:
            packet = random.randint(50, 100)
        elif 100000000 < len(message) < 1000000000:
            packet = random.randint(100, 200)
    else:
        return "Not enough pixels in your image to hide the data ! Choose another image"
    print("Dividing into {} packets".format(packet))
    return [numpy.array_split(numpy.array(message), packet), packet, message]


def back(img):
    return [int(i, 2) for i in img]


# cover_bin=test(cover)
# msg_bin=test(hit)
# msg_seg=segment(hit,cover)

def encode_ext(cover_img, extension_bin):
    ext_pos = 0
    pixel = 0
    for ext in cover_img:
        for ext1 in ext:
            if ext_pos < len(extension_bin) and pixel != 0:
                ext1[0] = int(test(ext1[0])[:-2] + extension_bin[ext_pos] + test(ext1[0])[-1], 2)
                ext_pos += 1
            if ext_pos < len(extension_bin) and pixel != 0:
                ext1[1] = int(test(ext1[0])[:-2] + extension_bin[ext_pos] + test(ext1[0])[-1], 2)
                ext_pos += 1
            if ext_pos < len(extension_bin) and pixel != 0:
                ext1[2] = int(test(ext1[0])[:-2] + extension_bin[ext_pos] + test(ext1[0])[-1], 2)
                ext_pos += 1
            if ext_pos == len(extension_bin):
                break
            pixel += 1


def encode_data(encode_msg, cover_img, pwd, extension_bin, output, key=''):
    extension_bin = test(extension_bin)
    cover_img[-2, -2][1] = 32
    if pwd!='N/A':
        pwd = test(pwd)
        cover_img[-1, -1][2] = len(pwd)
        print(cover_img[-1,-1][2])
        cover_img[-2, -2][0] = 3
    else:
        pwd='N/A'
    temp_msg = np.unpackbits(encode_msg[2])
    print('key is ', key)
    my_key_bin = ''.join(format(i, '08b') for i in key)
    my_key_len = len(my_key_bin)
    key_pos = 0
    msg_pos = 0
    pss_pos = 0
    ext_pos = 0
    pixel = 0

    # Hiding the length of the extension in the red channel of the first pixel of the cover image
    cover_img[-1, -1] = [len(extension_bin), encode_msg[1], cover_img[-1, -1][2]]
    # Hiding the extension in the second to last bit of the cover image bits
    for ext in cover_img:
        for ext1 in ext:
            if ext_pos < len(extension_bin) and pixel != 0:
                ext1[0] = int(test(ext1[0])[:-2] + extension_bin[ext_pos] + test(ext1[0])[-1], 2)
                ext_pos += 1
            if ext_pos < len(extension_bin) and pixel != 0:
                ext1[1] = int(test(ext1[1])[:-2] + extension_bin[ext_pos] + test(ext1[1])[-1], 2)
                ext_pos += 1
            if ext_pos < len(extension_bin) and pixel != 0:
                ext1[2] = int(test(ext1[2])[:-2] + extension_bin[ext_pos] + test(ext1[2])[-1], 2)
                ext_pos += 1
            if ext_pos == len(extension_bin):
                break
            pixel += 1
    if pwd!='N/A':
     for pss in cover_img:
        for pss1 in pss:
            if pss_pos < len(pwd) and pixel != 0:
                pss1[0] = int(test(pss1[0])[:-3] + pwd[pss_pos] + test(pss1[0])[-2] + test(pss1[0])[-1], 2)
                pss_pos += 1
            if pss_pos < len(pwd) and pixel != 0:
                pss1[1] = int(test(pss1[1])[:-3] + pwd[pss_pos] + test(pss1[1])[-2] + test(pss1[1])[-1], 2)
                pss_pos += 1
            if pss_pos < len(pwd) and pixel != 0:
                pss1[2] = int(test(pss1[2])[:-3] + pwd[pss_pos] + test(pss1[2])[-2] + test(pss1[2])[-1], 2)
                pss_pos += 1
            if pss_pos == len(pwd):
                break
            pixel += 1

    for key_pos1 in cover_img:
        for key_pos2 in key_pos1:
            if key_pos < my_key_len and pixel != 0:
                key_pos2[0] = int(
                    test(key_pos2[0])[:-4] + my_key_bin[key_pos] + test(key_pos2[0])[-3] + test(key_pos2[0])[-2] +
                    test(key_pos2[0])[-1], 2)
                key_pos += 1
            if key_pos < my_key_len and pixel != 0:
                key_pos2[1] = int(
                    test(key_pos2[1])[:-4] + my_key_bin[key_pos] + test(key_pos2[1])[-3] + test(key_pos2[1])[-2] +
                    test(key_pos2[0])[-1], 2)
                key_pos += 1
            if key_pos < my_key_len and pixel != 0:
                key_pos2[2] = int(
                    test(key_pos2[2])[:-4] + my_key_bin[key_pos] + test(key_pos2[2])[-3] + test(key_pos2[2])[-2] +
                    test(key_pos2[0])[-1], 2)
                key_pos += 1
            if key_pos == my_key_len:
                break
            pixel += 1

    for cover_val in cover_img:
        for cover_val1 in cover_val:
            if msg_pos < len(temp_msg) and pixel != 0:
                cover_val1[0] = int(test(cover_val1[0])[:-1] + str(temp_msg[msg_pos]), 2)
                msg_pos += 1
            if msg_pos < len(temp_msg) and pixel != 0:
                cover_val1[1] = int(test(cover_val1[1])[:-1] + str(temp_msg[msg_pos]), 2)
                msg_pos += 1
            if msg_pos < len(temp_msg) and pixel != 0:
                cover_val1[2] = int(test(cover_val1[2])[:-1] + str(temp_msg[msg_pos]), 2)
                msg_pos += 1
            if msg_pos == len(temp_msg):
                cv.imwrite(output, cover_img)
                return 'end here'
            pixel += 1


def revert_img(img):
    img=cv.imread(img)
    t = fuck(img)
    if img[-2, -2][1] == 32:
        check = img[-2, -2][0]
        the_pass = 'N/A'
        pwd = 'NO'
        extension_len = img[-1, -1][0]
        packet_num = img[-1, -1][1]
        key_val_val = ''
        extension = ''
        key_val = ''
        key_cnt = 0
        pss_cnt = 0
        pss_val = ''
        extension_val = ''
        pixel = 0
        pss_val_val = ''
        cnt = 0

        for cover_val in img:
            for cover_val1 in cover_val:
                if cnt < extension_len and pixel != 0:
                    extension += test(cover_val1[0])[-2]
                    cnt += 1
                if cnt < extension_len and pixel != 0:
                    extension += test(cover_val1[1])[-2]
                    cnt += 1
                if cnt < extension_len and pixel != 0:
                    extension += test(cover_val1[2])[-2]
                    cnt += 1
                if cnt == extension_len:
                    print(extension)
                    break
                pixel += 1
            break

        for i in range(0, len(extension), 8):
            extension_val += chr(int(extension[i:i + 8], 2))
        print(f'The extension is {extension_val}')
        print(f'Recovering {packet_num} packets')

        for key in img:
            for key1 in key:
                if key_cnt < 352 and pixel != 0:
                    key_val += test(key1[0])[-4]
                    key_cnt += 1
                if key_cnt < 352 and pixel != 0:
                    key_val += test(key1[1])[-4]
                    key_cnt += 1
                if key_cnt < 352 and pixel != 0:
                    key_val += test(key1[2])[-4]
                    key_cnt += 1
                if key_cnt == 352:
                    break
                pixel += 1
            break

        for i in range(0, len(key_val), 8):
            key_val_val += chr(int(key_val[i:i + 8], 2))
        print(f'The public key is {key_val_val.encode()}')

        if check == 3:
            pwd = 'YES'
            for pss in img:
                for pss1 in pss:
                    if pss_cnt < img[-1,-1][2] and pixel != 0:
                        pss_val += test(pss1[0])[-3]
                        pss_cnt += 1
                    if pss_cnt < img[-1,-1][2] and pixel != 0:
                        pss_val += test(pss1[1])[-3]
                        pss_cnt += 1
                    if pss_cnt < img[-1,-1][2] and pixel != 0:
                        pss_val += test(pss1[2])[-3]
                        pss_cnt += 1
                    if pss_cnt == img[-1,-1][2]:
                        break
                    pixel += 1
                break

            for i in range(0, len(pss_val), 8):
                pss_val_val += chr(int(pss_val[i:i + 8], 2))
            print(f'The password is {pss_val_val}')
            the_pass = simpledialog.askstring(title='Password', prompt='Enter the password ').strip()
        return [pwd, pss_val_val, extension_val, key_val_val, packet_num, the_pass,t]
    else:
        return "NO HIDDEN FILE DETECTED"


def fuck(img):
    f = np.unpackbits(img)
    return np.array([f[i] for i in range(7, len(f), 8)])


def final_revert(fuck1,pss,ext,key_val,output):
    ln = 0

    for i in range(0, len(fuck1), 8):
        if np.array(fuck1[i:i + 8]).tobytes() == end_byte:
            if np.array(fuck1[i + 8:i + 16]).tobytes() == end_byte1:
                if np.array(fuck1[i + 16:i + 24]).tobytes() == end_byte2:
                    print('yes')
                    fuck1 = fuck1[:i]
                    ln += 1
                    break

    h = np.packbits(fuck1)
    h1 = h.tobytes()
    my_key = Fernet(key_val.encode())
    h1 = my_key.decrypt(h1)
    if pss!='N/A':
        with open(output + ext, 'wb') as file:
            file.write(h1)
            file.close()
        with open(output + '.txt', 'wb') as text:
            text.write('Here is your public key is '.encode())
            text.write(key_val.encode())
            text.write(f'\nYour Password is {pss}'.encode())
    elif pss=='N/A':
        with open(output + ext, 'wb') as file:
            file.write(h1)
            file.close()
        with open(output + '.txt', 'wb') as text:
            text.write('Your public key is '.encode())
            text.write(key_val.encode())
            text.write('\nNo Password Configured'.encode())


# return [c,pwd,extension_val,packet_num]
