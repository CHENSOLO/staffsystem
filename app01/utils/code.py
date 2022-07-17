from PIL import Image
from numpy import size

img = Image.new(mode='RGB',size=(120,30),color=(255,255,255))

# 在图片查看器中打开
# img.show()

# 保存在本地
with open('code.png','wb') as f:
    img.save(f,format='png')