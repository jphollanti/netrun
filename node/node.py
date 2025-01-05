from . import jack_in
from . import black_ice
from . import white_ice
from . import firewall
from . import competing_netrunner
from . import trace_program
from . import signal_interference
from . import data_fortress
from . import mainframe
from . import data_core

node_types = [
    'Black ICE', # ICE = Intrusion Countermeasures Electronics
    'White ICE', 
    'Firewall', 
    'Competing Netrunner', 
    #'Trace Program', 
    #'Signal Interference',
]

end_node_types = ['Mainframe', 'Data Core']

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
    elif type == 'Mainframe':
        return mainframe.mainframe
    elif type == 'Data Core':
        return data_core.data_core
    else:
        raise Exception("Unknown node type: " + type)
    