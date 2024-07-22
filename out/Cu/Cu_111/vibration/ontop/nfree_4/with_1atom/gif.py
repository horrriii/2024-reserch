from ase.io import read, write
from ase.io import Trajectory

co = Trajectory("vib.8.traj")
write("1atom2.gif", co[::5], rotation="-90x,0y,0z") # type: ignore
