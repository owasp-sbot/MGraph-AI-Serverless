from dataclasses                                                                            import dataclass
from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Output_Format  import Model__Matplotlib__Output_Format
from typing                                                                                 import Tuple, Dict, Any

# todo: refactor the config into a separate class (i.e. top level should just be graph and config)
@dataclass
class Model__Matplotlib__Render:
    graph_data      : Dict[str, Any]                   = None                    # Serialized graph data
    layout          : str                              = 'spring'                # Layout algorithm to use
    figsize         : Tuple[int, int]                  = (10, 10)                # Figure size in inches
    node_size       : int                              = 1000                    # Size of nodes
    node_color      : str                              = 'lightblue'             # Color of nodes
    output_format   : Model__Matplotlib__Output_Format = Model__Matplotlib__Output_Format.png
    dpi             : int                              = 300                     # Resolution in dots per inch