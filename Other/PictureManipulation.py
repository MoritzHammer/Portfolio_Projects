from PIL import Image


class Convert:
    img_white = Image.open("ManipulationPictures/beautiful.jfif")  # open colour image
    fn = lambda x: 0 if x > 100 else 255
    r = img_white.convert('L').point(fn, mode='1')
    r.save('ManipulationPictures/black_white.png')

    img = Image.open('ManipulationPictures/black_white.png')
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save("ManipulationPictures/black_transparent.png", "PNG")

    jimg = Image.open('ManipulationPictures/beautiful.jfif')
    jimg = jimg.convert("RGBA")
    datas = jimg.getdata()

    newjData = []
    for item in datas:
        r = item[0] + 100
        g = item[1] - 50
        b = item[2] - 50
        newjData.append((r, g, b, 100))

    jimg.putdata(newjData)
    jimg.save("ManipulationPictures/red.png", "PNG")

