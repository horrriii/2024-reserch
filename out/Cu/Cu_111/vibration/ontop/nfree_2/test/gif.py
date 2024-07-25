from ase.io import read, write
from ase.io import Trajectory

co = Trajectory("check.traj")
write("check.gif", co[::5], rotation="0x,0y,0z") # type: ignore
