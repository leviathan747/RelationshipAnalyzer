import ui
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from io import BytesIO


# student functions
def get_slope(x1, y1, x2, y2):
    # Student implements
    deltay = y2 - y1
    deltax = x2 - x1
    m = deltay / deltax
    return m


def get_y_intercept(m, x, y):
    # Student implements
    mx = m * x
    b = y - mx
    return b


def plot_point(m, b, x):
    # Student implements
    mx = m * x
    y = mx + b
    return (x, y)


def is_linear(points):
    last_roc = None
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        roc = (y2 - y1) / (x2 - x1)
        if last_roc is None:
            last_roc = roc
        elif not math.isclose(roc, last_roc):
            return False
    return True


def is_proportional(points):
    last_k = None
    for i in range(len(points)):
        x, y = points[i]
        if x != 0:
            k = y / x
            if last_k is None:
                last_k = k
            elif not math.isclose(k, last_k):
                return False
        elif y != 0:
            return False  # y-intercept is not 0
    return True


def linear_regression(points):
    x, y = list(zip(*points))
    x2 = list(map(lambda x: x ** 2, x))
    xy = list(map(lambda p: p[0] * p[1], points))
    b = (sum(y)*sum(x2) - sum(x)*sum(xy)) / (len(points)*sum(x2) - sum(x)**2)
    m = (len(points)*sum(xy) - sum(x)*sum(y)) / (len(points)*sum(x2) - sum(x)**2)
    return m, b


v = None    # a reference to the top level view
data = ''   # the current saved data


class TextViewDelegate:
    def textview_did_change(self, textview):
        # data validation
        valid = self.validate(textview)

        # color the text red if it's not updated and enabled/disable
        # the update button
        if not valid:
            textview.text_color = 'red'
            v['update_button'].enabled = False
            v['error_message'].text = 'Enter 2 numbers separated by a space on each line. You need at least 2 points.'
        else:
            v['error_message'].text = ''
            if data != textview.text:
                textview.text_color = 'blue'
                v['update_button'].enabled = True
            else:
                textview.text_color = 'black'
                v['update_button'].enabled = False

    def validate(self, textview):
        try:
            points = parse_data(textview.text)
            if len(points) < 2:
                return False
            for p in points:
                if len(p) > 2:
                    return False
        except ValueError:
            return False
        return True


def parse_data(text):
    points = []
    for line in text.splitlines():
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

    # set default min and max values
    minx, maxx = -10, 10
    miny, maxy = -10, 10
    plt.xlim((minx, maxx))
    plt.ylim((miny, maxy))

    # turn on grid
    ax = plt.subplot(111)
    majorx, minorx = max((maxx - minx) // 10, 1), max((maxx - minx) // 20, 1)
    majory, minory = max((maxy - miny) // 10, 1), max((maxy - miny) // 20, 1)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(majorx))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(minorx))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(majory))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(minory))
    plt.grid(b=True)

    # handle the points
    if len(points) > 0:
        # unpack the points
        xs, ys = zip(*points)

        # re-calculate the min and max, ticks
        if min(xs) < minx or max(xs) > maxx or min(ys) < miny or max(ys) > maxy:
            minx, maxx = min(xs) - 0.2 * (max(xs) - min(xs)), max(xs) + 0.2 * (max(xs) - min(xs))
            miny, maxy = min(ys) - 0.2 * (max(ys) - min(ys)), max(ys) + 0.2 * (max(ys) - min(ys))
            majorx, minorx = max((maxx - minx) // 10, 1), max((maxx - minx) // 20, 1)
            majory, minory = max((maxy - miny) // 10, 1), max((maxy - miny) // 20, 1)
            plt.xlim((minx, maxx))
            plt.ylim((miny, maxy))
            ax.xaxis.set_major_locator(ticker.MultipleLocator(majorx))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(minorx))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(majory))
            ax.yaxis.set_minor_locator(ticker.MultipleLocator(minory))

        # plot each point
        plt.scatter(xs, ys)
        for x, y in zip(xs, ys):
            ax.annotate(f'({x:.1g}, {y:.1g})', (x + minorx/4, y - minory/2))

        # if there is more than one point, draw the line
        if len(points) > 1:
            # if it is linear, calculate the slope and y-intercept
            if is_linear(points):
                m = get_slope(*points[0], *points[1])
                b = get_y_intercept(m, *points[0])
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
                # calculate a linear regression
                m, b = linear_regression(points)
                # set the is_linear label
                v['is_linear_label'].text = 'linear: No'
                v['is_linear_label'].text_color = 'red'
                # set the is_proportional label
                v['is_proportional_label'].text = 'proportional: N/A'
                v['is_proportional_label'].text_color = 'black'

            # plot the line
            x0 = (minx, maxx)
            y0 = tuple(m * x + b for x in x0)
            label = 'y = '
            if m != 0:
                if m == 1:
                    label += 'x'
                else:
                    label += f'{m:.1g}x'
            if b != 0:
                if b < 0:
                    label += f' - {-b:.1g}'
                else:
                    label += f' + {b:.1g}'
            plt.plot(x0, y0, label=label)

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
    v['input_data'].keyboard_type = ui.KEYBOARD_NUMBER_PAD

    def _update(sender=None):
        global data
        data = v['input_data'].text
        v['input_data'].delegate.textview_did_change(v['input_data'])
        update_plot(parse_data(data))
    v['update_button'].action = _update
    update_plot()
    v.present('sheet')
