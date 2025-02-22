from pprint import pprint

from utils.color_util import ColorUtil


class Node:
    def __init__(self, node_id, name, value, position, is_accessible, is_user_claimed):
        self.node_id = node_id # aka (circle_number bloodweb position thing)_(unique_id)
        self.name = name.replace(".png", "") # aka unique_id # TODO does this need to replace .png?
        self.value = value
        self.x, self.y = position
        self.is_accessible = is_accessible
        self.is_user_claimed = is_user_claimed

    @staticmethod
    def from_dict(data, **kwargs):
        position = (int(data["x"]), int(data["y"]))
        node = Node(data["node_id"], data["name"], data["value"], position, data["is_accessible"],
                    data["is_user_claimed"])
        for attribute, val in kwargs.items():
            node.__setattr__(attribute, val)
        return node

    @staticmethod
    def state_from_color(color):
        """
        :return: (is_accessible, is_user_claimed)
        """
        if color == "taupe":
            return True, False
        elif color == "red":
            return True, True
        else: # neutral
            return False, False

    def print(self):
        pprint(self.__dict__)

    def get_id(self):
        return self.node_id

    def set_value(self, value):
        self.value = value
        return self

    def set_user_claimed(self, is_claimed):
        self.is_user_claimed = is_claimed

    def get_tuple(self):
        data = {
            "node_id": self.node_id,
            "name": self.name,
            "value": self.value,
            "x": str(self.x),
            "y": str(self.y),
            "is_accessible": self.is_accessible,
            "is_user_claimed": self.is_user_claimed,

            # pyvis attributes
            "title": f"{self.value}, " + ("user claimed" if self.is_user_claimed else "not claimed"),
            "color": ColorUtil.red_hex if self.is_user_claimed else ColorUtil.taupe_hex if self.is_accessible else ColorUtil.neutral_hex,
            "physics": False
        }
        return self.node_id, data

    def get_dict(self):
        t = self.get_tuple()
        return {t[0]: t[1]}
