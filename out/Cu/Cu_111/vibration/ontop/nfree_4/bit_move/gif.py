from ase.io import read, write
from ase.io import Trajectory

cu = read("Cux+.pwo")
write("x+.gif", cu[::5], rotation="0x,-90y,0z") # type: ignore
