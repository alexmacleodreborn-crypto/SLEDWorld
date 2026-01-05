from world_core.world_object import WorldObject


class ShopProfile(WorldObject):
    """
    Commercial place with objects.
    """

    def __init__(
        self,
        name: str,
        position: tuple[float, float, float],
        category: str = "grocery",
        area: tuple[int, int] = (40, 30),
    ):
        super().__init__(name=name, position=position)

        self.category = category
        self.area = area

    def snapshot(self):
        return {
            "type": "shop",
            "name": self.name,
            "position": self.position,
            "category": self.category,
            "area": self.area,
        }