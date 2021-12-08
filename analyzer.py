import ui
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from io import BytesIO

# student functions
def is_linear(points):
    return True  # TODO

def is_proportional(points):
    return False  # TODO
    pass

def get_slope(p1, p2):
    return (p2.y - p1.y) / (p2.x - p1.x)

def get_y_intercept(m, point):
    return point.y - m * point.x

def plot_point(m, b, x):
    return (x, m * x + b)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

v = None    # a reference to the top level view
data = ''   # the current saved data


class TextViewDelegate:
    def textview_did_change(self, textview):
        # TODO data validation

        # color the text red if it's not updated and enabled/disable the update button
        if data != textview.text:
            textview.text_color = 'red'
            v['update_button'].enabled = True
        else:
            textview.text_color = 'black'
            v['update_button'].enabled = False

def parse_data():
    points = []
    for line in data.splitlines():
        raw_x, raw_y = line.split()
        x, y = float(raw_x), float(raw_y)
        points.append((x, y))
    return points


# update the plot and labels
def update_plot(points=[]):
    # clear the plot
    plt.clf()

    # make the plot square (it will scale down)
    plt.figure(figsize=(7, 7))

    # draw axes
    plt.axvline(color='k')
    plt.axhline(color='k')

    # turn on grid
    ax = plt.subplot(111)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    plt.grid(b=True)

    # set default min and max values
    minx, maxx = -10, 10
    miny, maxy = -10, 10
    plt.xlim((minx, maxx))
    plt.ylim((miny, maxy))

    # handle the points
    if len(points) > 0:
        # unpack the points
        xs, ys = zip(*points)

        # re-calculate the min and max
        # TODO
        plt.xlim((minx, maxx))
        plt.ylim((miny, maxy))

        # plot each point
        plt.scatter(xs, ys)

        # if there is more than one point, draw the line
        if len(points) > 1:
            # if it is linear, calculate the slope and y-intercept
            if is_linear(points):
                m = get_slope(Point(*points[0]), Point(*points[1]))
                b = get_y_intercept(m, Point(*points[0]))
                # set the is_linear label
                v['is_linear_label'].text = 'linear: Yes'
                v['is_linear_label'].text_color = 'green'
                # set the is_proportional label
                if is_proportional(points):
                    v['is_proportional_label'].text = 'proportional: Yes'
                    v['is_proportional_label'].text_color = 'green'
                else:
                    v['is_proportional_label'].text = 'proportional: No'
                    v['is_proportional_label'].text_color = 'red'
            else:
                # set the is_linear label
                v['is_linear_label'].text = 'linear: No'
                v['is_linear_label'].text_color = 'red'
                # calculate a linear regression
                # TODO
                pass

            # plot the line
            x0 = (minx, maxx)
            y0 = tuple(m * x + b for x in x0)
            plt.plot(x0, y0, label=f'y = {m:.1f}x {"-" if b < 0 else "+"} {b:.1f}')

            # turn on the legend
            plt.legend(loc='best')

    # update the image view
    b = BytesIO()
    plt.savefig(b)
    img = ui.Image.from_data(b.getvalue())
    v['graph'].content_mode = ui.CONTENT_SCALE_ASPECT_FIT
    v['graph'].image = img

# define a variable for the top level view
v = None

if __name__ == '__main__':
    v = ui.load_view()
    v['input_data'].delegate = TextViewDelegate()
    def _update(sender=None):
        global data
        data = v['input_data'].text
        v['input_data'].delegate.textview_did_change(v['input_data'])
        update_plot(parse_data())
    v['update_button'].action = _update
    update_plot()
    v.present('sheet')
