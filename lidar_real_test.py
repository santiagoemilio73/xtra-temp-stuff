import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2


class LidarTest(Node):
    def __init__(self):
        super().__init__('lidar_test')

        self.subscription = self.create_subscription(
            PointCloud2,
            '/points',
            self.pointcloud_callback,
            10
        )

        self.get_logger().info('Waiting for LiDAR point cloud on /points...')

    def pointcloud_callback(self, msg):
        self.get_logger().info(
            f'Received point cloud: {msg.width * msg.height} points'
        )


def main():
    rclpy.init()
    node = LidarTest()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()