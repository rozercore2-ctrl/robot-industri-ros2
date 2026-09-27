import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class RectangleMotion(Node):

    def __init__(self):
        super().__init__('rectangle_motion')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.timer = self.create_timer(
            0.05,
            self.control_loop
        )

        # Ukuran persegi panjang
        self.length = 4.0
        self.width = 2.0

        # Kecepatan
        self.linear_speed = 0.25
        self.angular_speed = 0.4

        # Posisi robot
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.start_x = None
        self.start_y = None

        self.target_yaw = None

        # State
        self.state = 'FORWARD_1'

        self.get_logger().info(
            'Rectangle motion started.'
        )

    def odom_callback(self, msg):

        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation

        siny_cosp = 2.0 * (
            q.w * q.z + q.x * q.y
        )

        cosy_cosp = 1.0 - 2.0 * (
            q.y * q.y + q.z * q.z
        )

        self.yaw = math.atan2(
            siny_cosp,
            cosy_cosp
        )

        if self.start_x is None:

            self.start_x = self.x
            self.start_y = self.y

            self.get_logger().info(
                f'Start: x={self.x:.2f}, '
                f'y={self.y:.2f}'
            )

    def distance_from_start(self):

        dx = self.x - self.start_x
        dy = self.y - self.start_y

        return math.sqrt(
            dx * dx + dy * dy
        )

    def normalize_angle(self, angle):

        while angle > math.pi:
            angle -= 2.0 * math.pi

        while angle < -math.pi:
            angle += 2.0 * math.pi

        return angle

    def begin_turn(self):

        self.target_yaw = self.normalize_angle(
            self.yaw + math.pi / 2.0
        )

    def control_loop(self):

        if self.start_x is None:
            return

        cmd = Twist()

        # ==========================
        # SISI 1 - 4 meter
        # ==========================

        if self.state == 'FORWARD_1':

            if self.distance_from_start() < self.length:

                cmd.linear.x = self.linear_speed

            else:

                self.begin_turn()
                self.state = 'TURN_1'

                self.get_logger().info(
                    'Sisi 1 selesai - belok 90 derajat'
                )

        # ==========================
        # BELOK 1
        # ==========================

        elif self.state == 'TURN_1':

            error = self.normalize_angle(
                self.target_yaw - self.yaw
            )

            if abs(error) > 0.03:

                cmd.angular.z = self.angular_speed

            else:

                self.start_x = self.x
                self.start_y = self.y

                self.state = 'FORWARD_2'

                self.get_logger().info(
                    'Belok 1 selesai'
                )

        # ==========================
        # SISI 2 - 2 meter
        # ==========================

        elif self.state == 'FORWARD_2':

            if self.distance_from_start() < self.width:

                cmd.linear.x = self.linear_speed

            else:

                self.begin_turn()
                self.state = 'TURN_2'

                self.get_logger().info(
                    'Sisi 2 selesai - belok 90 derajat'
                )

        # ==========================
        # BELOK 2
        # ==========================

        elif self.state == 'TURN_2':

            error = self.normalize_angle(
                self.target_yaw - self.yaw
            )

            if abs(error) > 0.03:

                cmd.angular.z = self.angular_speed

            else:

                self.start_x = self.x
                self.start_y = self.y

                self.state = 'FORWARD_3'

                self.get_logger().info(
                    'Belok 2 selesai'
                )

        # ==========================
        # SISI 3 - 4 meter
        # ==========================

        elif self.state == 'FORWARD_3':

            if self.distance_from_start() < self.length:

                cmd.linear.x = self.linear_speed

            else:

                self.begin_turn()
                self.state = 'TURN_3'

                self.get_logger().info(
                    'Sisi 3 selesai - belok 90 derajat'
                )

        # ==========================
        # BELOK 3
        # ==========================

        elif self.state == 'TURN_3':

            error = self.normalize_angle(
                self.target_yaw - self.yaw
            )

            if abs(error) > 0.03:

                cmd.angular.z = self.angular_speed

            else:

                self.start_x = self.x
                self.start_y = self.y

                self.state = 'FORWARD_4'

                self.get_logger().info(
                    'Belok 3 selesai'
                )

        # ==========================
        # SISI 4 - 2 meter
        # ==========================

        elif self.state == 'FORWARD_4':

            if self.distance_from_start() < self.width:

                cmd.linear.x = self.linear_speed

            else:

                self.begin_turn()
                self.state = 'TURN_4'

                self.get_logger().info(
                    'Sisi 4 selesai - belok terakhir'
                )

        # ==========================
        # BELOK 4
        # ==========================

        elif self.state == 'TURN_4':

            error = self.normalize_angle(
                self.target_yaw - self.yaw
            )

            if abs(error) > 0.03:

                cmd.angular.z = self.angular_speed

            else:

                self.state = 'DONE'

                self.get_logger().info(
                    'PERSEGI PANJANG SELESAI!'
                )

        # ==========================
        # SELESAI
        # ==========================

        elif self.state == 'DONE':

            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.publisher.publish(cmd)


def main(args=None):

    rclpy.init(args=args)

    node = RectangleMotion()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        node.publisher.publish(Twist())

        node.destroy_node()

        rclpy.shutdown()


if __name__ == '__main__':
    main()
