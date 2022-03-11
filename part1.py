from oqc_imports import get_input, format_input, reduce_pulse
from oqc_helper import seq_to_matrix  # only for testing
import numpy as np  # only for testing equality of two pulses (np.allclose())

if __name__ == '__main__':
    input_string = get_input()
    gate_seq, angle_seq = format_input(input_string)
    gate_seq_short, angle_seq_short = reduce_pulse(gate_seq, angle_seq)

    # Verifying that obtained results are valid
    assert np.allclose(
        seq_to_matrix(gate_seq_short, angle_seq_short),
        seq_to_matrix(gate_seq, angle_seq))

    # Giving output
    final_seq = ', '.join([f'{ii}({jj})' for ii, jj in zip(gate_seq_short, angle_seq_short)])
    print('Input pulse sequence:', input_string,
          '\nPulses:', len(gate_seq),
          '\n\nFinal sequence:', final_seq,
          '\nPulses:', len(gate_seq_short))

