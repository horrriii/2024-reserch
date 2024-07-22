from ase.io import read, write
from ase.io import Trajectory

co = Trajectory("vib.32.traj")
write("1layer2.gif", co[::5], rotation="0x,0y,0z") # type: ignore
