from oqc_imports import get_input, format_input, replace_Y_XZ, reduce_pulse
from oqc_helper import seq_to_matrix  # only for testing
import numpy as np  # only for testing equality of two pulses (np.allclose())

if __name__ == '__main__':
    input_string, lengthZ, lengthX = get_input(part = 3)
        
    gate_seq, angle_seq = format_input(input_string)
    gate_seq_XZ, angle_seq_XZ = replace_Y_XZ(gate_seq, angle_seq, [lengthZ, lengthX])
    gate_seq_short, angle_seq_short = reduce_pulse(gate_seq_XZ, angle_seq_XZ)

    # Verifying that obtained results are valid
    #print(seq_to_matrix(gate_seq_short, angle_seq_short),'\n',
    #    seq_to_matrix(gate_seq, angle_seq))
    
    assert np.allclose(
        seq_to_matrix(gate_seq_short, angle_seq_short),
        seq_to_matrix(gate_seq, angle_seq))

    # Giving output
    final_seq = ', '.join([f'{ii}({jj})' for ii, jj in zip(gate_seq_short, angle_seq_short)])
    XZ_seq = ', '.join([f'{ii}({jj})' for ii, jj in zip(gate_seq_XZ, angle_seq_XZ)])
    print('Input sequence:', input_string,
            '\n\nXZ sequence:', XZ_seq,
            '\nDuration:', gate_seq_XZ.count("Z")*lengthZ + gate_seq_XZ.count("X")*lengthX,
            'ns\n\nFinal sequence:', final_seq,
            '\nDuration:', gate_seq_short.count("Z")*lengthZ + gate_seq_short.count("X")*lengthX,
            'ns\n')


