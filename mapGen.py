#Copyright (c) 2019 Scott Blenkhorne
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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
    objectives = []
    for y1 in range(height):
        for x1 in range(width):
            col = im.getpixel((x1,y1))
            if col == (255,255,255):
                mapTemp[y1] += "0"
            elif col == (0,0,0):
                mapTemp[y1] += "1"
            elif col == (0,255,0):
                mapTemp[y1]+= "0"
                spawnPos.append((x1*60, y1*60))
            elif col == (0,0, 255):
                mapTemp[y1]+= "3"
            else:
                mapTemp[y1] += "2"
    bit.append(mapTemp)
    bit.append(spawnPos)          
    return bit

def getMap(challenge):
    return [imageStuff("mapsTraining/Challenge"+str(challenge)+".png")]

def getMaps():
    allMaps = []
    for root, dirs, files in os.walk("mapsRaw"):
        for file in files:
            if file[-3:] == "png":
                allMaps.append(imageStuff("mapsRaw/"+file))
    return allMaps
