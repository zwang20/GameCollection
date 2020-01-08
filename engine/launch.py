
def launch(program):
    # do not except NameErrors 
    __import__(program)
    del program
