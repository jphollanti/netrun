from . import jack_in
from . import black_ice
from . import white_ice
from . import firewall
from . import competing_netrunner
from . import mainframe
from . import data_core

_registry = {
    'Jack-In': jack_in.jack_in,
    'Black ICE': black_ice.black_ice,
    'White ICE': white_ice.white_ice,
    'Firewall': firewall.firewall,
    'Competing Netrunner': competing_netrunner.competing_netrunner,
    'Mainframe': mainframe.mainframe,
    'Data Core': data_core.data_core,
}

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
    if type not in _registry:
        raise Exception("Unknown node type: " + type)
    return _registry[type]
