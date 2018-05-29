from tkinter import Button, Frame, Label, OptionMenu, StringVar, Tk
from tkinter import messagebox
from calendargrid import CalendarGrid
from table import Table


class Gui:

    def __init__(self, year, sports, headers, calgrid_bg_tile_color):
        self._main_window = Tk()
        self._main_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._init_layout(year, sports, headers, calgrid_bg_tile_color)
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._main_window.destroy()

    def loop(self):
        self._main_window.mainloop()

    #########################################################################
    # api
    #########################################################################

    def load_cal_grid(self, year):
        if self._cal_grid:
            self._cal_grid.destroy()
        self._cal_grid = CalendarGrid(self._cont_calendar)
        self._cal_grid.create_grid_year(year)
        self._cal_grid.pack(padx=20, pady=20)

    def select_date(self, date):
        """
        selects calendargrid date and update date label
        """
        self._cal_grid.selected(date)

    def set_date_label(self, date):
        self._date_lbl.config(text='Date: {}'.format(str(date)))

    def set_season_label(self, year):
        self._season_lbl.config(text=str(year))

    def set_save_status_label(self, text, color='green'):
        self._sync_save_status.config(text=text, fg=color)

    def add_activity(self, *values):
        """
        fills new column with values
        """
        self._table.add_row(*values)

    def load_activities(self, activitity_list):
        """
        loads activity into table
        """
        for activitity in activitity_list:
            self._table.add_row(activitity)

    def remove_activity(self, activity_index):
        """
        removes activitity from table by index
        """
        return self._table.delete_row(activity_index)

    def remove_all_activities(self):
        """
        cleans activity table
        """
        self._table.clear_table()

    def color_date(self, date, color_rgb):
        """
        sets color to calendargrid field by date
        """
        self._cal_grid.set_tile_color_rgb(date, color_rgb)
        
    def workout_type(self):
        """
        returns workout type from dropdown with corresponding default values
        """
        return self._workout_choice.get()

    def workout_selected(self):
        """
        returns index of selected workout from table
        """
        return self._table.last_selected

    def export_workouts(self):
        """
        returns activities in rows from table as list of tuples
        """
        return self._table.export()
    
    def workout_reset_selection(self):
        """
        sets selection to None
        """
        self._table.reset_selected()

    def workout_count(self):
        return self._table.size()

    def disable_add(self):
        self._add_btn.config(state="disabled")

    def enable_add(self):
        self._add_btn.config(state="normal")

    #########################################################################
    # callbacks
    #########################################################################
    
    def on_remove(self, callback):
        self._remove_btn.config(command=callback)

    def on_add(self, callback):
        self._add_btn.config(command=callback)

    def on_save(self, callback):
        self._save_btn.config(command=callback)

    def on_select_date(self, callback):
        self._cal_grid.bind_tiles_callback(callback, event_trigger='<Button-1>')

    def on_over_date(self, callback):
        self._cal_grid.bind_tiles_callback(callback, event_trigger='<Enter>')
        
    def on_workout_select(self, callback):
        pass

    def on_workout_type_selected(self, callback):
        pass

    def on_next_year(self, callback):
        self._next_btn.config(command=callback)

    def on_prev_year(self, callback):
        self._prev_btn.config(command=callback)

    #########################################################################
    # init
    #########################################################################

    def _init_layout(self, year, sports, headers, calgrid_bg_tile_color):
        # top level
        grid_container = Frame(self._main_window)
        grid_container.pack(fill='both', expand=True, padx=20)

        # 0
        year_nav_containter = Frame(grid_container)
        year_nav_containter.grid(row=0, column=1, columnspan=20, pady=10)
        self._prev_btn = Button(year_nav_containter, text="<")
        self._prev_btn.pack(side="left")
        self._season_lbl = Label(year_nav_containter, text="2018")
        self._season_lbl.pack(side="left", padx=10)
        self._next_btn = Button(year_nav_containter, text=">")
        self._next_btn.pack(side="left")

        # 1
        # calendar grid
        self._cont_calendar = Frame(grid_container)
        self._cont_calendar.grid(row=1, column=1, columnspan=20, sticky='nsew')

        self._cal_grid = CalendarGrid(self._cont_calendar, tile_bg=calgrid_bg_tile_color)
        self._cal_grid.create_grid_year(year)
        self._cal_grid.pack(padx=20, pady=20)

        # 2
        # TODO summary charts

        # 3
        # buttons
        self._date_lbl = Label(grid_container, text="Date: ")
        self._date_lbl.grid(row=3, column=1, sticky="w", pady=10)

        # 4
        # dropdown for default sport
        self._workout_choice = StringVar(grid_container)
        self._workout_choice.set(sports[0])

        self._workout_type = OptionMenu(grid_container, self._workout_choice, *sports)
        self._workout_type.grid(row=4, column=17, sticky="e")
        
        self._add_btn = Button(grid_container, text="Add")
        self._add_btn.grid(row=4, column=18, sticky="e")

        # TODO sync button
        # sync_btn = Button(grid_container, text="Sync")
        # sync_btn.grid(row=4, column=1, sticky="w")

        self._save_btn = Button(grid_container, text="Save")
        self._save_btn.grid(row=4, column=19, sticky="e")
        
        self._sync_save_status = Label(grid_container, text="Saved")
        self._sync_save_status.grid(row=4, column=20, sticky="w", padx=(10, 0))
        self._sync_save_status.config(fg='green')

        # 5
        # table
        cont_table = Frame(grid_container)
        cont_table.grid(row=5, column=1, columnspan=20, pady=10, sticky='nsew')
        # TODO take headers (Capitalize) and zip with 'label'
        self._table = Table(cont_table, ({'label': 'Sport'},
                                         {'label': 'Duration'},
                                         {'label': 'Distance'},
                                         {'label': 'Intensity'},
                                         {'label': 'Description'}))
        self._table.pack(fill='both', expand=True)

        # 6
        # bottom
        self._remove_btn = Button(grid_container, text="Remove")
        self._remove_btn.grid(row=6, column=20, sticky='nsew', pady=10)
