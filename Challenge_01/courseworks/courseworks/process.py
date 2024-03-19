import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import numpy as np

class My_Subscriber(Node):
    def __init__(self):
        super().__init__('process')
        self.signal_sub = self.create_subscription(Float32, 'signal', self.listener_callback_signal, 10)
        self.time_sub = self.create_subscription(Float32, 'time', self.listener_callback_time, 10)

        self.frequency = 1 # Frcuencia de la señal
        self.amplitude = 1/2 # Amplitud modificada de la señal
        self.offset = 1/2 # Offset de la señal
        self.phase = 1/2 # Fase de la señal

        self.t = 0 # Tiempo que llega del topico

        self.timer_period = 0.1 # Periodo de muestreo
        self.proc_signal_publisher = self.create_publisher(Float32, 'proc_signal', 10) # Publisher de la señal modificada
        self.proc_signal_timer = self.create_timer(self.timer_period, self.timer_callback_proc_signal) # Timer callback de señal procesada
        self.msg = Float32() # Tipo de dato entero

        self.get_logger().info('Precess node initialized.')

    def timer_callback_proc_signal(self):

        omega = 2 * np.pi * self.frequency # Carcular omega
        self.signal = self.amplitude * np.sin(omega * self.t + self.phase) + self.offset # Modificar señal

        self.msg.data = self.signal
        self.proc_signal_publisher.publish(self.msg) # Publicar señal

    def listener_callback_signal(self, msg):
        self.get_logger().info('Message: {}'.format(msg.data))

        self.signal = msg.data # Guardar el dato de señal recibido

    def listener_callback_time(self, msg):
        self.get_logger().info('Message: {}'.format(msg.data))

        self.t = msg.data # Guardar el tiempo recibido

def main(args=None):
    rclpy.init(args=args)
    m_s = My_Subscriber()
    rclpy.spin(m_s)
    m_s.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()