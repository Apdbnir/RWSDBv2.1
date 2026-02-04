"""
Action history system for undo/redo functionality in the database application.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Callable, Optional

class Action:
    """Represents a single action that can be undone/redone"""
    
    def __init__(self, name: str, undo_func: Callable, redo_func: Callable, 
                 description: str = "", data: Optional[Dict] = None):
        self.name = name
        self.undo_func = undo_func
        self.redo_func = redo_func
        self.description = description
        self.data = data or {}
        self.timestamp = datetime.now()
    
    def execute_undo(self):
        """Execute the undo function"""
        if self.undo_func:
            self.undo_func()
    
    def execute_redo(self):
        """Execute the redo function"""
        if self.redo_func:
            self.redo_func()


class ActionHistory:
    """Manages the history of actions for undo/redo functionality"""
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.actions: List[Action] = []
        self.current_position = -1  # Points to the last executed action
    
    def add_action(self, action: Action):
        """Add a new action to the history"""
        # Remove any actions after current position (if we've undone some actions)
        if self.current_position < len(self.actions) - 1:
            self.actions = self.actions[:self.current_position + 1]
        
        # Add the new action
        self.actions.append(action)
        
        # Remove oldest actions if we exceed the max history
        if len(self.actions) > self.max_history:
            self.actions.pop(0)
            self.current_position = len(self.actions) - 1
        else:
            self.current_position = len(self.actions) - 1
    
    def can_undo(self) -> bool:
        """Check if we can undo an action"""
        return self.current_position >= 0
    
    def can_redo(self) -> bool:
        """Check if we can redo an action"""
        return self.current_position < len(self.actions) - 1
    
    def undo(self) -> bool:
        """Undo the last action"""
        if not self.can_undo():
            return False
        
        action = self.actions[self.current_position]
        action.execute_undo()
        self.current_position -= 1
        return True
    
    def redo(self) -> bool:
        """Redo the next action"""
        if not self.can_redo():
            return False
        
        self.current_position += 1
        action = self.actions[self.current_position]
        action.execute_redo()
        return True
    
    def get_undo_description(self) -> str:
        """Get description of the action that would be undone"""
        if self.can_undo():
            return self.actions[self.current_position].description
        return ""
    
    def get_redo_description(self) -> str:
        """Get description of the action that would be redone"""
        if self.can_redo():
            return self.actions[self.current_position + 1].description
        return ""
    
    def clear(self):
        """Clear all actions from history"""
        self.actions = []
        self.current_position = -1
    
    def get_actions_count(self) -> int:
        """Get the number of actions in history"""
        return len(self.actions)
    
    def get_current_position(self) -> int:
        """Get the current position in history"""
        return self.current_position