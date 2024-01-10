from contants import LIGHT


class Route:
    traffic_density = [0, 0, 0, 0]
    base64 = ''
    fps = 0.0
    next_time = 0
    state = LIGHT.RED
    current_vehicle = 0

    def change_state(self, state):
        self.state = state
