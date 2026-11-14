"""Complete campaign render links, with no alternate State or RAM snapshot."""
from .services import ServiceBinding
from .contexts_tick import MapTickFrame
from .contexts_gameplay import FirstDeploymentFrame


def _visible_packets(state, frame):
    from .business_gameplay import render_visible_map_packets_complete
    return render_visible_map_packets_complete(state, frame)


def _city_entries(state, frame):
    from .business_gameplay import render_city_map_entries_complete
    return render_city_map_entries_complete(state, frame)


def _force_markers(state, frame):
    from .business_highbank import render_force_city_markers_fields
    return render_force_city_markers_fields(state, frame)


def _active_controller(state, frame):
    from .business_gameplay import select_active_battle_controller_complete
    return select_active_battle_controller_complete(state, frame)


def render_bindings():
    """Four exact at-call ABIs; known helpers still own their real algorithms."""
    return (ServiceBinding(89574, MapTickFrame, MapTickFrame, _visible_packets), ServiceBinding(92586, MapTickFrame, MapTickFrame, _city_entries), ServiceBinding(424444, FirstDeploymentFrame, FirstDeploymentFrame, _force_markers), ServiceBinding(106862, MapTickFrame, MapTickFrame, _active_controller))
