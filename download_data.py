try:
    from art import tprint

    tprint("ASL dataset downloader", font="slant")
except ImportError:
    print("ASL dataset downloader")

try:
    import kaggle
    
    kaggle.api.dataset_download_files("https://www.kaggle.com/datasets/grassknoted/asl-alphabet", path="data", unzip=True)
except IOError as e:
    if "Could not find kaggle.json." in str(e):
        print(f'{e}\nread "https://github.com/Kaggle/kaggle-api#api-credentials=" to learn how to set up API credentials.')
    else:
        raise e
else:
    print("Done!")

