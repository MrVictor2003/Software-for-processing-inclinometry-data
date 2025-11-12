from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

def init_sensors():
    i2c.writeto_mem(0x68, 0x6B, b'\x00')
    i2c.writeto_mem(0x0D, 0x0A, b'\x01')
    i2c.writeto_mem(0x0D, 0x09, b'\x01')
    time.sleep(0.1)

def read_mpu6050():
    data = i2c.readfrom_mem(0x68, 0x3B, 14)
    ax = (data[0]<<8|data[1])/16384.0
    ay = (data[2]<<8|data[3])/16384.0
    az = (data[4]<<8|data[5])/16384.0
    gx = (data[8]<<8|data[9])/131.0
    gy = (data[10]<<8|data[11])/131.0
    gz = (data[12]<<8|data[13])/131.0
    return ax, ay, az, gx, gy, gz

def read_qmc5883():
    data = i2c.readfrom_mem(0x0D, 0x00, 6)
    x = (data[1]<<8|data[0])
    y = (data[3]<<8|data[2])
    z = (data[5]<<8|data[4])
    if x>32767: x-=65536
    if y>32767: y-=65536
    if z>32767: z-=65536
    return x, y, z

init_sensors()
measurements = []
start = time.ticks_ms()

for i in range(300):
    accel_gyro = read_mpu6050()
    magn = read_qmc5883()
    t = time.ticks_ms() - start
    p = i * 8
    measurements.append((t/1000, accel_gyro[0], accel_gyro[1], accel_gyro[2],
                        accel_gyro[3], accel_gyro[4], accel_gyro[5],
                        magn[0], magn[1], magn[2], p))
    print(f"Измерение {i+1}/300")
    time.sleep(0.1)

with open("data.txt", "w") as f:
    for m in measurements:
        f.write(f"{m[0]:.3f},{m[1]:.6f},{m[2]:.6f},{m[3]:.6f},{m[4]:.6f},{m[5]:.6f},{m[6]:.6f},{m[7]:.1f},{m[8]:.1f},{m[9]:.1f},{m[10]}\n")

print("300 измерений сохранены")
