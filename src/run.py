import startup
import requests
import os
from PIL import Image
from io import BytesIO

def generate_background(covers):
    images = []
    
    for cover in covers:
        r = requests.get(cover["url"])
        i = Image.open(BytesIO(r.content))
        images.append(i)
    wallpaper_width = 1920
    wallpaper_height = 1080


    wallpaper = Image.new('RGB', (wallpaper_width, wallpaper_height), color='black')
    cols = 5
    rows = 2
    
    size = wallpaper_width//cols
    padding = (wallpaper_height - (size * 2)) // 2
    
    
    #156 pixels of padding on top and bottom
    for i, img in enumerate(images):
        img = img.resize((size, size))

        col = i % cols
        row = i % rows

        y_pos = padding + (size * row)
        x_pos = size * col

        wallpaper.paste(img, (x_pos, y_pos))
    wallpaper.save('generated_wallpaper.jpg')


if __name__ == "__main__":
    token = startup.refresh()
    data = startup.get_top_tracks(token)
    items = data["items"]

    albums = set()
    covers = []
    nxt = data["next"]
    limit = data["limit"]
    page = 0
    n = 0
    i = 0

    while n < 10:
        item = items[i]
        album = item["album"]["id"]

        if album in albums:
            i += 1
            if i >= limit:
                data = json.loads(requests.get(nxt).text)
                items = data["items"]
                i = 0
            continue
        else:
            albums.add(album)
            covers.append(item["album"]["images"][0])
            i += 1
            if i >= limit:
                data = json.loads(requests.get(nxt).text)
                items = data["items"]
                i = 0
            n += 1

        generate_background(covers) 



        
