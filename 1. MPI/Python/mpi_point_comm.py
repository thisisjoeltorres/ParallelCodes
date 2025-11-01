from mpi4py import MPI
import time

def ping_pong():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Se requieren al menos dos procesos
    if size < 2:
        if rank == 0:
            print("❗ Se necesitan al menos 2 procesos para ejecutar este programa.")
        return

    # Mensaje inicial
    message = {
        "data": "Mensaje de prueba",
        "timestamp": time.time(), # Estaremos cambiando esta parte del mensaje durante el ping-pong.
        "hop": 0 # Igualmente actualizaremos el ping-pong.
    }

    if rank == 0:
        # --- PROCESO 0: envía el mensaje ---
        start_time = time.time()
        comm.send(message, dest=1, tag=1)
        print(f"[P0] Enviado mensaje a P1")

        # --- Recibe la respuesta, solo se ejecuta cuando P1 responde --- 
        response = comm.recv(source=1, tag=2)
        end_time = time.time()

        print(f"[P0] Respuesta recibida desde P1: {response['data']}")
        print(f"[P0] Tiempo de ida y vuelta: {(end_time - start_time)*1000:.3f} ms")

    elif rank == 1:
        # --- PROCESO 1: recibe mensaje y responde ---
        received = comm.recv(source=0, tag=1)
        print(f"[P1] Recibido mensaje de P0: {received['data']}")

        # Actualiza el mensaje
        received['timestamp'] = time.time()
        received['hop'] += 1

        # Envía la respuesta al proceso 0
        comm.send(received, dest=0, tag=2)
        print(f"[P1] Enviada respuesta a P0")

if __name__ == "__main__":
    ping_pong()
