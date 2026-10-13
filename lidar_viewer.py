import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore

app = QtWidgets.QApplication(sys.argv)

window = pg.PlotWidget(title="VLP-16 | Top-Down Room View")
window.setLabel("bottom", "X", units="m")
window.setLabel("left", "Y", units="m")
window.setXRange(-5, 5)
window.setYRange(-5, 5)
window.setAspectLocked(True)
window.showGrid(x=True, y=True, alpha=0.3)

points_plot = window.plot(
    [], [],
    pen=None,
    symbol="o",
    symbolSize=3
)

status = QtWidgets.QLabel("SIMULATION MODE — no physical LiDAR data")
layout = QtWidgets.QVBoxLayout()
container = QtWidgets.QWidget()
container.setLayout(layout)
layout.addWidget(status)
layout.addWidget(window)
container.resize(800, 800)
container.setWindowTitle("LiDAR Room Viewer")
container.show()

# Temporary simulated points; replace with ROS 2 data later.
def update():
    angle = np.random.uniform(0, 2 * np.pi, 500)
    distance = np.random.uniform(0.5, 4.5, 500)

    x = distance * np.cos(angle)
    y = distance * np.sin(angle)

    points_plot.setData(x, y)
    status.setText("SIMULATION MODE — no physical LiDAR data")

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)

update()
sys.exit(app.exec())