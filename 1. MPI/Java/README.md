# MPI in Java

## Installation

1. Install Open MPI on your system
2. Download and install MPJ Express from: http://mpj-express.org/

## Compilation

```bash
javac -cp $MPJ_HOME/lib/mpj.jar HelloMPI.java
```

## Running

```bash
mpjrun.sh -np 4 HelloMPI
```

Where `-np 4` specifies the number of processes to run.
