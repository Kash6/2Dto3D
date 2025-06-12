import sys
import time
import threading
import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui

global POINTS
POINTS = []

global COLORS
COLORS = []

global graph_region
# Single Frame P Size = 0.01
# Multiple Frames P Size = 0.00001
graph_region = gl.GLScatterPlotItem(pos=np.zeros((1, 3), dtype=np.float32), color=(0, 1, 0, 0.5), size=0.00001, pxMode=False)
box = gl.GLBoxItem(size=QtGui.QVector3D(1,1,1), color=(255,255,255,80), glOptions="opaque")
print(dir(gl))


def update_graph():
    global graph_region, POINTS, COLORS
    colors = np.array(COLORS, dtype=np.float32)
    if len(POINTS) > 0:
        a = np.array(POINTS)
        graph_region.setData(pos=a, color=colors)


def start_graph():
    print("Setting up graph")
    global app, graph_region, w, g, d3, t
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.resize(800, 600)
    w.opts['distance'] = 20
    w.show()
    w.setWindowTitle('3D Scene Reconstruction')

    g = gl.GLGridItem()
    w.addItem(g)
    graph_region.rotate(90, -1, 0, 0)
    # graph_region.translate(0, 0, 2.4)
    w.addItem(graph_region)
    w.addItem(box)
    t = QtCore.QTimer()
    t.timeout.connect(update_graph)
    t.start(50)

    QtGui.QApplication.instance().exec_()
    global RUNNING
    RUNNING = False
    print("\n[STOP]\tGraph Window closed. Stopping...")

def start_scan():
    global POINTS, COLORS
    try:
        i = 0
        rot_trans = np.load(f"./SLAMOut/{i}.npy").astype(np.float128)
        rot = rot_trans[:3, :3]
        trans = rot_trans[:3, -1]
        pc = (np.load(f"./PointClouds/{i}.npy").astype(np.float128) @ rot.T ) + trans
        colorMap = np.load(f"./PointClouds/{i}_ColorMap.npy")
        POINTS = pc
        COLORS = colorMap.astype(float) / 255.0
        print(f"{i} Done. Shape = {POINTS.shape}, {COLORS.shape}")
        for i in range(1, 3):
            rot_trans = np.load(f"./SLAMOut/{i}.npy").astype(np.float128)
            rot = rot_trans[:3, :3]
            trans = rot_trans[:3, -1]
            pc = (np.load(f"./PointClouds/{i}.npy").astype(np.float128) @ rot.T ) + trans
            colorMap = np.load(f"./PointClouds/{i}_ColorMap.npy")
            POINTS = np.vstack((POINTS, pc))
            COLORS = np.vstack((COLORS, colorMap.astype(float) / 255.0))
            print(f"{i} Done. Shape = {POINTS.shape}, {COLORS.shape}")            
            time.sleep(1)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    start_scan()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        graph_thread = threading.Thread(target=start_graph, args=())
        graph_thread.daemon = True  # Daemonize thread
        start_graph()