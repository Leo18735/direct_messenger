from Connection import Connection
import argparse

def main(destination_ip: str, destination_port: int, source_ip: str, source_port: int):
    connection: Connection = Connection(destination_ip, destination_port, source_ip, source_port)
    connection.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    default_port: int = 45632

    parser.add_argument("destination_ip", help="Ip to connect to")
    parser.add_argument("-dp", "--destination_port", help="Port to connect to", default=default_port, type=type(default_port))
    parser.add_argument("-si", "--source_ip", help="Ip to listen on", default="0.0.0.0", type=str)
    parser.add_argument("-sp", "--source_port", help="Port to listen on", default=default_port, type=type(default_port))

    args = parser.parse_args()

    main(args.destination_ip, args.destination_port, args.source_ip, args.source_port)
