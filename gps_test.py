import serial
import pynmea2
import time

#might also work for /dev/ttys0
serial_port = "/dev/serial0"

def get_gps_data():
	try:
		ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
		print("Serial port opened")

		while True:
			line = ser.readline().decode('utf-8', errors-'ignore')
			if line.startswith('$GPGGA'):
				try:
					msg = pynmea2.parse(line)
					if msg.gps_qual > 0:
						print(f"TimeStamp: {msg.timestamp}")
						print(f"Lat: {msg.latitude:.6f} {msg.lat_dir}")
						print(f"Lon: {msg.longitude:.6f} {msg.lon_dir}")
						print(f"Altitude: {msg.altitude} {msg.altitude_units}")
						print(f"satellites: {msg.num_sats}")
						print("-" * 29)
					else:
						print(f"Waiting for valid Gps fix ...")
				except pynmea2.ParseError as e:
					print(f"Parse error: {e}")
			time.sleep(0.5)
	except serial.SerialException as e:
		print(f"Error: could not open serial port {serial_port}")
		print(f"details: {e}")
	except keyboardInterrupt:
		print("\nProgram terminated by user")
	finally:
		if 'ser' in locals() and ser.is_open:
			ser.close()
			print("Serial port Closed")
if __name__ == "__main__":
	get_gps_data():