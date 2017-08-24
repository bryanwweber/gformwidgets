import time
from io import BytesIO

from IPython import display
import gspread  # noqa: I201
import numpy as np  # noqa: I201
from oauth2client.service_account import ServiceAccountCredentials as SAC  # noqa: I201, N814
import pandas as pd  # noqa: I201
import ipywidgets as widgets  # noqa: I201
from bqplot import (
    Axis, Bars,  Figure, LinearScale, OrdinalScale,
)
import segno


def draw_graph(sheet_name='', question=''):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SAC.from_json_keyfile_name('me-2233-fall-2017-60cc76fc6b82.json', scope)
    gc = gspread.authorize(credentials)
    workbook = gc.open(sheet_name)
    sheet = workbook.sheet1
    # fig, ax = plt.subplots()

    def first_time():
        percentage, names = update_data(sheet, question)
        x_ord = OrdinalScale(domain=names)
        y_sc = LinearScale()

        bar = Bars(x=names, y=percentage, scales={'x': x_ord, 'y': y_sc})

        ax_x = Axis(scale=x_ord, grid_lines='solid', label='')
        ax_y = Axis(scale=y_sc, orientation='vertical', grid_lines='solid', label='Percent')
        fig = Figure(marks=[bar], axes=[ax_x, ax_y], title=question)
        return fig

    def update(b):
        if not cb.value:
            percentage, names = update_data(sheet, question)
            print(percentage)
            update_plot(percentage, names, fig)
        else:
            while True:
                try:
                    percentage, names = update_data(sheet, question)
                    update_plot(percentage, names, fig)
                    time.sleep(5)
                except KeyboardInterrupt:
                    break

    def update_data(sheet, question):
        data = pd.DataFrame(sheet.get_all_records())
        data.replace('', np.nan, inplace=True)
        if question not in data.columns:
            return [], []
        data.dropna(subset=[question], inplace=True)
        groups = data.groupby(question)
        percentage = [len(group)/len(data.index)*100 for _, group in groups]
        names = [name for name, _ in groups]
        return percentage, names

    def update_plot(percentage, names, fig):
        fig.axes[0].scale.domain = names
        fig.marks[0].x = names
        fig.marks[0].y = percentage

    b = widgets.Button(
        description='Update Plot',
        disabled=False,
    )
    b.on_click(update)
    cb = widgets.Checkbox(
        value=False,
        description='Update Continuously',
        disabled=False,
    )
    fig = first_time()
    h = widgets.VBox([widgets.HBox([b, cb]), fig])
    display.display(h)


def create_qr(link='', scale=20):
    s = segno.make(link, micro=False)
    b = BytesIO()
    s.save(b, kind='svg', scale=scale)
    display.display(display.SVG(b.getvalue().decode('UTF-8')))
