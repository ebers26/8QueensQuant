from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter, ParameterVector
from qiskit.quantum_info import Pauli
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from operator import itemgetter
from scipy.optimize import minimize

G = nx.Graph()
G.add_edges_from([[0,3], [0,4], [1,3], [1,4], [2,3], [2,4]])
nx.draw(G, pos=nx.bipartite_layout(G, [0,1,2]))

#COST FUNCTION

def append_zz_term(qc, q1, q2, gamma):
    qc.cx(q1,q2)
    qc.rz(2*gamma, q2)
    qc.cx(q1, q2)  

def get_cost_operator_circuit(G, gamma):
    N = G.number_of_nodes()
    qc = QuantumCircuit(N,N)
    for i, j in G.edges():
        append_zz_term(qc, i, j, gamma)
    return qc

qc = get_cost_operator_circuit(G, np.pi / 3)
qc.draw()

#MIXER FUNCTION
def append_x_term(qc, q1, beta):
    qc.rx(2*beta, q1)

def get_mixer_operator_circuit(G, beta):
    N = G.number_of_nodes()
    qc = QuantumCircuit(N,N)
    for n in G.nodes():
        append_x_term(qc, n, beta)
    return qc

qc2 = get_mixer_operator_circuit(G, np.pi/3)
qc2.draw()

def get_qaoa_circuit(G, beta, gamma):
    assert(len(beta) == len(gamma))