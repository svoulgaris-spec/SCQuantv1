import numpy as np
import symengine as symeng
from scipy.linalg import expm

from math import ceil, log
from ionqvision.ansatze import VariationalAnsatz
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression, ParameterVector
from qiskit.quantum_info import SparsePauliOp, Operator


class ButterflyOrthogonalAnsatz(VariationalAnsatz):
    def __init__(self, num_qubits, param_prefix="θ"):
        """
        Construct the so-called "Butterfly" orthogonal quantum layer as
        illustrated in Fig. 8 of "Quantum Vision Transformers" by Cherrat et al.

        :EXAMPLE:

            >>> from ionqvision.ansatze.ansatz_library import ButterflyOrthogonalAnsatz
            >>> ansatz = ButterflyOrthogonalAnsatz(4)
            >>> ansatz.draw()
                 ┌────────────┐               ░ ┌────────────┐ ░ 
            q_0: ┤0           ├───────────────░─┤0           ├─░─
                 │            │┌────────────┐ ░ │  RBS(θ[2]) │ ░ 
            q_1: ┤  RBS(θ[0]) ├┤0           ├─░─┤1           ├─░─
                 │            ││            │ ░ ├────────────┤ ░ 
            q_2: ┤1           ├┤  RBS(θ[1]) ├─░─┤0           ├─░─
                 └────────────┘│            │ ░ │  RBS(θ[3]) │ ░ 
            q_3: ──────────────┤1           ├─░─┤1           ├─░─
                               └────────────┘ ░ └────────────┘ ░ 
        """
        d = int(log(num_qubits, 2))
        if abs(log(num_qubits, 2) - d) > 1e-8:
            raise ValueError("num_qubits nums be a power of 2")

        I = np.array([[1, 0], [0, 1]], dtype=complex)  # Identity matrix
        X = np.array([[0, 1], [1, 0]], dtype=complex)  # Pauli-X matrix
        Y = np.array([[0, -1j], [1j, 0]], dtype=complex)  # Pauli-Y matrix
        Z = np.array([[1, 0], [0, -1]], dtype=complex)  # Pauli-Z matrix
        H1 = np.kron(np.kron(np.kron(X, I), I), I)
        H2 = np.kron(np.kron(np.kron(Y, I), I), I)
        H3 = np.kron(np.kron(np.kron(Z, I), I), I)

        super().__init__(num_qubits)
        theta = iter(ParameterVector(param_prefix, d * num_qubits//2))
        for depth in reversed(range(d)):
            for j in range(2**depth):
                for i in range(2**(d - depth - 1)):
                    offset = i*2**(depth + 1)
                    qubits = [offset + j, offset + j + 2**depth]
                    self.rbs(next(theta), *qubits)
                    self.append(self._evolve(H1, 1).to_instruction(), range(num_qubits))
                    self.append(self._evolve(H2, 1).to_instruction(), range(num_qubits))
                    self.append(self._evolve(H3, 1).to_instruction(), range(num_qubits))
            self.barrier()


    def _evolve(self, H, dt):
        """Evolve the state by Hamiltonian H over time dt."""
        U = Operator(expm(-1j * H * dt))  # Unitary operator
        return U
