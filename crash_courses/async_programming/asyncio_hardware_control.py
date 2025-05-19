import asyncio
import serial_asyncio


async def read_serial(ser):
    while True:
        byte = await asyncio.to_thread(ser.read, 1)
        print(f"Received: {byte}")


async def main():
    import serial

    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=None)
    await read_serial(ser)


asyncio.run(main())
