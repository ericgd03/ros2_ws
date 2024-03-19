import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import numpy as np

class My_Publisher(Node):
    def __init__(self):
        super().__init__('signal_generator')


        self.frequency = 1 # Frcuencia de la señal
        self.amplitude = 1 # Amplitud de la señal

        self.t = 0      # Tiempo
        self.signal = 0 # señal = amplitude * np.sin(2 * np.pi * frequency * time)

        self.signal_publisher = self.create_publisher(Float32, 'signal', 10)
        self.time_publisher = self.create_publisher(Float32, 'time', 10)

        self.timer_period = 0.1 # Periodo de muestreo

        self.signal_timer = self.create_timer(self.timer_period, self.timer_callback_signal)
        self.time_timer = self.create_timer(self.timer_period, self.timer_callback_time)
        self.get_logger().info('Signal generator node successfully initialized.')
        self.msg = Float32()

    def timer_callback_signal(self):

        self.t += self.timer_period # Tiempo que va aumentando
        self.signal = self.amplitude * np.sin(2 * np.pi * self.frequency * self.t) # Señal senoidal del tiempo

        self.msg.data = self.signal
        self.signal_publisher.publish(self.msg)

    def timer_callback_time(self):

        self.msg.data = self.t # Tiempo

        self.time_publisher.publish(self.msg)

def main(args=None):
    rclpy.init(args=args)
    m_p = My_Publisher()
    rclpy.spin(m_p)
    m_p.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()