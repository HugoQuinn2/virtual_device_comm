from comm_manager import comm_manager
from utils.log import logger
from utils.file_actions_util import *
import time
import click

file_data = None

def handler_actions(data: bytes):
        hex_data = [f"{b:02X}" for b in data]

        for action in file_data.get("actions", []):
             _action_response = action.get("response", [])
             _action_name = action.get("name", "NO NAME")
             _action_delay = action.get("delay", 0)
             _action_request = action.get("request", [])

             if hex_data == _action_response:
                 logger.info(f"Executin action: {_action_name}, <{_action_delay}ms>")
                 time.sleep(_action_delay / 1000)
                 return bytes(int(b, 16) for b in _action_request)
        
        logger.warning(f"No actions founded for {hex_data}")

@click.group()
@click.version_option(version='0.1.0', prog_name='Virtual Device Comm (VDC)')
def cli():
    pass

@cli.command(help='Create a Virtual Device Comm and response petition on base a File Data Actions')
@click.option('--port', '-p', default=None, help='Port to connect, will override file config if provided.')
@click.option('--filename', '-f', required=True, help='File action (JSON)')
@click.option('--baudrate', '-b', default=None, help='Baudrate, will override file config if provided.')
def vd(port, filename, baudrate):
    global file_data

    # Load file actions
    logger.info(f"Loading {filename}.")
    file_data = load_file(filename)

    _file_action_name = file_data.get("name")
    _file_action_version = file_data.get("version")
    _file_action_port = file_data.get("port")
    _file_action_baudrate = file_data.get("baudrate", 9600)

    # Load data file actions
    logger.info(f"Loading data file actions: {_file_action_name} <{_file_action_version}>")
    _port = port if port is not None else _file_action_port
    _baudrate = baudrate if baudrate is not None else _file_action_baudrate

    # Creat com manager and start communication
    comm_man = comm_manager(
        port=_port,
        baudrated=_baudrate,
        on_data_received=handler_actions
    )

    comm_man.start() 

if __name__ == '__main__':
    cli()