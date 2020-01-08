
def launch(program):
    try:
        __import__(program)
        del program
    except NameError:
        print('Program '+program+' failed to import')
