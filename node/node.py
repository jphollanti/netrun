from . import jack_in
from . import black_ice
from . import white_ice
from . import firewall
from . import competing_netrunner
from . import trace_program
from . import signal_interference

node_types = [
    'Black ICE', # ICE = Intrusion Countermeasures Electronics
    'White ICE', 
    'Firewall', 
    'Competing Netrunner', 
    #'Trace Program', 
    #'Signal Interference',
]

end_node_types = ['Data Fortresses', 'Mainframe', 'Data Core']

def generate_node(type):
    # print("Generating node of type", type)

    if type == 'Jack-In':
        return jack_in.jack_in

    elif type == 'Black ICE':
        return black_ice.black_ice
    elif type == 'White ICE':
        return white_ice.white_ice
    elif type == 'Firewall':
        return firewall.firewall
    elif type == 'Competing Netrunner':
        return competing_netrunner.competing_netrunner
    # elif type == 'Trace Program':
    #     return trace_program.trace_program()
    # elif type == 'Signal Interference':
    #     return signal_interference.signal_interference()