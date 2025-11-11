class Component:
    pass


class PlayerComponent(Component):
    def __init__(self, name):
        self.name = name


class HealthComponent(Component):
    def __init__(self, value):
        self.health = value


class ScoreComponent(Component):
    def __init__(self, value):
        self.score = value


class Entity:
    def __init__(self, eid):
        self.id = eid
        self.name = ""
        self.health = 0
        self.score = 0


class ECSManager:
    def __init__(self, event_bus):
        self.entities = {}
        self.next_id = 0
        self.event_bus = event_bus

    def create_entity(self):
        e = Entity(self.next_id)
        self.entities[self.next_id] = e
        self.next_id += 1
        return e

    def add_component(self, entity, component):
        if isinstance(component, PlayerComponent):
            entity.name = component.name
        elif isinstance(component, HealthComponent):
            entity.health = component.health
        elif isinstance(component, ScoreComponent):
            entity.score = component.score

    def get_player(self):
        return list(self.entities.values())[0] if self.entities else None
