import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class KeyboardControlNode(Node):
    def __init__(self):
        super().__init__('keyboard_control')
        self.publisher_ = self.create_publisher(String, 'motor_commands', 10)
        self.get_logger().info('Keyboard control node started. Press keys (w, a, s, d) to control motors.')

    def get_keyboard_input(self):
        # Get keyboard input
        while True:
            key = input('Enter command (w: forward, s: backward, a: left, d: right, q: quit): ')
            if key in ['w', 'a', 's', 'd', 'q']:
                return key
            else:
                print('Invalid command. Please enter w, a, s, d, or q.')

    def main_loop(self):
        while True:
            command = self.get_keyboard_input()
            if command == 'q':
                break
            msg = String()
            msg.data = command
            self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardControlNode()
    node.main_loop()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()