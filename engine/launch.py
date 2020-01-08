
def launch(program):
    try:
        __import__(program)
        del program
    except NameError:
        print('Program '+game+' failed to import')
