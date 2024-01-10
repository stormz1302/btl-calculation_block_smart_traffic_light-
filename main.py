import json

from flask import Flask, request
from flask_socketio import SocketIO, join_room

from caculator_module import Calculator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins='*')

simulation_id = ''
embedded_id = ''

calculator = Calculator()


@socketio.on('connect')
def handle_connect(data):
    session_id = request.sid  # Get the session ID of the connected client
    join_room(session_id)  # Optionally, join the client to a room with its own session ID
    print("Client connected:", request.sid)


@socketio.on('simulation_login')
def simulation_logged_in(data):
    print('simulation block logged in')
    global simulation_id
    simulation_id = request.sid  # Get the session ID of the connected client


@socketio.on('embedded_login')
def simulation_logged_in(data):
    print('embedded block logged in')
    global embedded_id
    embedded_id = request.sid


@socketio.on('r1_ai')
def update_route_1(data):
    global calculator
    try:
        if data == 'end_of_stream':
            calculator.reset_route('r1')

        parsed = json.loads(data)
        base64_img = parsed['base64Img']
        # print(base64_img)
        current_vehicle_per_fps = parsed['current_vehicle_per_fps']
        data_car = parsed['data_car']
        data_bus = parsed['data_bus']
        data_truck = parsed['data_truck']
        data_motor = parsed['data_motor']
        fps = parsed['fps']

        calculator.update_ai(key='r1', base64=base64_img, current_vehicle=current_vehicle_per_fps, car=data_car,
                             bus=data_bus, truck=data_truck, motor=data_motor, fps=fps)

    except KeyError as e:
        print(f"Key not found: {e}")


@socketio.on('r2_ai')
def update_route_2(data):
    global calculator
    try:
        if data == 'end_of_stream':
            calculator.reset_route('r2')

        parsed = json.loads(data)
        base64Img = parsed['base64Img']
        current_vehicle_per_fps = parsed['current_vehicle_per_fps']
        data_car = parsed['data_car']
        data_bus = parsed['data_bus']
        data_truck = parsed['data_truck']
        data_motor = parsed['data_motor']
        fps = parsed['fps']

        calculator.update_ai(key='r2', base64=base64Img, current_vehicle=current_vehicle_per_fps, car=data_car,
                             bus=data_bus, truck=data_truck, motor=data_motor, fps=fps)

    except KeyError as e:
        print(f"Key not found: {e}")


@socketio.on('r3_ai')
def update_route_3(data):
    global calculator
    try:
        if data == 'end_of_stream':
            calculator.reset_route('r3')

        parsed = json.loads(data)
        base64Img = parsed['base64Img']
        current_vehicle_per_fps = parsed['current_vehicle_per_fps']
        data_car = parsed['data_car']
        data_bus = parsed['data_bus']
        data_truck = parsed['data_truck']
        data_motor = parsed['data_motor']
        fps = parsed['fps']

        calculator.update_ai('r3', base64Img, current_vehicle_per_fps, data_car, data_bus, data_truck, data_motor, fps)

    except KeyError as e:
        print(f"Key not found: {e}")


@socketio.on('r4_ai')
def update_route_4(data):
    global calculator
    try:
        if data == 'end_of_stream':
            calculator.reset_route('r4')

        parsed = json.loads(data)
        base64Img = parsed['base64Img']
        current_vehicle_per_fps = parsed['current_vehicle_per_fps']
        data_car = parsed['data_car']
        data_bus = parsed['data_bus']
        data_truck = parsed['data_truck']
        data_motor = parsed['data_motor']
        fps = parsed['fps']
        #
        # print("ROUTE 4")
        # # print('Base64: ', base64Img)
        # print('Current_vehicle: ', current_vehicle_per_fps)
        # print('data_car: ', data_car)
        # print('data_bus: ', data_bus)
        # print('data_truck: ', data_truck)
        # print('data_motor: ', data_motor)
        # print('fps: ', fps)

        calculator.update_ai('r4', base64Img, current_vehicle_per_fps, data_car, data_bus, data_truck, data_motor, fps)

    except KeyError as e:
        print(f"Key not found: {e}")


@socketio.on('r1_embedded')
def update_r1_em(data):
    global calculator
    try:
        parsed = json.loads(data)

        r1_state = parsed['r1']
        r2_state = parsed['r2']
        r3_state = parsed['r3']
        r4_state = parsed['r4']

        calculator.update_embedded('r1', r1_state)
        calculator.update_embedded('r2', r2_state)
        calculator.update_embedded('r3', r3_state)
        calculator.update_embedded('r4', r4_state)

    except KeyError as e:
        print(f"Key not found: {e}")


def update_simulation(data):
    global simulation_id
    if simulation_id:
        print('sent to simulation')
        sent_data(data, simulation_id)


def update_embedded(data):
    global embedded_id
    if embedded_id:
        print('sent to embedded block')
        sent_data(data, embedded_id)


def sent_data(data, _id):
    socketio.emit('update_result', data, room=_id)


def background_task():
    global calculator
    print('background task started!')
    while True:
        calculator.calculate()
        """
        Simulation
        event: update_result
        content: json
        data:
        {
            r1: {
                base64Img: '',
                state: 'red',
                vehicle_count: 0,
                density: 0.0,
                car: 0.0,
                bus: 0.0,
                truck: 0.0,
                motor: 0.0,
                fps: 0.0
            },
            r2: {
                base64Img: '',
                state: 'red',
                vehicle_count: 0,
                density: 0.0,
                car: 0.0,
                bus: 0.0,
                truck: 0.0,
                motor: 0.0,
                fps: 0.0
            },
            r3: {
                base64Img: '',
                state: 'red',
                vehicle_count: 0,
                density: 0.0,
                car: 0.0,
                bus: 0.0,
                truck: 0.0,
                motor: 0.0,
                fps: 0.0
            },
            r4: {
                base64Img: '',
                state: 'red',
                vehicle_count: 0,
                density: 0.0,
                car: 0.0,
                bus: 0.0,
                truck: 0.0,
                motor: 0.0,
                fps: 0.0
            },
        }
        
        Embedded Block
        event: update_result
        """
        simulation_data = {'r1': calculator.get_simulation_route('r1'), 'r2': calculator.get_simulation_route('r2'),
                           'r3': calculator.get_simulation_route('r3'), 'r4': calculator.get_simulation_route('r4')}

        simulation_data = json.dumps(simulation_data)

        embedded_data = calculator.get_embedded_data()
        embedded_data = json.dumps(embedded_data)

        update_simulation(simulation_data)
        update_embedded(embedded_data)

        socketio.sleep(0.1)


if __name__ == '__main__':
    socketio.start_background_task(background_task)
    socketio.run(app, host='0.0.0.0', port=5000)
