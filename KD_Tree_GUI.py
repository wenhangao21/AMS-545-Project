import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Rectangle
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import TextBox
from matplotlib import gridspec as gridspec
import numpy as np
from utilities import split_value, split_list, print_tree, trunc, Node, buildKdTree, query


pts_x = np.array([])
pts_y = np.array([])
rectangle = [0] * 4

fig = plt.figure(figsize=(13, 8))
ax = fig.add_subplot(111)
plt.title("KD-Tree Implementation")
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])

gs = gridspec.GridSpec(1, 3)
ax.set_position(gs[0:2].get_position(fig))
ax.set_subplotspec(gs[0:2])
txt = fig.add_subplot(gs[2])
txt.set_axis_off()
txt.text(0.1, 0.95, 'number of points: ' + str(0))
txt.text(0.1, 0.9, 'rectangle: [' + '%.3f' % rectangle[0] + "," + '%.3f' % rectangle[2] + "] " + " x " + '[' + '%.3f' % rectangle[1]
         + "," + '%.3f' % rectangle[3] + "]")


def txt_out(pts_x, rectangle):
    txt.clear()
    txt.set_axis_off()
    txt.text(0.1, 0.95, 'number of points: ' + str(len(pts_x)))
    txt.text(0.1, 0.9, 'rectangle: [' + '%.3f' % rectangle[0] + "," + '%.3f' % rectangle[2] + "] " + " x " + '[' + '%.3f' % rectangle[1]
             + "," + '%.3f' % rectangle[3] + "]")


def clear():
    global pts_y, pts_x
    ax.clear()
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.patches = []
    pts_x = np.array([])
    pts_y = np.array([])
    ax.plot(pts_x, pts_y, '.', 5, color='tan')
    fig.canvas.draw()


############################## Add Points ########################

def onclick(event):
    if not event.inaxes == ax:
        return
    global pts_y, pts_x
    if check_box.get_status()[0] and not check_box2.get_status()[0]:
        print('Input point: (%f, %f)' %
              (event.xdata, event.ydata))
        # store the points in a list
        pts_x = np.append(pts_x, event.xdata)
        pts_y = np.append(pts_y, event.ydata)
        ax.plot(event.xdata, event.ydata, '.', 5, color='tan')
        txt_out(pts_x, rectangle)
        fig.canvas.draw()


cid = fig.canvas.mpl_connect('button_press_event', onclick)
ax2 = plt.axes([0.52, 0.01, 0.14, 0.055])  # add points button
check_box = CheckButtons(ax2, ['Click to Add Points'], [True])


############## Press for Rectangle ###########################
def on_press(event):
    global rectangle
    if not event.inaxes == ax:
        return
    if not check_box.get_status()[0] and check_box2.get_status()[0]:
        print('press')
        x0 = event.xdata
        y0 = event.ydata
        rectangle[0] = x0
        rectangle[1] = y0


def on_release(event):
    global rectangle
    if not event.inaxes == ax:
        return
    if not check_box.get_status()[0] and check_box2.get_status()[0]:
        x0 = rectangle[0]
        y0 = rectangle[1]
        print('release')
        x1 = event.xdata
        y1 = event.ydata
        rectangle[0] = min(x0, x1)
        rectangle[1] = min(y0, y1)
        rectangle[2] = max(x0, x1)
        rectangle[3] = max(y0, y1)
        ax.patches = []
        rec = Rectangle((min(x0,x1), min(y1,y0)), abs(x1-x0), abs(y1-y0))
        ax.add_patch(rec)
        txt_out(pts_x, rectangle)
        fig.canvas.draw()


cid2 = fig.canvas.mpl_connect('button_press_event', on_press)
cid3 = fig.canvas.mpl_connect('button_release_event', on_release)

ax3 = plt.axes([0.38, 0.01, 0.13, 0.055])
check_box2 = CheckButtons(ax3, ['Select Rectangle'], [False])


################ Random Points #################
def rand_pts(text):
    global pts_y, pts_x, rectangle
    if not check_box.get_status()[0] and not check_box2.get_status()[0]:
        ax.clear()
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        rectangle = [0] *4
        n = int(text)
        pts_x = np.random.uniform(0, 1, n)
        pts_y = np.random.uniform(0, 1, n)
        ax.plot(pts_x, pts_y, '.', 5, color='tan')
        txt_out(pts_x, rectangle)
        fig.canvas.draw()


initial_text = 100
ax4 = plt.axes([0.10, 0.01, 0.03, 0.055])
text_box = TextBox(ax4, 'Random Points: ', initial=initial_text)
text_box.on_submit(rand_pts)


# ########## Build KD Tree
flag = False
def build_tree(event):
    global flag
    flag = True
    plt.close()




ax5 = plt.axes([0.18, 0.01, 0.14, 0.055])
button_build_KD_tree = Button(ax5, "Build KD-Tree and Query")
button_build_KD_tree.on_clicked(build_tree)

fig.canvas.set_window_title('KD Tree Implementation')
plt.show()

############### After Tree is built ################
if flag:
    fig = plt.figure(figsize=(13, 8))
    ax = fig.add_subplot(111)
    plt.title("KD-Tree Implementation")
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    gs = gridspec.GridSpec(1, 3)
    ax.set_position(gs[0:2].get_position(fig))
    ax.set_subplotspec(gs[0:2])
    txt = fig.add_subplot(gs[2])
    txt.set_axis_off()
    txt_out(pts_x,rectangle)
    ax.plot(pts_x, pts_y, '.', 5, color='tan')
    points = np.column_stack((pts_x, pts_y))
    root = Node()
    buildKdTree(root, points)
    # print truncated if small case
    if 1 <= len(pts_x) <= 8:
        temp_root = Node()
        buildKdTree(temp_root, points)
        print_tree(temp_root)
    output = query(root, rectangle)
    if len(output) >= 1:
        out_x = output[:, 0]
        out_y = output[:, 1]
        ax.plot(out_x, out_y, '.', 5, color='red')
        print(str(len(output)) + " points in the query rectangle. Those points are:")
        print(trunc(output, 3))
        txt.text(0.1, 0.85, str(len(output)) + " points in the query rectangle, they are marked in red.")
    else:
        print("No point in the query rectangle.")
    plt.show()
