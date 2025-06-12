import serial
import threading
import time
from utils.log import logger

class comm_manager:
    def __init__(self, port: str, baudrated: int = 9600, on_data_received=None):
        # Varibles de comunicacion, utilizados al crear la comunicacion virtual
        self.port = port
        self.baudrated = baudrated

        # Banderas estado
        self.on_data_received = on_data_received
        self._running = False
        self._thread = None
        self.serial = None

    def start(self):
        logger.info(f"Communication open to {self.port}@{self.baudrated}")

        try:
            self.serial = serial.Serial(
                self.port, 
                self.baudrated, 
                timeout=1
            )
        except serial.SerialException as e:
            logger.error(f"Failed to open serial port {self.port}: {e}")
            return

        self._running = True
        self._run()
    
    def stop(self):
        self._running = False

        if self._thread:
            self._thread.join()
        if self.serial and self.serial.is_open:
            self.serial.close()

        logger.info("Comm closed.")
        
    def _run(self):
        logger.info(f"Serial monitor started. Press Ctrl+C to stop.")
        try:
            while self._running:
                if self.serial.in_waiting > 0:
                    trama = self.serial.read(self.serial.in_waiting)
                    logger.debug(f"REQUEST => {trama.hex().upper()}")

                    if self.on_data_received:
                        try:
                            respuesta = self.on_data_received(trama)
                            if isinstance(respuesta, bytes):
                                self.send_response(respuesta)
                            else:
                                logger.warning("The response is not of type bytes.")
                        except Exception as e:
                            logger.error(f"Frame processing failed: {e}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Interrupted by user.")
        finally:
            self.stop()
    
    def send_response(self, data: bytes):
        if self.serial and self.serial.is_open:
            self.serial.write(data)
            logger.debug(f"RESPONSE <= {data.hex().upper()!r}")
