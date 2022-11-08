import math

import arcade

from chronobio.game.location import Location
from chronobio.viewer.constants import (
    FARM_BUILDING_DISTANCE_FROM_CENTER,
    FARM_BUILDING_WIDTH,
    FIELD_DISTANCE,
    FIELD_OFFSET,
    FIELD_WIDTH,
    SOUP_FACTORY_DISTANCE_FROM_CENTER,
    SOUP_FACTORY_WIDTH,
)

location_to_position: dict[Location, tuple[float, float]] = {
    Location.FARM: (FARM_BUILDING_DISTANCE_FROM_CENTER, FARM_BUILDING_WIDTH),
    Location.FIELD1: (FIELD_OFFSET + 0 * FIELD_DISTANCE, 2 * FIELD_WIDTH),
    Location.FIELD2: (FIELD_OFFSET + 1 * FIELD_DISTANCE, 2 * FIELD_WIDTH),
    Location.FIELD3: (FIELD_OFFSET + 2 * FIELD_DISTANCE, 2 * FIELD_WIDTH),
    Location.FIELD4: (FIELD_OFFSET + 3 * FIELD_DISTANCE, 2 * FIELD_WIDTH),
    Location.FIELD5: (FIELD_OFFSET + 4 * FIELD_DISTANCE, 2 * FIELD_WIDTH),
    Location.SOUP_FACTORY: (SOUP_FACTORY_DISTANCE_FROM_CENTER, SOUP_FACTORY_WIDTH),
}


class MovingEntity:
    def __init__(
        self, sprite_path=":resources:images/tiles/boxCrate_double.png"
    ) -> None:
        self.target_location: Location = Location.FARM
        self.sprite: arcade.Sprite = arcade.Sprite(sprite_path, scale=1.0)
        self.sprite.width = 80
        self.sprite.height = 80
        self.sprite.angle = 0
        self.x, self.y = location_to_position[self.target_location]

    def update_position(self, farm: "Farm"):
        target_x, target_y = location_to_position[self.target_location]
        self.x = (target_x - self.x) * 0.1 + self.x
        self.y = (target_y - self.y) * 0.1 + self.y

        self.sprite.center_x, self.sprite.center_y = farm.rotate(self.x, self.y)


class Farm:
    def __init__(self, x, y, angle=0):
        self.angle = angle
        self.x = x
        self.y = y
        self.employees: dict[int, MovingEntity] = {}

    def rotate(self, x, y):
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        return cos * x - sin * y + self.x, sin * x + cos * y + self.y

    def update(self, data):
        seen = set()
        for employee in data["employees"]:
            seen.add(employee["id"])
            employee_entity = self.employees.get(
                employee["id"],
                MovingEntity("chronobio/viewer/images/farmer.png"),
            )
            employee_entity.sprite.width = 60
            employee_entity.sprite.height = 60
            employee_entity.target_location = Location[employee["location"]]
            self.employees[employee["id"]] = employee_entity
        for employee_id in list(self.employees):
            if employee_id not in seen:
                del self.employees[employee_id]

    def draw(self):
        sprite_list = arcade.SpriteList()

        for employee in self.employees.values():
            employee.update_position(self)
            sprite_list.append(employee.sprite)

        sprite_list.draw()