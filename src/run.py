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

    cover_size = 640

    wallpaper = Image.new('RGB', (wallpaper_width, wallpaper_height), color='black')
    cols = 5
    rows = 2

    spacing_x = (wallpaper_width - cols * cover_size) // (cols + 1)
    spacing_y = (wallpaper_height - rows * cover_size) // (rows + 1)

    for i, img in enumerate(images):
        img = img.resize((cover_size, cover_size))

        col = i % cols
        row = i // cols

        x = spacing_x + col * (cover_size + spacing_x)
        y = spacing_y + row * (cover_size + spacing_y)

        wallpaper.paste(img, (x, y))

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



        
