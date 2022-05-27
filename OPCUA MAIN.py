from opcua import Client, ua
import requests
import time
import json


def read_input_value(node_id):
    client_node = Client.get_node(client, node_id)  # get node
    client_node_value = client_node.get_value()  # read node value
    print("READ Value of : " + str(client_node) + " : " + str(client_node_value))
    return client_node_value


def write_value_bool(node_id, value):
    client_node = client.get_node(node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Boolean))
    client_node.set_value(client_node_dv)
    print("WRITTEN Value of : " + str(client_node) + " : " + str(client_node_value))


def write_value_int(node_id, value):
    client_node = Client.get_node(client, node_id)  # get node
    client_node_value = value
    client_node_dv = ua.DataValue(ua.Variant(client_node_value, ua.VariantType.Int16))
    client_node.set_value(client_node_dv)
    print("WRITTEN Value of : " + str(client_node) + " : " + str(client_node_value))


def get_firebase_state():
    endpoint = "https://cylinder-88625-default-rtdb.firebaseio.com/cylindercontrol.json"
    resp = json.loads(requests.get(endpoint).text)
    return resp


def put_firebase_state(json_inp):
    endpoint = "https://cylinder-88625-default-rtdb.firebaseio.com/cylindercontrol.json"
    # json.loads(requests.put(endpoint, json=json_inp).text)
    requests.put(endpoint, json=json_inp)
    print('Inserted data successfully')


if __name__ == '__main__':
    url = "opc.tcp://192.168.0.1:4840"
    client = Client(url)

    client.connect()

    root = client.get_root_node()
    print("Object root node is: ", root)

    try:
        while True:
            # todo read from firebase
            jsonData = get_firebase_state()
            print(jsonData) # cn
            print('test')
            start_state = True if jsonData["start"] == 'true' else False
            stop_state = True if jsonData["stop"] == 'true' else False

            write_value_bool('ns=3;s="PYTHON"."START"', start_state)
            write_value_bool('ns=3;s="PYTHON"."STOP"', stop_state)

            outputPy = read_input_value('ns=3;s="PYTHON"."OUTPUT"')
            put_firebase_state(json.loads(outputPy))

            print('done pushing ', str(outputPy))

    finally:
        client.disconnect()
