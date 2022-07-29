from docarray import Document
from datetime import datetime
import math
import urllib
from urllib import request


server_url = 'grpcs://dalle-flow.dev.jina.ai'

prompt = input("Enter Request: ")

da = Document(text=prompt).post(server_url, parameters={'num_images': 8}).matches
da.plot_image_sprites(fig_size=(10, 10), show_index=True)
fav_id = int(input("Select an image to refine [0-15]: "))
fav = da[fav_id]
fav.display()
diffused = fav.post(f'{server_url}', parameters={'skip_rate': 0.3, 'num_images': 36},
                    target_executor='diffusion').matches
diffused.plot_image_sprites(fig_size=(10, 10), show_index=True)
dfav_id = int(input("Select an image to upscale: [0-7]: "))
fav = diffused[dfav_id]
print("Display Fav")
fav.display()
upscale = fav.post(f'{server_url}/upscale')
print("Display Upscale")
upscale.display()
timestamp = math.floor(datetime.timestamp(datetime.now()))
response = urllib.request.urlopen(upscale.uri)
with open(f"{timestamp}.png", 'wb') as f:
    f.write(response.file.read())
