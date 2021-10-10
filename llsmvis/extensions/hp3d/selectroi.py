# setup notebook
# notebook formatting
from IPython.core.display import display, HTML

display(HTML("<style>.container { width:90% !important; }</style>"))

# pretty print all cell's output and not just the last one
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
import time
import numpy as np
# imports
import pandas as pd

import bokeh
from bokeh.layouts import gridplot
from bokeh.plotting import output_notebook

output_notebook()  # set default; alternative is output_file()
# Generate linked plots + TABLE displaying data + save button to export cvs of selected data

from random import random

from bokeh.io import output_notebook  # prevent opening separate tab with graph
from bokeh.io import show

from bokeh.layouts import row
from bokeh.layouts import grid
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.models import Button  # for saving data
from bokeh.events import ButtonClick  # for saving data
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.models import HoverTool
from bokeh.plotting import figure

from matplotlib import cm
from matplotlib import colors


def select_im(im, txtstr, fnamehead='test', datapath='.', exportdinfo='False'):
    # create data
    xdim = np.int(im.shape[1])
    ydim = np.int(im.shape[0])
    [xd, yd] = np.meshgrid(np.arange(0, xdim, 20), np.arange(0, ydim, 20))
    x = list(xd.ravel())
    y = list(yd.ravel())

    pink_cmap = cm.get_cmap('pink', 256)
    pink_cmap256 = pink_cmap(np.linspace(0, 1, 256))
    palette = tuple(colors.to_hex(i) for i in pink_cmap256)

    # create first subplot
    plot_width = np.int(xdim / 2)
    plot_height = np.int(ydim / 2)

    s1 = ColumnDataSource(data=dict(x=x, y=y))
    fig01 = figure(
        plot_width=plot_width,
        plot_height=plot_height,
        tools=["lasso_select", "reset", "save"],
        title="Select Here",
    )
    fig01.circle("x", "y", source=s1, alpha=0.6)
    fig01.image(image=[im], x=0, y=0, dw=xdim, dh=ydim,
                palette=palette, level="image")
    # create second subplot
    s2 = ColumnDataSource(data=dict(x=[], y=[]))

    # demo smart error msg:  `box_zoom`, vs `BoxZoomTool`
    fig02 = figure(
        plot_width=np.int(xdim / 2),
        plot_height=np.int(ydim / 2),
        x_range=(0, xdim),
        y_range=(0, ydim),
        tools=["box_zoom", "wheel_zoom", "reset", "save"],
        title="Watch Here",
    )

    fig02.circle("x", "y", source=s2, alpha=0.6, color="firebrick")

    # create dynamic table of selected points
    columns = [
        TableColumn(field="x", title="X axis"),
        TableColumn(field="y", title="Y axis"),
    ]

    table = DataTable(
        source=s2,
        columns=columns,
        width=10,
        height=10,
        sortable=True,
        selectable=True,
        editable=True,
    )

    # fancy javascript to link subplots
    # js pushes selected points into ColumnDataSource of 2nd plot
    # inspiration for this from a few sources:
    # credit: https://stackoverflow.com/users/1097752/iolsmit via: https://stackoverflow.com/questions/48982260/bokeh-lasso-select-to-table-update
    # credit: https://stackoverflow.com/users/8412027/joris via: https://stackoverflow.com/questions/34164587/get-selected-data-contained-within-box-select-tool-in-bokeh
    s1.selected.js_on_change(
        "indices",
        CustomJS(
            args=dict(s1=s1, s2=s2, table=table),
            code="""
            var inds = cb_obj.indices;
            var d1 = s1.data;
            var d2 = s2.data;
            d2['x'] = []
            d2['y'] = []
            for (var i = 0; i < inds.length; i++) {
                d2['x'].push(d1['x'][inds[i]])
                d2['y'].push(d1['y'][inds[i]])
            }
            s2.change.emit();
            table.change.emit();

            var inds = source_data.selected.indices;
            var data = source_data.data;
            var out = "x, y\\n";
            for (i = 0; i < inds.length; i++) {
                out += data['x'][inds[i]] + "," + data['y'][inds[i]] + "\\n";
            }
            var file = new Blob([out], {type: 'text/plain'});

        """,
        ),
    )

    # create save button - saves selected datapoints to text file onbutton
    # inspriation for this code:
    # credit:  https://stackoverflow.com/questions/31824124/is-there-a-way-to-save-bokeh-data-table-content
    # note: savebutton line `var out = "x, y\\n";` defines the header of the exported file, helpful to have a header for downstream processing

    savebutton = Button(label="Save", button_type="success")
    savebutton.js_on_event(ButtonClick, CustomJS(
        args=dict(source_data=s1),
        # look into here: https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement - Xiyu
        code="""
            var inds = source_data.selected.indices;
            var data = source_data.data;
            var out = "x, y\\n";
            for (var i = 0; i < inds.length; i++) {
                out += data['x'][inds[i]] + "," + data['y'][inds[i]] + "\\n";
            }
            var file = new Blob([out], {type: 'text/plain'});
            var elem = window.document.createElement('a');
            elem.href = window.URL.createObjectURL(file);
            elem.download = '""" + fnamehead + '_' + txtstr + """.txt';
            document.body.appendChild(elem);
            elem.click();
            document.body.removeChild(elem);
            """
    )
                           )
    if exportdinfo is True:
        export_fpath_button = Button(label="export filepath", button_type="success")
        export_fpath_button.js_on_event(ButtonClick, CustomJS(
            args=dict([]),
            # look into here: https://developer.mozilla.org/en-US/docs/Web/API/Document/createElement - Xiyu
            code="""
                var out2 = " """ + datapath + """  \\n";
                var file2 = new Blob([out2], {type: 'text/plain'});
                var elem2 = window.document.createElement('a');
                elem2.href = window.URL.createObjectURL(file2);
                elem2.download = '""" + fnamehead + '_fpath' + """.txt';
                document.body.appendChild(elem2);
                elem2.click();
                document.body.removeChild(elem2);
                """
        ))
    # add Hover tool
    # define what is displayed in the tooltip
    tooltips = [("X:", "@x"), ("Y:", "@y"), ("static text", "static text")]

    fig02.add_tools(HoverTool(tooltips=tooltips))

    # display results
    # demo linked plots
    # demo zooms and reset
    # demo hover tool
    # demo table
    # demo save selected results to file
    if exportdinfo is True:
        layout = grid([fig01, fig02, table, savebutton, export_fpath_button], ncols=2, nrows=3)
    else:
        layout = grid([fig01, fig02, table, savebutton], ncols=2, nrows=3)

    output_notebook()
    show(layout)