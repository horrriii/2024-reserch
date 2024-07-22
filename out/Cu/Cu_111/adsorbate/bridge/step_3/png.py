from ase.io import read, write

atoms = read("Cu-650-7.6988415998004704.pwo", index=-1)
write("bridge.png", atoms, rotation="0x, 0y, 0z")
