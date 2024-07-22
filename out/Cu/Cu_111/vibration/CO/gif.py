from ase.io import read, write
from ase.io import Trajectory

co = Trajectory("vib.5.traj")
write("co.gif", co[::5], rotation="0x,90y,0z") # type: ignore
