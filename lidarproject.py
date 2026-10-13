import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

app = QtWidgets.QApplication([])

window = pg.plot(title="LiDAR 2D Test")
window.setLabel("bottom", "X (meters)")
window.setLabel("left", "Y (meters)")
window.setXRange(-5, 5)
window.setYRange(-5, 5)

person_x = 0
person_y = 0

def update():
    top_x = np.random.uniform(-4, 4, 30)
    top_y = np.full(30, 3)

    bottom_x = np.random.uniform(-4, 4, 30)
    bottom_y = np.full(30, -3)

    right_y = np.random.uniform(-3, 3, 30)
    right_x = np.full(30, 4)

    left_y = np.random.uniform(-3, 3, 30)
    left_x = np.full(30, -4)

    window.clear()
    window.plot(top_x, top_y, pen=None, symbol='x', symbolSize=10)
    window.plot(bottom_x, bottom_y, pen=None, symbol='x', symbolSize=10)
    window.plot(right_x, right_y, pen=None, symbol='x', symbolSize=10)
    window.plot(left_x, left_y, pen=None, symbol='x', symbolSize=10)
    while person_x < 5:
        person_x += 0.1
        person_points_x = np.random.uniform(person_x - 0.3, person_x + 0.3, 15)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)

update()
app.exec()