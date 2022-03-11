def get_input(part = 1):
    """
    Prompts the user for relevant inputs.
    :param part is the part number in the test
    """
    input_string = input('Enter input Ex) "X(90), Y(180), X(90)": ')
    if input_string == '':
        input_string = "X(90), Y(-90.0), X(90), X(-90), X(-120), X(10), Y(20), Y(30), X(30), X(30), Y(180), X(60)"
        # input_string = "X(90), Y(180), X(90)"
        print(f'Setting input: {input_string}\n' )
    
    if part == 3:
        try:
            lengthX = float(input('Enter duration of X gate (ns): '))
            if lengthX < 0:
                print("Gate duration cannot be negative. Setting it to 10 ns")
                lengthX = 10
            
            lengthZ = float(input('Enter duration of Z gate (ns): '))
            if lengthZ < 0:
                print("Gate duration cannot be negative. Setting it to 100 ns")
                lengthZ = 100
        except:
            print("Wrong inputs. Setting lengthX = 10 ns, lengthZ = 100 ns")
            lengthZ, lengthX = 10, 100
        
        return input_string, lengthZ, lengthX
    
    return input_string
        

def format_input(raw_input):
    """
    Formats the input for the pulse shortening function.
    :param raw_input: string of pulse sequence separated by comma:
    Ex) "X(90), Y(120), X(30)"
    :return: lists of gate and angle sequences
    """
    raw_sequence = raw_input.split(',')
    raw_sequence = [jj.strip().replace('(', '').replace(')', '').upper() for jj in raw_sequence]

    # ensuring gates to be X or Y only
    check_1 = [jj[0] == 'X' or jj[0] == 'Y' for jj in raw_sequence]
    if False in check_1:
        # print("Provided sequence not consists of X or Y gates only")
        raise ValueError("Provided sequence does not consist of only X and Y gates!")

    # ensuring the angles are numbers
    check_2 = [jj[1:].replace('.', '', 1).isdigit() or
               (jj[1] in ['+', '-'] and jj[2:].replace('.', '', 1).isdigit())
               for jj in raw_sequence]
    if False in check_2:
        # print("provided angles are not numbers")
        raise TypeError("Could not parse angles to numbers!")

    gate_sequence = [jj[0] for jj in raw_sequence]
    angle_sequence = [float(jj[1:])%360 for jj in raw_sequence]

    return gate_sequence, angle_sequence


def reduce_pulse(gate_seq, angle_seq):
    """
    Reduces the length of gate sequence according to rules provided in technical test
    :param gate_seq: list of strings specifying gates
    :param angle_seq: list of floats specifying corresponding angles
    :return: reduced list of gate and angle sequences
    """

    g_s, a_s = gate_seq, angle_seq
    while True:
        # starting with a single FSM, nothing fancy
        for ii, gg in enumerate(g_s):
            # print(ii, gg)
            if ii == 0:
                gate_seq_short, angle_seq_short = [g_s[0]], [a_s[0]]
                continue
            if gg is not gate_seq_short[-1]:
                gate_seq_short.append(gg)
                angle_seq_short.append(a_s[ii])
            else:
                angle_seq_short[-1] += a_s[ii]
        angle_seq_short = [ii%360 for ii in angle_seq_short]

        for ii in range(1, len(angle_seq_short) - 1):
            if angle_seq_short[ii] == 180:
                angle_seq_short[ii-1] -= angle_seq_short[ii + 1]
                del angle_seq_short[ii + 1]
                del gate_seq_short[ii + 1]
            if ii >= len(angle_seq_short)-1:
                break

        if len(gate_seq_short)==1:
            break

        zero_angle = [ii for ii, jj in enumerate(angle_seq_short) if jj == 0]
        angle_seq_short = [jj for ii, jj in enumerate(angle_seq_short) if ii not in zero_angle]
        gate_seq_short = [jj for ii, jj in enumerate(gate_seq_short) if ii not in zero_angle]
        rep = [ii for ii in range(len(gate_seq_short) - 1) if gate_seq_short[ii] is gate_seq_short[ii+1]]
        if len(rep) == 0:
            break
        g_s, a_s = gate_seq_short, angle_seq_short

    return gate_seq_short, angle_seq_short


def replace_Y_XZ(gate_seq, angle_seq, lens=[10, 10]):
    """
    substitutes Y(theta) with Z(90)X(theta)Z(-90) according to rules provided in technical test
    :param gate_seq: list of strings specifying gates (X, Y)
    :param angle_seq: list of floats specifying corresponding angles
    :param lens: [lengthZ, lengthX]
    :return: g_s_XZ: list of strings specifying gates (X, Z), a_s_XZ: corresponding angles
    """
    g_s_XZ, a_s_XZ = [], []
    for ii, jj in enumerate(gate_seq):
        if jj == 'X':
            g_s_XZ.append('X')
            a_s_XZ.append(angle_seq[ii])
        else:
            if lens[0]<=lens[1]:
                g_s_XZ.extend(['Z', 'X', 'Z']) # Y(theta) = Z(90)X(theta)Z(-90)
                a_s_XZ.extend([90, angle_seq[ii], -90])
            else:
                g_s_XZ.extend(['X', 'Z', 'X']) # Y(theta) = X(90)Z(-theta)X(-90)
                a_s_XZ.extend([90, -angle_seq[ii], -90])
    return g_s_XZ, a_s_XZ
