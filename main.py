from variables import *

try:
    import crazy_spin_pvc
    try:
        del crazy_spin_pvc
    except NameError:
        pass
except KeyboardInterrupt:
    pass

raise KeyboardInterrupt
