import startup

if __name__ == "__main__":
    token = startup.refresh()
    startup.get_top_tracks(token)
    
