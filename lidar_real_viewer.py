#!/usr/bin/env python3

import sys
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore


class LidarViewer(Node):
    def __init__(self):
        super().__init__("lidar_real_viewer")

        self.latest_xy = None
        self.received_cloud = False
        self.point_count = 0

        self.subscription = self.create_subscription(
            PointCloud2,
            "/velodyne_points",
            self.pointcloud_callback,
            10,
        )

        self.get_logger().info(
            "Waiting for real point-cloud data on /velodyne_points"
        )

    def pointcloud_callback(self, msg):
        try:
            points = point_cloud2.read_points(
                msg,
                field_names=("x", "y", "z"),
                skip_nans=True,
            )

            if points is None or len(points) == 0:
                self.latest_xy = np.empty((0, 2), dtype=np.float32)
                self.received_cloud = True
                self.point_count = 0
                return

            # ROS 2 returns a structured NumPy array.
            x = np.asarray(points["x"])
            y = np.asarray(points["y"])
            z = np.asarray(points["z"])

            # Keep finite measurements within a 10 m horizontal radius.
            valid = (
                np.isfinite(x)
                & np.isfinite(y)
                & np.isfinite(z)
                & (x * x + y * y <= 100.0)
            )

            self.latest_xy = np.column_stack((x[valid], y[valid]))
            self.point_count = int(np.count_nonzero(valid))
            self.received_cloud = True

        except Exception as exc:
            self.get_logger().error(
                f"Point-cloud processing failed: {exc}"
            )


def main():
    rclpy.init()
    node = LidarViewer()

    app = QtWidgets.QApplication(sys.argv)

    window = pg.PlotWidget(title="Velodyne VLP-16 — Live Room View")
    window.setLabel("bottom", "X", units="m")
    window.setLabel("left", "Y", units="m")
    window.setXRange(-10, 10)
    window.setYRange(-10, 10)
    window.setAspectLocked(True)
    window.showGrid(x=True, y=True, alpha=0.3)

    points_plot = window.plot(
        [],
        [],
        pen=None,
        symbol="o",
        symbolSize=3,
        symbolBrush=(80, 200, 255, 180),
    )

    status = QtWidgets.QLabel(
        "WAITING FOR LIDAR — listening on /velodyne_points"
    )

    container = QtWidgets.QWidget()
    container.setWindowTitle("Live VLP-16 Room Viewer")
    layout = QtWidgets.QVBoxLayout(container)
    layout.addWidget(status)
    layout.addWidget(window)
    container.resize(900, 850)
    container.show()

    def update():
        # Process ROS messages without blocking the GUI.
        rclpy.spin_once(node, timeout_sec=0.0)

        if node.received_cloud and node.latest_xy is not None:
            xy = node.latest_xy

            points_plot.setData(
                xy[:, 0],
                xy[:, 1],
            )

            status.setText(
                f"REAL LIDAR DATA | Displayed points: {node.point_count}"
            )

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(30)

    try:
        exit_code = app.exec()
    finally:
        timer.stop()
        node.destroy_node()
        rclpy.shutdown()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
