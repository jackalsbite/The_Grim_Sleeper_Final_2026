from abc import ABC
from typing import Callable, Dict, Any
import pykraken as kn
 
 
class StateType(ABC):
    def handle_event(self, event: kn.Event) -> None:
        pass
 
    def update(self) -> None:
        pass
 
 
class FSM:
    _stack: list[StateType] = []
    _registry: Dict[str, Dict[str, Any]] = {}
 
    @staticmethod
    def register_state(name: str, factory: Callable[[], StateType], persistent: bool = False) -> None:
        FSM._registry[name] = {"factory": factory, "persistent": persistent, "instance": None}
 
    @staticmethod
    def enter_state(state: str) -> None:
        entry = FSM._registry.get(state)
        if not entry:
            kn.log.error(f"State '{state}' is not registered.")
            return

        if entry.get("persistent"):
            if entry.get("instance") is None:
                entry["instance"] = entry["factory"]()

            new_state = entry["instance"]
            FSM._stack.append(new_state)
        else:
            new_state = entry["factory"]()
            FSM._stack.append(new_state)

        if hasattr(new_state, "startup"):
            new_state.startup()
 
    @staticmethod
    def exit_state() -> None:
        if FSM._stack:
            FSM._stack.pop()
        else:
            kn.log.warn("FSM stack is empty. Cannot exit state.")
 
    @staticmethod
    def get_current_state() -> StateType:
        if not FSM._stack:
            kn.log.warn("FSM stack is empty. No current state.")
        
        return FSM._stack[-1]