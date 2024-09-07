# src\RAD_trading\events\event_system.py
class EventSystem:
    def __init__(self):
        self.listeners = {}
    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)
    def unsubscribe(self, event_type, listener):
        if event_type in self.listeners and listener in self.listeners[event_type]:
            self.listeners[event_type].remove(listener)
    def emit(self, event):
        if event.type in self.listeners:
            for listener in self.listeners[event.type]:
                listener(event)
