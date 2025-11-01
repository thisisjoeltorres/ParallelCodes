from mpi4py import MPI
import os
import psutil
import json

def cluster_job():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Información del entorno
    job_id = os.getenv('SLURM_JOB_ID', 'Local')
    node_name = os.getenv('HOSTNAME', 'localhost')

    # --- MONITORIZACIÓN DE RECURSOS INICIAL ---
    process = psutil.Process(os.getpid())
    cpu_start = psutil.cpu_percent(interval=None)
    mem_start = process.memory_info().rss / (1024 ** 2)

    start_time = MPI.Wtime()

    # --- SIMULACIÓN DE CÁLCULO --- (Simulamos una suma parcial)
    local_sum = sum(i for i in range(rank * 1_000_000, (rank + 1) * 1_000_000))

    # --- MONITORIZACIÓN DE RECURSOS FINAL ---
    cpu_end = psutil.cpu_percent(interval=None)
    mem_end = process.memory_info().rss / (1024 ** 2)
    end_time = MPI.Wtime()
    elapsed = end_time - start_time

    # --- SIMULACIÓN DE SISTEMA DE ARCHIVOS PARALELOS --- 
    # (Aca es donde se guardan los archivos de acuerdo a sus respectivos rangos)

    output_dir = "parallel_output"
    os.makedirs(output_dir, exist_ok=True)
    local_file = os.path.join(output_dir, f"rank_{rank}.json")

    # Guardar resultados parciales de cada proceso
    data = {
        "rank": rank,
        "node": node_name,
        "local_sum": local_sum,
        "cpu_usage": f"{cpu_end:.2f}%",
        "mem_usage_MB": round(mem_end, 2),
        "elapsed_s": round(elapsed, 4),
    }
    with open(local_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[Proceso {rank}] Nodo={node_name} | CPU={cpu_end:.1f}% | MEM={mem_end:.2f}MB | Tiempo={elapsed:.4f}s")

    # --- REDUCCIÓN GLOBAL (recolectar resultados) ---
    global_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

    if rank == 0:
        # Combinar los archivos locales simulando un sistema de archivos paralelo
        combined_data = []
        for r in range(size):
            path = os.path.join(output_dir, f"rank_{r}.json")
            with open(path, "r") as f:
                combined_data.append(json.load(f))

        combined_file = os.path.join(output_dir, "combined_results.json")
        with open(combined_file, "w") as f:
            json.dump({
                "job_id": job_id,
                "nodes": node_name,
                "processes": size,
                "total_sum": global_sum,
                "details": combined_data
            }, f, indent=2)

        print("\n=== RESULTADOS GLOBALES ===")
        print(f"Trabajo: {job_id}")
        print(f"Procesos: {size}")
        print(f"Suma total: {global_sum}")
        print(f"Datos combinados guardados en: {combined_file}")

if __name__ == "__main__":
    cluster_job()
