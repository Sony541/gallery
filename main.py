import os, json, codecs
from PIL import Image, ImageDraw
location = os.path.expanduser("D:\\Фотографии\\Сканер\\Чемодан фото\\bujh\\")


names_hor = [
]

names_vert = [
"Фото.002.jpg",
"Фото.003.jpg",
"Фото.004.jpg",
"Фото.005.jpg",
"Фото.009.jpg",
"Фото.010.jpg",
"Фото.015.jpg",
"Фото.016.jpg",
"Фото.033.jpg",
"Фото.034.jpg",
"Фото.039.jpg",
"Фото.040.jpg",
"Фото.045.jpg",
"Фото.046.jpg",
"Фото.056.jpg",
"Фото.057.jpg",
"Фото.061.jpg",
"Фото.062.jpg",
"Фото.130.jpg",
"Фото.131.jpg",
"Фото.137.jpg",
"Фото.138.jpg",
"Фото.143.jpg",
"Фото.144.jpg",
"Фото.145.jpg",
"Фото.146.jpg",
"Фото.147.jpg",
"Фото.148.jpg",
"Фото.163.jpg",
"Фото.164.jpg",
"Фото.169.jpg",
"Фото.170.jpg",
"Фото.171.jpg",
"Фото.172.jpg",
"Фото.187.jpg",
"Фото.188.jpg",
"Фото.191.jpg",
"Фото.192.jpg",
"Фото.195.jpg",
"Фото.196.jpg",
"Фото.200.jpg",
"Фото.201.jpg",
"Фото.202.jpg",
"Фото.203.jpg",
"Фото.220.jpg",
"Фото.221.jpg",
"Фото.222.jpg",
"Фото.223.jpg",
"Фото.226.jpg",
"Фото.227.jpg",
"Фото.232.jpg",
"Фото.233.jpg",
"Фото.252.jpg",
"Фото.253.jpg",
"Фото.258.jpg",
"Фото.259.jpg",
"Фото.265.jpg",
"Фото.266.jpg",
"Фото.286.jpg",
"Фото.287.jpg",
"Фото.289.jpg",
"Фото.290.jpg",
"Фото.296.jpg",
"Фото.297.jpg",
"Фото.301.jpg",
"Фото.302.jpg",
"Фото.303.jpg",
"Фото.304.jpg",
"Фото.305.jpg",
"Фото.306.jpg"
]

def top_bot(arr):
    cnt = 0
    while (cnt + 1 < len(arr)):
        im1 = Image.open(arr[cnt])
        w1 = im1.size[0]
        h1 = im1.size[1]
        pix1 = im1.load()

        im2 = Image.open(arr[cnt + 1])
        w2 = im2.size[0]
        h2 = im2.size[1]
        pix2 = im2.load()

        wf = w1
        hf = h1 + h2
        if (w2 > w1): wf = w2

        imf = Image.new('RGB', (wf, hf))

        draw = ImageDraw.Draw(imf)

        for i in range(w1):
            for j in range(h1):
                p = pix1[i, j]
                draw.point((i, j), p)

        for i in range(w2):
            for j in range(h2):
                p = pix2[i, j]
                draw.point((i, h1 + j), p)

        imf.save(arr[cnt].replace(".jpg", "_m.jpg"), "JPEG")
        print(location)
        print(arr[cnt])
        os.rename(arr[cnt], arr[cnt].replace(location, location+"tmp\\"))
        os.rename(arr[cnt+1], arr[cnt+1].replace(location, location+"tmp\\"))
        del draw
        cnt += 2

def left_right(arr):
    cnt = 0
    while (cnt + 1 < len(arr)):
        im1 = Image.open(arr[cnt])
        w1 = im1.size[0]
        h1 = im1.size[1]
        pix1 = im1.load()

        im2 = Image.open(arr[cnt + 1])
        w2 = im2.size[0]
        h2 = im2.size[1]
        pix2 = im2.load()

        wf = w1 + w2
        hf = h1
        if (h2 > h1): hf = h2

        imf = Image.new('RGB', (wf, hf))

        draw = ImageDraw.Draw(imf)

        for i in range(w1):
            for j in range(h1):
                p = pix1[i, j]
                draw.point((i, j), p)

        for i in range(w2):
            for j in range(h2):
                p = pix2[i, j]
                draw.point((w1 + i, j), p)

        imf.save(arr[cnt].replace(".jpg", "_m.jpg"), "JPEG")
        print(location)
        print(arr[cnt])
        os.rename(arr[cnt], arr[cnt].replace(location, location+"tmp\\"))
        os.rename(arr[cnt+1], arr[cnt+1].replace(location, location+"tmp\\"))
        del draw
        cnt += 2

def main():
    arr_hor = [location + n for n in names_hor]
    arr_vert = [location + n for n in names_vert]
    #os.mkdir(location+"tmp")
    left_right(arr_hor)
    top_bot(arr_vert)

main()