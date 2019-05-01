from PIL import Image
import os
#(255,255,255) = empty space
#(0,0,0) = wall
#(0,255,0) = spawn

def imageStuff(image):
    im = Image.open(image)
    im = im.convert('RGB')
    bit = []
    width, height = im.size
    mapTemp = ["" for x in range(height)]
    spawnPos =[]
    for y1 in range(height):
        for x1 in range(width):
            col = im.getpixel((x1,y1))
            if col == (255,255,255):
                mapTemp[y1] += "0"
            elif col == (0,0,0):
                mapTemp[y1] += "1"
            else:
                mapTemp[y1]+= "0"
                spawnPos.append((x1*60, y1*60))
    bit.append(mapTemp)
    bit.append(spawnPos)          
    return bit

def getMaps():
    allMaps = []
    for root, dirs, files in os.walk("mapsRaw"):
        for file in files:
            allMaps.append(imageStuff("mapsRaw/"+file))
    return allMaps
