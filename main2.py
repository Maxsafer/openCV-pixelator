from os import listdir
import numpy as np
import cv2
import sys

def inputImg():
  files = []
  counter = 0
  inv = 0
  print(f'Type inv after selection to invert black and white i.e. 13inv')
  print(f'{counter}. Exit')
  for file in listdir('./images'):
    if (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")) and file != 'output.jpg':
      counter += 1
      print(f'{counter}. {file}')
      files.append(file)
  chosen = input()
  if "inv" in chosen: inv = 1
  chosen = int(chosen.replace("inv",""))-1
  if chosen != -1: 
    inputName = f'{files[chosen]}'
    return [inputName, inv]
  else:
    sys.exit()

def generate_empty_image(bits, constant):
    return np.ones(shape=(bits * constant, bits * constant, 1), dtype=np.int16)

def toAscii(image, bits, w, h, inv, inString, border_size):
  inString = " " + inString
  if inv == False: 
    rangeX = "<= 127"
  else:
    rangeX = ">= 127"

  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  canvas_width = image.shape[1] + 2 * border_size
  canvas_height = image.shape[0] + 2 * border_size
  canvas = np.zeros((canvas_height, canvas_width), dtype=np.uint8)
  x_offset = border_size
  y_offset = border_size
  canvas[y_offset:y_offset+image.shape[0], x_offset:x_offset+image.shape[1]] = image
  image = cv2.resize(canvas, (bits, bits), interpolation=cv2.INTER_AREA)
  # cv2.imwrite('bordered_image.jpg', image)
  imascii = []

  constant = 15

  genimg = generate_empty_image(bits, constant)
  inputCounter = 0
  
  for row in range(0, bits):
    imascii.append([])
    for column in range(0, bits):
      color = image[row, column]
      if eval(f"{color} {rangeX}") and (inString[inputCounter] == " " or inString[inputCounter] == "\n"): imascii[row].append(" ")
      else: 
        imascii[row].append((inString[inputCounter]).replace("\n"," "))
        if len(inString)-1 == inputCounter:
          imascii[row].append(" ")
          inputCounter = 0
        else:
          inputCounter += 1
  
  file1 = open("text-output.txt", "w")

  for i in range(bits):
    file1.write('\n')
    for j in range(bits):
      file1.write(imascii[i][j])
      cv2.putText(img=genimg, text=f'{imascii[i][j]}', org=(j * constant, (i * constant) + 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=.5, color=(255),thickness=2)
  
  file1.close()
  cv2.imwrite('output2.jpg', genimg)
  
def imageWriter(bits, inString, border_size):
  selectImg = inputImg()
  input = cv2.imread(f'./images/{selectImg[0]}')
  
  # Get input size
  height, width = input.shape[:2]
  
  # Resize input to "pixelated"
  temp = cv2.resize(input, (bits, bits), interpolation=cv2.INTER_AREA)
  
  toAscii(temp, bits, width, height, selectImg[1], inString, border_size)
  
  # Initialize output image
  output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
  
  cv2.imwrite('output.jpg', output)
  print('')
  print('__________________')
  
if __name__ == '__main__':
  border_size = 10
  min_size = 7

  with open('text-input.txt') as f:
    inString = " ".join(f.readlines())

  for x in range(min_size, 32):
    if ((2 ** x) * (2 ** x)) > len(inString):  
      bits = 2 ** x # overshoots the space for it to fit the whole text and the restarts from the begining to fill the whole picture
      break
    
  while True:
    imageWriter(bits, inString, border_size)