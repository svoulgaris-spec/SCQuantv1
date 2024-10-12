# The Quintum Quantum Classifier

## Introduction:
Quintum's presented solution to the IonQ Challenge at SCQuantathonv1 October 2024. 

IonQ Challenge: Our goal was to use quantum machine learning (QML) by using a hybrid model with classical pre- and post- processing with a quantum layer in between consisting of an encoder, ansatz, and quantum features. In our final solution, we tweaked the AngleEncoder to improve its performance, built the EfficientSU(2) ansatz we came across while researching the problem, and attempted to implement a Suzuki-Trotter circuit to make training more effecient through the use of time evolution.

## Submitted Files
- AngleEncoderRots.py: A library containing AngleEncoderX, AngleEncoderY, and AngleEncoderZ. All of them are the same base encoder for the quantum layer, with the difference being whether the X, Y, or Z axis rotation is applied to the qubits.
- QAOAnsatz.ipynb: This function calls the ansatz_library to use the QAOAAnsatz ansatz. It currently runs 8 bits and is run in a jupyter notebook. By clicking play, we can set up the quantum layer and train the model.  
- ansatz_library.py: A library containing AngleEncoder, BrickworkLayoutAnsatz, ButterflyOrthogonalAnsatz, CrossOrthogonalAnsatz, QAOAAnsatz, QCNAnsatz, and UnaryEncoder Ansatz. These functions can be attached to quantum circuits with qbits to to encode the quantum solution. 
- su2.py: This library implements the Efficient SU(2) ansatz using the existing IonQVision framework. This class can be called like any other function in the ansatz_library. While this class was not implemented in our final solution, we would like to see how it could integrated with the Suzuki-Trotter implementation
- trotter.py: This library implements an interweaving Butterfly Orthogonal ansatz with the Suzuki-Trotter circuit implementation. We would like to eventually implement an interweaving Suzuki-Trotter for other ansatzes.

## Key Concepts for Stacking the BOFT Ansatz with Suzuki-Trotter:
1. Ansatz: This refers to the parametric quantum circuit (like your Butterfly
Orthogonal Ansatz) that encodes your quantum solution. It remains as the
backbone structure of your quantum model.
2. Suzuki-Trotter decomposition: You apply the decomposition to simulate a
Hamiltonian evolution. This helps in breaking down the complex evolution into
smaller, more manageable operations.

The Suzuki-Trotter decomposition can be layered between or within the
parametric layers of the ansatz, specifically targeting the more complex unitary
operators or multi-qubit gates. 

## Incorporation Strategy:
1. Identify the Complex Interactions:
Within your Butterfly Orthogonal Ansatz, identify where complex unitary
operations or interactions between multiple qubits happen. These are
usually locations where the Trotter approximation would be useful to
simulate the dynamics more efficiently.
2. Apply Suzuki-Trotter to Complex Gates:
Instead of applying Suzuki-Trotter globally to the entire circuit, apply it
locally to the parts of the circuit where multi-qubit operations or
Hamiltonians (used to evolve states) are involved.
You split those operations using Suzuki-Trotter, simulating the evolution in
smaller steps.
3. Combine the Suzuki-Trotter Evolution with the Ansatz:
Layer Suzuki-Trotter steps either before or after the segments that
involve heavy interaction (like CNOT or controlled-U gates).

The decomposition acts as an improvement on specific parts, while the
rest of the ansatz remains unchanged.
Here’s a simplified Python-style pseudocode example to illustrate this approach:
```
def butterfly_ansatz(params, qubits):
  # Define your butterfly orthogonal ansatz here
  # Parametric layers with entangling gates and rotations
  for i in range(len(qubits)):
    apply_rotational_layer(params[i], qubits[i])
    apply_entangling_layer(qubits[i], qubits[i+1])
  return
def suzuki_trotter_hamiltonian_evolution(hamiltonian, qubits,
steps):
  # Decompose the Hamiltonian evolution using Suzuki-Trotter steps
  for _ in range(steps):
    for term in hamiltonian:
      apply_single_term_exp(term, qubits)
  return
def quantum_circuit_with_enhancement(params, qubits, hamiltonian, trotter_steps):
  # Start with the original ansatz
  butterfly_ansatz(params, qubits)
  # Apply Suzuki-Trotter decomposition as an enhancement suzuki_trotter_hamiltonian_evolution(hamiltonian, qubits, trotter_steps)
  
  # Continue with another layer of ansatz if needed
  butterfly_ansatz(params, qubits)
```
## Explanation:
1. butterfly_ansatz: This represents your original Butterfly Orthogonal Ansatz. It applies a series of parametric gates like rotational and entangling layers.
2. suzuki_trotter_hamiltonian_evolution: This applies the Suzuki-Trotter decomposition to simulate the Hamiltonian evolution on the selected qubits. It breaks down the Hamiltonian into simpler terms, applying the evolution in a series of steps to maintain accuracy.
3. quantum_circuit_with_enhancement: This combines both the original ansatz and the Suzuki-Trotter-enhanced simulation. The butterfly_ansatz runs first, followed by the Suzuki-Trotter decomposition, and then you can repeat the ansatz or add more layers as needed.

## Positioning Suzuki-Trotter:
1. Before the Ansatz: If you apply the decomposition before the ansatz, it would prepare the qubits by evolving them according to the Hamiltonian (complex interactions) before the variational layers of the ansatz are applied.
2. After the Ansatz: If you apply it after the ansatz, it further refines the state prepared by the ansatz, enhancing accuracy by evolving the state through the SuzukiTrotter decomposition.
3. Interleaved: You can also interleave the decomposition within the layers of your ansatz (between entangling or parametric layers). This approach allows the Suzuki-Trotter to affect only specific layers or sections of the ansatz where complex multi-qubit interactions happen.

## Next Steps:
- Hamiltonian Identification: Identify which Hamiltonian you're simulating in your quantum circuit. The Suzuki-Trotter decomposition approximates the time-evolution operator \( e^{iHt} \), so knowing your system’s Hamiltonian (e.g., Ising model, Hubbard model, etc.) will guide the decomposition process.
- Tuning: You’ll need to tune the number of steps in the Suzuki-Trotter approximation. Start with a small number (like 1-3) and increase to balance precision and computational cost.

This method keeps your Butterfly Orthogonal Ansatz intact while layering in the Suzuki-Trotter steps as enhancements to improve accuracy without replacing the core circuit.
