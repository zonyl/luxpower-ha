import socket
import struct

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('10.20.70.1', 8000))

registers = {}
data = {}

def connect():
    while 1:
        data = clientsocket.recv(2048)
        print("Packet:", data.hex())
        if len(data) == 291:
            print("Modbus Packet")
            p = {}

            p['address'] = int(data[20])
            p['function'] = int(data[21])
            p['serial_number'] = data[22:32].decode('utf-8')
            p['start_address'] = struct.unpack("<H", data[32:34])[0]
            p['number_of_bytes'] = int(data[34])
            r = p['start_address']
            for i in range(35, len(data)-3, 2):
                registers[r] = struct.unpack("<H", data[i:i+2])[0]
                r+=1
            decode_registers()
            print("MP", p)
            print("R", registers)

def decode_registers():
    decode_working_mode()
    r5 = registers[5].to_bytes(2,'big')
    data["State of Health (%)"] = r5[0]
    data["State of Charge (%)"] = r5[1]
    data["R-Phase (Volts)"] = registers[12] * 0.1
    data["S-Phase (Volts)"] = registers[13] * 0.1
    print("Data", data)

def decode_working_mode():
    mode = 'undefined'
    match registers[0]:
        case 0:
            mode = "Standby"
        case 64:
            mode = "Battery off-grid"

    data['Working Mode'] = mode

def main():
    connect()

if __name__ == "__main__":
    main()
