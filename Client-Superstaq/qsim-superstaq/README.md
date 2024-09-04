## About :

This is the implementation Supermarq Benchmarks with **QSIM** *(qctoolkit.in)*. QSIM is Qiskit's BasicAer version of **dm_simulator** (Density matrix simulator).
For the repository of this dm_simulator please go through [Qiskit-Aakash](https://github.com/indian-institute-of-science-qc/qiskit-aakash/tree/terra_upgrade).

The **.ipynb** file present in this directory consists of QSIM implementations of all the example benchmarks provided by **SupermarQ**. There is no requirement for installing Supermarq or any other dependencies except for the installation process given below.

- We have been directly importing all the modules from the repository itself.

A **run** function is created to perform execution of example benchmarks provided by **supermarq** (except for **VQEProxy**, **Bitcode** and **Phasecode**). 

- VQEProxy is executed independent of the **run** function in seperate cell of **.ipynb** file.
- Implementation of **Bitcode** and **Phasecode** are **yet to be done**.

## Installation :

Please follow the below procedure for installing required essentials to run the benchmarking Programs. Make sure that you have already installed anaconda in your device.

**Step-1 :** Creating virtual environment.

```bash
conda create -n QiskitAakash python=3.8.19

conda activate QiskitAakash
```
The above step creates new anaconda environment with name **QiskitAakash** and activates it. Now you can go for next steps!!!

**Step-2 :** Clone the repository 
```bash
git clone -b terra_upgrade https://github.com/indian-institute-of-science-qc/qiskit-aakash.git
```
This will download a folder with the name of **qiskit-aakash**.

**Step-3 :** Go to the specified hash-id:
```bash
cd qiskit-aakash
git checkout -b dmsim bea98fbff86c234c0b1990add17493a1e86917cb
git log -n1
```
**Step-4 :** Installation of requirements :
Install ipython-genutils :
```bash
python -m pip install ipython-genutils
```
or
```bash
conda install -c conda-forge ipython_genutils
```
Install rustup :
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
python -m pip install setuptools-rust
```

Install requirements : If you want to run tests or linting checks, install the developer requirements.
```bash
pip install -r requirements-dev.txt
```

**Step-5 :** Installing **Qiskit** from the repository of **Qiskit-Aakash**

```bash
pip install numpy matplotlib notebook openpyxl pandas cirq
pip install .
```

These commands install compatible versions of required modules. Make sure to use these versions, because other versions might not be compatible with these programs.

All the installation procedure is completed !!!