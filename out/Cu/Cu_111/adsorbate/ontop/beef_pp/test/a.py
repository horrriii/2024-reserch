from ase.io import read, write
from ase.calculators.espresso import Espresso
from subprocess import run
from pathlib import Path
import os
from datetime import datetime
import shutil

# Settings ---------------------------------------------------------------------
calculation_id = int(os.environ["SLURM_ARRAY_TASK_ID"])

input_data = {
    "control": {
        "tprnfor": True,
    },
    "system": {
        "ecutwfc": 60,
        "ecutrho": 480,
        "occupations": "smearing",
        "smearing": "mp",
        "degauss": 0.01,
        "input_dft": "vdw-df2-b86r",
    },
    "electrons": {
        "electron_maxstep": 100,
        "conv_thr": 1.0e-09,
        "mixing_beta": 0.7,
        "mixing_mode": "plain",
        "diagonalization": "rmm-davidson",
    },
}

pseudopotentials = {
    "H": "h_pbe_v1.4.uspp.F.UPF",
    "B": "b_pbe_v1.4.uspp.F.UPF",
    "C": "c_pbe_v1.2.uspp.F.UPF",
    "O": "o_pbe_v1.2.uspp.F.UPF",
}

kpts = (4, 4, 1)


# Calculator -------------------------------------------------------------------
def get_calculator(label):
    return Espresso(
        input_data=input_data,
        pseudopotentials=pseudopotentials,
        kpts=kpts,
        label=label,
    )

# Logger -----------------------------------------------------------------------
def echo(*message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    messages = " ".join([str(m) for m in message])
    run(f'echo "{now} | {messages}" >> status.log', shell=True)
    run(f'echo "{now} | {messages}"', shell=True)


# Workflow ---------------------------------------------------------------------
# Select the structure to calculate
storage_directory = Path("structure_complexes")
selections = sorted([sdir for sdir in storage_directory.iterdir() if sdir.is_dir()])
selection = selections[calculation_id]


# Read the structures
files = sorted(list(selection.glob("*.traj")))

images = [read(f) for f in files]
names = [f.stem for f in files]
heights = [float(f.stem.split("_")[-1]) for f in files]

# Preapare directory
work_dir = Path("work_" + selection.stem)
work_dir.mkdir(exist_ok=True)
os.chdir(work_dir)

# Status report
echo("STARTING WORKFLOW ---")
echo("Selected:", selection)
echo("Files found:\n\t" + "\n\t".join(f.name for f in files))
echo("Entering work directory $(pwd)")

# Run calculation
echo("Starting calculations")
echo("Name, Height, Energy")
best_energy = 0
for i, (img, name, height) in enumerate(zip(images, names, heights)):
    img.calc = get_calculator(name)
    energy = img.get_potential_energy()
    echo(f"Image {i} : {name} {height} {energy:.6f}")
    
    if energy < best_energy:
        best_energy = energy
    else:
        break


# Clean up
shutil.rmtree(os.environ["ESPRESSO_TMPDIR"])
echo("FINISHED WORKFLOW ---")



