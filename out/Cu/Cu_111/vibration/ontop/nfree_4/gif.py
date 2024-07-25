from ase.io import read, write
from ase.io import Trajectory

co = Trajectory("vib.1.traj")
write("ontop1.gif", co[::5], rotation="0x,0y,0z") # type: ignore
