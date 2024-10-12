#
# IonQ, Inc., Copyright (c) 2024,
# All rights reserved.
# Use in source and binary forms of this software, without modification,
# is permitted solely for the purpose of activities associated with the IonQ
# chalenge of hackathon hosted by SCQ only during the October 10-13, 2024 
# duration of such event.
#
import numpy as np
import symengine as symeng

from math import ceil, log
from ionqvision.ansatze import VariationalAnsatz
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterExpression, ParameterVector
from qiskit.quantum_info import SparsePauliOp




class AngleEncoderX(VariationalAnsatz):
    """
    Implement a quantum circuit for higher-order sparse angle encoding, specifically for rotating around the X direction.

    INPUT:

        - ``num_qubits`` -- number of qubits
        - ``entanglement_depth`` -- (optional) number layers of entangling CNOT
          gates: for each ``k`` in ``range(entanglement_depth)``, use gates
          ``CNOT(j, j + k + 1)``.
        - ``param_prefix`` -- (optional) string prefix for named circuit
          parameters
        - NOTE: xi denotes the parameter vector being used (this will be the same for all directions)

    EXAMPLES::

        >>> from ionqvision.ansatze.ansatz_library import AngleEncoder
        >>> ansatz = AngleEncoder(4, entanglement_depth=3, param_prefix="y")
        >>> ansatz.draw()
             ┌────────────┐                              
        q_0: ┤ Rx(π*y[0]) ├──■──────────────■─────────■──
             ├────────────┤┌─┴─┐            │         │  
        q_1: ┤ Rx(π*y[1]) ├┤ X ├──■─────────┼────■────┼──
             ├────────────┤└───┘┌─┴─┐     ┌─┴─┐  │    │  
        q_2: ┤ Rx(π*y[2]) ├─────┤ X ├──■──┤ X ├──┼────┼──
             ├────────────┤     └───┘┌─┴─┐└───┘┌─┴─┐┌─┴─┐
        q_3: ┤ Rx(π*y[3]) ├──────────┤ X ├─────┤ X ├┤ X ├
             └────────────┘          └───┘     └───┘└───┘
    """
    def __init__(self, num_qubits, entanglement_depth=1, param_prefix="x"):
        super().__init__(num_qubits)

        x = ParameterVector(param_prefix, num_qubits)
        [self.rx(np.pi * xi, qbt) for qbt, xi in enumerate(x)] 

        for k in range(entanglement_depth):
            top_qubit = 0
            while top_qubit < num_qubits - (k + 1):
                self.cx(top_qubit, top_qubit + k + 1)
                top_qubit += 1


class AngleEncoderY(VariationalAnsatz):
    """
    Implement a quantum circuit for higher-order sparse angle encoding, specifically for rotating around the Y direction.

    INPUT:

        - ``num_qubits`` -- number of qubits
        - ``entanglement_depth`` -- (optional) number layers of entangling CNOT
          gates: for each ``k`` in ``range(entanglement_depth)``, use gates
          ``CNOT(j, j + k + 1)``.
        - ``param_prefix`` -- (optional) string prefix for named circuit
          parameters
        - NOTE: xi denotes the parameter vector being used (this will be the same for all directions)

    EXAMPLES::

        >>> from ionqvision.ansatze.ansatz_library import AngleEncoder
        >>> ansatz = AngleEncoder(4, entanglement_depth=3, param_prefix="y")
        >>> ansatz.draw()
             ┌────────────┐                              
        q_0: ┤ Ry(π*y[0]) ├──■──────────────■─────────■──
             ├────────────┤┌─┴─┐            │         │  
        q_1: ┤ Ry(π*y[1]) ├┤ X ├──■─────────┼────■────┼──
             ├────────────┤└───┘┌─┴─┐     ┌─┴─┐  │    │  
        q_2: ┤ Ry(π*y[2]) ├─────┤ X ├──■──┤ X ├──┼────┼──
             ├────────────┤     └───┘┌─┴─┐└───┘┌─┴─┐┌─┴─┐
        q_3: ┤ Ry(π*y[3]) ├──────────┤ X ├─────┤ X ├┤ X ├
             └────────────┘          └───┘     └───┘└───┘
    """
    def __init__(self, num_qubits, entanglement_depth=1, param_prefix="x"):
        super().__init__(num_qubits)

        x = ParameterVector(param_prefix, num_qubits)
        [self.ry(np.pi * xi, qbt) for qbt, xi in enumerate(x)] 

        for k in range(entanglement_depth):
            top_qubit = 0
            while top_qubit < num_qubits - (k + 1):
                self.cx(top_qubit, top_qubit + k + 1)
                top_qubit += 1

class AngleEncoderZ(VariationalAnsatz):
    """
    Implement a quantum circuit for higher-order sparse angle encoding, specifically for rotating around the Z direction.

    INPUT:

        - ``num_qubits`` -- number of qubits
        - ``entanglement_depth`` -- (optional) number layers of entangling CNOT
          gates: for each ``k`` in ``range(entanglement_depth)``, use gates
          ``CNOT(j, j + k + 1)``.
        - ``param_prefix`` -- (optional) string prefix for named circuit
          parameters
        - NOTE: xi denotes the parameter vector being used (this will be the same for all directions)

    EXAMPLES::

        >>> from ionqvision.ansatze.ansatz_library import AngleEncoder
        >>> ansatz = AngleEncoder(4, entanglement_depth=3, param_prefix="y")
        >>> ansatz.draw()
             ┌────────────┐                              
        q_0: ┤ Rz(π*y[0]) ├──■──────────────■─────────■──
             ├────────────┤┌─┴─┐            │         │  
        q_1: ┤ Rz(π*y[1]) ├┤ X ├──■─────────┼────■────┼──
             ├────────────┤└───┘┌─┴─┐     ┌─┴─┐  │    │  
        q_2: ┤ Rz(π*y[2]) ├─────┤ X ├──■──┤ X ├──┼────┼──
             ├────────────┤     └───┘┌─┴─┐└───┘┌─┴─┐┌─┴─┐
        q_3: ┤ Rz(π*y[3]) ├──────────┤ X ├─────┤ X ├┤ X ├
             └────────────┘          └───┘     └───┘└───┘
    """
    def __init__(self, num_qubits, entanglement_depth=1, param_prefix="x"):
        super().__init__(num_qubits)

        x = ParameterVector(param_prefix, num_qubits)
        [self.rz(np.pi * xi, qbt) for qbt, xi in enumerate(x)]

        for k in range(entanglement_depth):
            top_qubit = 0
            while top_qubit < num_qubits - (k + 1):
                self.cx(top_qubit, top_qubit + k + 1)
                top_qubit += 1