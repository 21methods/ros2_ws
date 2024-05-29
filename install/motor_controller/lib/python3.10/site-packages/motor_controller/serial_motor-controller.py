import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class SerialMotorController(Node):
	def __init__(self):
		super().__init__('serial_motor_controller')
		self.publisher_= self.create_publisher(String,  'motor_status', 10)
		self.subscription = self.create_subscription(
			string, 
			'motor_commands',
			self.listener_callback,
			10
		)
		self.arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
		self.get_logger().info('Serial motor controller node started.')

	def listener_callback(self, msg):
		command = msg.data.upper()
		self.get_logger().info(f'Receveived command: {command}')
		if command in ['F', 'B', 'L', 'R', 'S']:
			self.arduino.write(command.encode())
			self.get_logger().info(f'Sent command: {command}')
			feedback = self.arduino.readline().decode('utf-8').strip()
			if feedback:
				self.get_logger().info(f'Feedback from Arduino: {feedback}')
				self.publisher_.publish(String(data=feedback))
			else:
				self.get_logger().warn(f'Invalid command: {command}')
def main(args=None):
	rclpy.init(args=args)
	node = SerialMotorController()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()

