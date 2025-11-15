import sys, os
import csv
import time

from qiskit import BasicAer, execute

# ------------------- BACKEND ------------------------
backend = BasicAer.get_backend("dm_simulator")

options = {
    'plot': False,
    'show_partition': False,
    "decoherence_factor": 0.9,
    "depolarization_factor": 0.9,
}

# ------------------- PATH SETUP ---------------------
cd = os.path.abspath(os.path.join(os.path.dirname("qsim-superstaq"), '..'))

sys.path.insert(0, os.path.join(cd, 'supermarq-benchmarks/supermarq/benchmarks'))
sys.path.insert(0, os.path.join(cd, 'supermarq-benchmarks/supermarq'))
sys.path.insert(0, os.path.join(cd, 'supermarq-benchmarks'))

from converters import *
from benchmarks import (
    GHZ,
    HamiltonianSimulation,
    MerminBell,
    QAOAFermionicSwapProxy,
    QAOAVanillaProxy,
)


# ============================================================
# FUNCTION TO RUN A SINGLE BENCHMARK FOR A GIVEN QUBIT SIZE
# ============================================================
def run_single(benchmark_class, qubits, shots, benchmark_title):
    benchmark_obj = benchmark_class(qubits)

    # -------- Creation time --------
    t_c = time.time()
    qc = benchmark_obj.qiskit_circuit()
    creation_time = time.time() - t_c

    # -------- Execution time --------
    t_e = time.time()
    job = execute(qc, backend, shots=shots, **options)
    result = job.result()
    execution_time = time.time() - t_e

    # -------- Quantum processing time --------
    quantum_time = result.time_taken

    # -------- Convert probabilities to integer counts --------
    counts = result.results[0].data.partial_probability
    for key in counts:
        counts[key] = int(counts[key] * shots)

    # -------- Score --------
    score = benchmark_obj.score(counts)

    # -------- Benchmark name (Example: GHZ-8) --------
    benchmark_name = f"{benchmark_title}-{qubits}"

    return {
        "num_qubits": qubits,
        "creation_time": creation_time,
        "execution_time": execution_time,
        "quantum_time": quantum_time,
        "score": score,
        "benchmark_name": benchmark_name
    }


# ============================================================
# FUNCTION TO RUN FULL RANGE AND SAVE AFTER EACH ITERATION
# ============================================================
def run_benchmark_range(benchmark_class, benchmark_title, min_qubits, max_qubits, shots):
    csv_filename = f"{benchmark_title}.csv"

    headers = ["num_qubits", "creation_time", "execution_time",
               "quantum_time", "score", "benchmark_name"]

    # -------- Create CSV with header if not exists --------
    if not os.path.exists(csv_filename):
        with open(csv_filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

    print(f"\n===== Running {benchmark_title} from {min_qubits} to {max_qubits} qubits =====")

    for q in range(min_qubits, max_qubits + 1):
        try:
            result_row = run_single(benchmark_class, q, shots, benchmark_title)

            # -------- Write this row immediately to CSV --------
            with open(csv_filename, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writerow(result_row)

            print(f"✔ Saved results of {benchmark_title} at {q} qubits")

        except Exception as e:
            print(f"✘ Failed for qubits = {q}: {e}")

    print(f"📁 Completed {benchmark_title}, saved in {csv_filename}")


# ============================================================
# MAIN — RUN ALL BENCHMARKS TOGETHER
# ============================================================
if __name__ == "__main__":

    min_qubits = 3
    max_qubits = 14
    shots = 1000

    benchmark_list = [
        (GHZ, "GHZ"),
        (HamiltonianSimulation, "HamiltonianSimulation"),
        (MerminBell, "MerminBell"),
        (QAOAFermionicSwapProxy, "QAOAFermionicSwapProxy"),
        (QAOAVanillaProxy, "QAOAVanillaProxy"),
    ]

    for benchmark_class, benchmark_title in benchmark_list:
        run_benchmark_range(
            benchmark_class,
            benchmark_title,
            min_qubits,
            max_qubits,
            shots
        )

    print("\n🎉 ALL BENCHMARKS COMPLETED SUCCESSFULLY!")
