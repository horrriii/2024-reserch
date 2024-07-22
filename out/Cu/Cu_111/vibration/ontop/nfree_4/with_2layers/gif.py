from ase.io import read, write
from ase.io import Trajectory

co = Trajectory("vib.59.traj")
write("2layer1.gif", co[::5], rotation="90x,0y,180z") # type: ignore
