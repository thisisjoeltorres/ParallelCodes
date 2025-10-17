# MPI in C++

## Installation

Install Open MPI on your system:
- Ubuntu/Debian: `sudo apt-get install openmpi-bin libopenmpi-dev`
- macOS: `brew install open-mpi`
- Windows: Download from https://www.microsoft.com/en-us/download/details.aspx?id=57467

## Compilation

```bash
mpic++ -o hello_mpi hello_mpi.cpp
```

## Running

```bash
mpirun -np 4 ./hello_mpi
```

Where `-np 4` specifies the number of processes to run.
