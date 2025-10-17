# MPI in Python

## Installation

1. Install Open MPI on your system
2. Install mpi4py:

```bash
pip install mpi4py
```

## Running

```bash
mpirun -np 4 python hello_mpi.py
```

Where `-np 4` specifies the number of processes to run.
