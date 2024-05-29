import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MotorControlNode(Node):
    def __init__(self):
        super().__init__('motor_control')
        self.publisher_ = self.create_publisher(String, 'motor_commands', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.commands = ['f', 'b', 'l', 'r', 's'].upper()
        self.command_index = 0

    def timer_callback(self):
        msg = String()
        msg.data = self.commands[self.command_index]
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.command_index = (self.command_index + 1) % len(self.commands)

def main(args=None):
    rclpy.init(args=args)
    node = MotorControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
