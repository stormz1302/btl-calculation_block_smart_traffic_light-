from fuzzy_calculator import *
from route import *


class Calculator:
    route1 = Route()
    route2 = Route()
    route3 = Route()
    route4 = Route()

    routes = {'r1': route1, 'r2': route2, 'r3': route3, 'r4': route4}
    print('routes: ', routes.keys())

    def update_ai(self, key, base64, current_vehicle, car, bus, truck, motor, fps):
        if key not in ['r1', 'r2', 'r3', 'r4']:
            print('key: ', key)
            return

        print('key: ', key)
        route = self.routes[key]
        route.base64 = base64
        # print('', base64)
        # print()
        route.current_vehicle = current_vehicle
        route.traffic_density[0] = car
        route.traffic_density[1] = bus
        route.traffic_density[2] = truck
        route.traffic_density[3] = motor
        route.fps = fps

    def update_embedded(self, key, state):
        if key not in ['r1', 'r2', 'r3', 'r4']:
            print('key: ', key)
            return

        route = self.routes[key]
        if state == 'red':
            route.state = LIGHT.RED
        elif state == 'yellow':
            route.state = LIGHT.YELLOW
        elif state == 'green':
            route.state = LIGHT.GREEN
        else:
            route.state = LIGHT.RED

    def calculate(self):
        route1 = self.route1
        route2 = self.route2
        route3 = self.route3
        route4 = self.route4

        light_time_d1, light_time_d2 = estimate_light_time(route1.current_vehicle, route2.current_vehicle,
                                                           route3.current_vehicle, route4.current_vehicle)

        if route1.state == LIGHT.RED and route3.state == LIGHT.RED:
            route1.next_time = light_time_d1
            route3.next_time = light_time_d1
            route2.next_time = light_time_d1
            route4.next_time = light_time_d1  # print('Next time: ', light_time_d1)

        elif route2.state == LIGHT.RED and route4.state == LIGHT.RED:
            route1.next_time = light_time_d2
            route3.next_time = light_time_d2
            route2.next_time = light_time_d2
            route4.next_time = light_time_d2
            print('Next time: ', light_time_d2)

    def get_simulation_route(self, key):
        if key not in ['r1', 'r2', 'r3', 'r4']:
            print('key ' + key + ' not found')
            return
        route = self.routes[key]

        _state = 'red'
        if route.state == LIGHT.RED:
            _state = 'red'
        elif route.state == LIGHT.YELLOW:
            _state = 'yellow'
        else:
            _state = 'green'

        car = route.traffic_density[0]
        bus = route.traffic_density[1]
        truck = route.traffic_density[2]
        motor = route.traffic_density[3]
        # print(key + '\tSUM: car: ' + str(car) + '\tbus: ' + str(bus))
        density = 0
        density = car + bus + truck + motor

        return {'base64Img': route.base64, 'state': _state, 'next_time': route.next_time,
                'vehicle_count': route.current_vehicle, 'density': density, 'car': car, 'bus': bus, 'truck': truck,
                'motor': motor, 'fps': route.fps}

    def get_embedded_data(self):
        return {'r1': self.route1.next_time, 'r2': self.route2.next_time, 'r3': self.route3.next_time,
                'r4': self.route4.next_time}

    def reset_route(self, key):
        if key not in ['r1', 'r2', 'r3', 'r4']:
            print('key ' + key + ' not found')
            return
        new_route = Route()
        self.routes[key] = new_route
        if key == 'r1':
            route1 = new_route
        elif key == 'r2':
            route2 = new_route
        elif key == 'r3':
            route3 = new_route
        elif key == 'r4':
            route4 = new_route
