import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Rectangle
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import TextBox
from matplotlib import gridspec as gridspec
import numpy as np
from utilities import split_value, split_list, print_tree, trunc, Node, buildKdTree, query


rectangles = []


query_box = [0.4, 0.4, 0.6, 0.6]

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
txt.text(0.1, 0.95, 'number of input rectangles: ' + str(0))
txt.text(0.1, 0.9, 'query box: [' + '%.3f' % query_box[0] + "," + '%.3f' % query_box[2] + "] " + " x " + '[' + '%.3f' % query_box[1]
         + "," + '%.3f' % query_box[3] + "]")

temp_rect = [0] * 4


def txt_out(rectangles, query_box):
    txt.clear()
    txt.set_axis_off()
    txt.text(0.1, 0.95, 'number of input rectangles: ' + str(len(rectangles)))
    txt.text(0.1, 0.9, 'query box: [' + '%.3f' % query_box[0] + "," + '%.3f' % query_box[2] + "] " + " x " + '[' + '%.3f' % query_box[1]
             + "," + '%.3f' % query_box[3] + "]")


def clear():
    global query_box, rectangles
    ax.clear()
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.patches = []
    rectangles = np.array([])
    query_box = [0] * 4
    fig.canvas.draw()


############################## Add Rectangles ########################

def on_press(event):
    global temp_rect
    if not event.inaxes == ax:
        return
    if check_box.get_status()[0]:
        # print('press')
        x0 = event.xdata
        y0 = event.ydata
        temp_rect[0] = x0
        temp_rect[1] = y0


def on_release(event):
    global rectangles, temp_rect
    if not event.inaxes == ax:
        return
    if check_box.get_status()[0]:
        x0 = temp_rect[0]
        y0 = temp_rect[1]
        # print('release')
        x1 = event.xdata
        y1 = event.ydata
        if x1 != x0:
            rectangle = [0] * 4
            rectangle[0] = min(x0, x1)
            rectangle[1] = min(y0, y1)
            rectangle[2] = max(x0, x1)
            rectangle[3] = max(y0, y1)
            rectangles.append(np.array(rectangle))
            rec = Rectangle((min(x0,x1), min(y1,y0)), abs(x1-x0), abs(y1-y0), fill = None)
            ax.add_patch(rec)
            txt_out(rectangles, query_box)
            print("Added rectangle: ", trunc(np.array(rectangle), 4))
            fig.canvas.draw()


cid1 = fig.canvas.mpl_connect('button_press_event', on_press)
cid2 = fig.canvas.mpl_connect('button_release_event', on_release)
ax2 = plt.axes([0.49, 0.01, 0.18, 0.055])  # add rectangle button
check_box = CheckButtons(ax2, ['Click to Add Rectangles'], [True])


def QB(text):
    global query_box
    lst = text.split(",")
    query_box[0] = float(lst[0])
    query_box[1] = float(lst[1])
    query_box[2] = float(lst[2])
    query_box[3] = float(lst[3])
    txt_out(rectangles, query_box)


initial_text = "0.4, 0.4, 0.6, 0.6"
ax4 = plt.axes([0.10, 0.01, 0.23, 0.055])
text_box = TextBox(ax4, 'x0, y0, x1, y1: ', initial=initial_text)
text_box.on_submit(QB)




########## Build KD Tree
flag = False
def build_tree(event):
    global flag
    flag = True
    plt.close()




ax5 = plt.axes([0.34, 0.01, 0.14, 0.055])
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
    txt_out(rectangles, query_box)
    ax.patches = []
    for rec in rectangles:
        x0, y0, x1, y1 = rec[0], rec[1], rec[2], rec[3]
        rec = Rectangle((min(x0,x1), min(y1,y0)), abs(x1-x0), abs(y1-y0), fill= None)
        ax.add_patch(rec)
    fig.canvas.draw()
    root = Node()
    rectangles = np.array(rectangles)
    buildKdTree(root, rectangles, k=4)
    output = query(root, query_box, k=4)
    if 1 <= len(rectangles) <= 8:
        temp_root = Node()
        buildKdTree(temp_root, rectangles, k=4)
        print_tree(temp_root)
    if len(output) >= 1:
        for rec in output:
            x0, y0, x1, y1 = rec[0], rec[1], rec[2], rec[3]
            rec = Rectangle((min(x0, x1), min(y1, y0)), abs(x1 - x0), abs(y1 - y0), fill=None, edgecolor="red")
            ax.add_patch(rec)
        print(str(len(output)) + " rectangles in the query box. Those rectangles are:")
        print(trunc(output, 4))
        txt.text(0.1, 0.85, str(len(output)) + " rectangles in the query box, they are marked in red.")
    else:
        print("No rectangle in the query box.")
    plt.show()
