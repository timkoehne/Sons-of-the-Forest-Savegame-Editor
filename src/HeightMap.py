from Misc import *
import png
import math
from scipy import interpolate
import numpy as np
from Misc import *

FILEPATH = "../res/heightmap.png"

class HeightMap:
    
    MINHEIGHT = 0
    MAXHEIGHT = 750
    HEIGHTDIFF = MAXHEIGHT - MINHEIGHT
    BITDEPTH = 16
    
    def __init__(self):
        
        pngdata = png.Reader(FILEPATH).read_flat()
        self.heightmapImg = np.array(pngdata[2]).reshape((pngdata[1], pngdata[0], -1))
        
    def getHeight(self, ingamePos) -> float:
        bboxMap = (0, 0, MAPIMAGESIZE, MAPIMAGESIZE)
        pixelPos = transformCoordinatesystemToImage(ingamePos, bboxMap)
        height = (self.heightmapImg[pixelPos[0]][pixelPos[1]][0] / pow(2,HeightMap.BITDEPTH) * HeightMap.HEIGHTDIFF) + HeightMap.MINHEIGHT
        return height
        
    def generateHeightmap(heightData, interpolationMethod):
            bbox = (0, 0, MAPIMAGESIZE, MAPIMAGESIZE)
        
            # # cant really use data dependent min and max
            # # because thats not saved inside the image
            minHeight = min(heightData, key=lambda value: value[1])[1]
            maxHeight = max(heightData, key=lambda value: value[1])[1]
            print("min y in data", minHeight)
            print("max y in data", maxHeight)
            
            #convert ingame positions to pixel positions
            for pos in heightData:
                x, y = transformCoordinatesystemToImage((pos[0], pos[2]), bbox)
                pos[0], pos[2] = x, y
                col = (((pos[1] - HeightMap.MINHEIGHT) / (HeightMap.HEIGHTDIFF)) * pow(2,HeightMap.BITDEPTH))
                pos[1] = col
                # print(f"pixel {int(x)}, {int(y)} has the color {col}")
            
            #add border values
            #assuming the water at the map border is at height = HeightMap.MINHEIGHT
            for x in range(0, MAPIMAGESIZE):
                for y in range(0, MAPIMAGESIZE):
                    if x == 0 or y == 0 or x == MAPIMAGESIZE-1 or y ==MAPIMAGESIZE-1:
                        heightData.append([x, HeightMap.MINHEIGHT, y])
            
            #interpolate missing data
            xArr = [pos[0] for pos in heightData]
            yArr = [pos[1] for pos in heightData]
            zArr = [pos[2] for pos in heightData]
            
            x = np.arange(0, MAPIMAGESIZE)
            y = np.arange(HeightMap.MINHEIGHT, HeightMap.MAXHEIGHT)
            z = np.arange(0, MAPIMAGESIZE)
            X, Z = np.meshgrid(x, z)
            
            heightMapArr = interpolate.griddata((xArr, zArr), yArr, (X, Z), method=interpolationMethod)
            heightMapArr = heightMapArr.astype(np.uint16)
            
            with open(FILEPATH, "wb") as file:
                w = png.Writer(MAPIMAGESIZE, MAPIMAGESIZE, greyscale=True, bitdepth=HeightMap.BITDEPTH)
                w.write(file, heightMapArr)