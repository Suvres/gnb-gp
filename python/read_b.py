def read_b(x):
    if x < 1024:
        return "{0:.2f} B".format(x)
    elif x < (1024 * 1024):
        return "{0:.2f} KB".format(x/1024)
    elif x < (1024 * 1024 * 1024):
        return "{0:.2f} MB".format(x / (1024 * 1024))
    elif x < (1024 * 1024 * 1024 * 1024):
        return "{0:.2f} GB".format(x / (1024 * 1024 * 1024))

