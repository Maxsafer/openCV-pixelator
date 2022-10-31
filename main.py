from os import listdir
import cv2
import sys

def inputImg():
  files = []
  counter = 0
  print(f'{counter}. Exit')
  for file in listdir('./images'):
    if (file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")) and file != 'output.jpg':
      counter += 1
      print(f'{counter}. {file}')
      files.append(file)
  chosen = int(input())-1
  if chosen != -1: 
    inputName = f'{files[chosen]}'
    return inputName
  else:
    sys.exit()

def imageWriter(bits):
  input = cv2.imread(f'./images/{inputImg()}')
  
  # Get input size
  height, width = input.shape[:2]
  
  # Resize input to "pixelated" size (w, h)
  temp = cv2.resize(input, (bits, bits), interpolation=cv2.INTER_AREA)
  
  # Initialize output image
  output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
  
  cv2.imwrite('output.jpg', output)
  print('__________________')
  
if __name__ == '__main__':
  while True:
    bits = 23
    imageWriter(bits)