"""
Default AI2-THOR Blue Physics Based Agent. It can ONLY move in x/z directions
and can only change it's yaw.
"""

# TODO: raise exception for robothor scenes

from typing import Union, Tuple, Dict, List
from .agent import Agent
import ai2thor.utils


class Jarvis(Agent):
    def __init__(
            self,
            camera: ai2thor.utils.Camera = ai2thor.utils.Camera(),
            noise: None = None,
            default_rotate_degrees: float = 90,
            default_move_meters: float = 0.25,
            nav_success_max_meter_dist: float = 1.5):
        Agent.__init__(
            self,
            camera=camera,
            noise=noise,
            default_rotate_degrees=default_rotate_degrees,
            default_move_meters=default_move_meters,
            nav_success_max_meter_dist=nav_success_max_meter_dist)
        # step here to set up the agent

    @property
    def pos(self) -> Tuple[float, float]:
        """Returns the tuple(x, z) position of the agent"""
        event = self._base_controller.last_event
        pos = event.metadata['agent']['position']
        return pos['x'], pos['z']

    @property
    def rot(self) -> float:
        """Returns the yaw (or heading direction) of the agent"""
        event = self._base_controller.last_event
        return event.metadata['agent']['rotation']['y']

    @property
    def pose(self) -> Dict[str, float]:
        # use this format for teleporting
        event = self._base_controller.last_event
        horizon = event.metadata['agent']['cameraHorizon']
        pos = self.pos
        rot = self.rot
        return {
            'x': pos[0],
            'z': pos[1],
            'rot_y': rot,
            'horizon': horizon
        }

    @property
    def reachable_positions(self) -> List[Dict[str, float]]:
        # TODO: Cache per scene
        self._step('GetReachablePositions', renderImage=False)
        event = self._base_controller.last_event
        positions = event.metadata['reachablePositions']
        return [{
            'x': pos['x'],
            'z': pos['z']
        } for pos in positions]

    def teleport(
            self,
            x: Union[None, float] = None,
            z: Union[None, float] = None,
            rot_y: Union[None, float] = None,
            horizon: Union[None, float] = None) -> bool:
        # uses default values if they're not specified
        event = self._base_controller.last_event
        pos = event.metadata['agent']['position']
        y = pos['y']
        x = pos['x'] if x is None else x
        z = pos['z'] if z is None else z

        rot = event.metadata['agent']['rotation']
        rot_x = rot['x']
        rot_z = rot['z']
        rot_y = rot['y'] if rot_y is None else rot_y

        horizon = self.horizon if horizon is None else horizon

        return self._step(
            'TeleportFull',
            x=x, y=y, z=z,
            rotation={'x': rot_x, 'y': rot_y, 'z': rot_z},
            horizon=horizon
        )


'''
class Jarvis(ai2thor.agents.Agent):
    def __init__(
            self,
            controller: ai2thor.typing_controller.Controller,
            agent_idx: Union[int, None] = None):
        ai2thor.agents.Agent.__init__(self, controller, agent_idx)

    def open(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            openness: Union[None, float] = None,
            force_action: bool = False) -> None:
        pass

    def close(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass

    def cook(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

    def cut(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

    def destroy(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

    def dirty(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

    def clean(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

    def liquid_fill(
            self,
            liquid_type: str,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

    def liquid_empty(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

    def use_up(
            self,
            x: Union[float, None] = None,
            y: Union[float, None] = None,
            object_id: Union[None, str] = None,
            force_action: bool = False) -> None:
        pass

'''
