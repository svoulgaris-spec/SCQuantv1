from ionqvision.ansatze import VariationalAnsatz
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression, ParameterVector

class SU2Ansatz(VariationalAnsatz):
    """
    Implement a quantum circuit for higher-order sparse angle encoding.

    INPUT:

        - ``num_qubits`` -- number of qubits
        - ``param_prefix`` -- (optional) string prefix for named circuit
          parameters

    EXAMPLE:
        
        >>> numQ = 3
        >>> ansatz = SU2Ansatz(num_qubits=numQ)
        >>> ansatz.draw()
             ┌──────────┐┌──────────┐                  ┌──────────┐ ┌──────────┐     »
        q_0: ┤ Ry(θ[0]) ├┤ Rz(θ[3]) ├──────────■───────┤ Ry(θ[6]) ├─┤ Rz(θ[9]) ├─────»
             ├──────────┤├──────────┤        ┌─┴─┐     ├──────────┤┌┴──────────┤     »
        q_1: ┤ Ry(θ[1]) ├┤ Rz(θ[4]) ├──■─────┤ X ├─────┤ Ry(θ[7]) ├┤ Rz(θ[10]) ├──■──»
             ├──────────┤├──────────┤┌─┴─┐┌──┴───┴───┐┌┴──────────┤└───────────┘┌─┴─┐»
        q_2: ┤ Ry(θ[2]) ├┤ Rz(θ[5]) ├┤ X ├┤ Ry(θ[8]) ├┤ Rz(θ[11]) ├─────────────┤ X ├»
             └──────────┘└──────────┘└───┘└──────────┘└───────────┘             └───┘»
        «                  ┌───────────┐┌───────────┐
        «q_0: ──────■──────┤ Ry(θ[12]) ├┤ Rz(θ[15]) ├
        «         ┌─┴─┐    ├───────────┤├───────────┤
        «q_1: ────┤ X ├────┤ Ry(θ[13]) ├┤ Rz(θ[16]) ├
        «     ┌───┴───┴───┐├───────────┤└───────────┘
        «q_2: ┤ Ry(θ[14]) ├┤ Rz(θ[17]) ├─────────────
        «     └───────────┘└───────────┘             
            """
    
    def __init__(self, num_qubits, param_prefix="θ"):
        super().__init__(num_qubits)

        qubits = list(range(num_qubits))

        theta = iter(ParameterVector(param_prefix, 2*num_qubits**2))
        
        [self.ry(next(theta), qubit) for qubit in qubits]
        [self.rz(next(theta), qubit) for qubit in qubits]

        for j in range(0, num_qubits-1):
        
            for i in range(num_qubits-1, 0, -1):
                self.cx(qubits[i-1], qubits[i])
                
            [self.ry(next(theta), qubit) for qubit in qubits]
            [self.rz(next(theta), qubit) for qubit in qubits]