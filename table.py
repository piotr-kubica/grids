from tkinter import Frame, Label, StringVar, Entry, Grid


class CellInput(Entry):

    def __init__(self, parent, row, col, borderwidth=0, relief="flat", **kwargs):
        Entry.__init__(self, parent, relief=relief, borderwidth=borderwidth, **kwargs)
        self._parent = parent
        self._row = row
        self._col = col
        self._init_on_click()

    def move_one_row_up(self):
        self._row -= 1
        self.grid()
        
    def grid(self, **options):
        options['row'] = self._row
        options['column'] = self._col
        options['sticky'] = 'snwe'
        super().grid(options)

    def set_text(self, value):
        super().delete(0, 'end')
        super().insert(0, value)

    def _init_on_click(self):
        def select_row(event):
            if self._parent:
                self._parent.select_row(self._row)
        self.bind("<Button-1>", select_row)


class Table(Frame):

    # cols = ({'label': 'Hello world', 'justify': 'left'})
    def __init__(self, parent=None, cols=None, row_height=22):
        Frame.__init__(self, parent)
        self._rows = []
        self._row_height = row_height
        self._cols = cols
        self._on_select_callback = None
        self._on_change_callback = None
        self._init_header(self._cols)
        self._last_selected = None
        # expand last column to fill width
        Grid.columnconfigure(self, len(cols)-1, weight=1)

    def pack(self, **options):
        options['side'] = options.get('side', 'left')
        options['fill'] = options.get('fill', 'both')
        options['expand'] = options.get('expand', True)
        super().pack(options)

    def add_row(self, *values):
        # because header takes 1 row
        new_row_grid_index = len(self._rows) + 1
        new_row = []
        self._rows.append(new_row)
        for i, col in enumerate(self._cols):
            cell_text = StringVar()
            cell = CellInput(self, row=new_row_grid_index, col=i,
                             textvariable=cell_text, justify=col.get('justify'))
            cell.grid()
            new_row.append(cell)
            # set cell text values
            if i < len(values):
                cell_text.set(values[i])
        Grid.rowconfigure(self, new_row_grid_index, minsize=self._row_height)
        # calls callback with operation-type, value and row index
        if self._on_change_callback:
            self._on_change_callback('add', values, new_row_grid_index)
        return new_row

    def delete_row(self, row_grid_index):
        if row_grid_index is None:
            return None

        # user inputs index with offset starting from 1
        # because header takes 1 row
        row_nr = row_grid_index - 1

        if row_nr >= len(self._rows) or row_nr < 0:
            return None

        row_to_del = self._rows.pop(row_nr)
        removed_row_values = []
        for cell in row_to_del:
            removed_row_values.append(cell.get())
            cell.grid_forget()

        for i, row in enumerate(self._rows):
            if i >= row_nr:
                for cell in row:
                    cell.move_one_row_up()

        # calls callback with operation-type and removed values in row
        if self._on_change_callback:
            self._on_change_callback('delete', tuple(removed_row_values))

        return removed_row_values

    def clear_table(self):
        while len(self._rows):
            self.delete_row(1)

    def select_row(self, row_nr):
        self._last_selected = row_nr
        if self._on_select_callback:
            self._on_select_callback(self.export())

    def export(self):
        output = []
        for row in self._rows:
            cell_values = tuple([cell.get() for cell in row])
            output.append(cell_values)
        return output

    def load(self, list_of_tuples):
        for values in list_of_tuples:
            self.add_row(*values)

    def size(self):
        return len(self._rows)
            
    def on_row_select(self, callback):
        self._on_select_callback = callback

    def on_add_or_remove(self, callback):
        self._on_change_callback = callback

    @property
    def last_selected(self):
        return self._last_selected

    def reset_selected(self):
        self._last_selected = None

    def _init_header(self, cols):
        for i, col in enumerate(cols):
            label = Label(self, text=col.get('label', 'Label'.join(str(i))),
                          justify="center", relief="groove")
            label.grid(row=0, column=i, sticky='snwe', ipadx=15)
        # retuns last col
        return col
