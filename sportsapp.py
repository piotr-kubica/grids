from gui import Gui
from config import Config
from datetime import datetime, timedelta
from copy import copy
from operator import add
from functools import reduce
from timedelta_util import timedelta_from_hh_mm
from color_util import rgb_to_hex
from date_util import roll_year, date_from_str
import os.path
import csv

class Sportsapp():

    def __init__(self, date):
        self._activities = {}
        self._current_date = copy(date)
        self._selected_date = copy(date)

        # components
        self._cfg = Config()
        self._ui = Gui(date.year, sorted(self._cfg.activity_defaults_sports),
                       self._cfg.activity_defaults_headers,
                       calgrid_bg_tile_color=rgb_to_hex(self._cfg.min_color))
        # bindings
        self._ui.on_select_date(self.select_date)
        self._ui.on_over_date(self.show_date)
        self._ui.on_add(self.add_activity)
        self._ui.on_remove(self.remove_activity)
        self._ui.on_next_year(self.next_year)
        self._ui.on_prev_year(self.prev_year)
        self._ui.on_save(self.save)
        # TODO bind backup to program Exit -> in _ui.on_closing
        # self.create_backup_file()

        self.load_activities_from_file()
        self.color_grid()
        self.select_date(self._selected_date)
        
    def load_activities_from_file(self):
        filename = self._cfg.activity_filename(self._selected_date)
        if not (os.path.exists(filename) and os.path.isfile(filename)):
            open(filename, 'a').close()
        
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter='|')
            for row in reader:
                self._activities.setdefault(date_from_str(row[0]), []).append(tuple(row[1:]))

    def color_grid(self):
        for activity_date in self._activities.keys():
            self.update_calgrid_color(activity_date)
        
    def create_backup_file(self):
        # create csv file if not existing
        pass

    def save_activites_to_file(self):
        filename = self._cfg.activity_filename(self._selected_date)
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter='|')
            for date in sorted(self._activities.keys()):
                for activity in self._activities[date]:
                    act = list(activity)
                    act.insert(0, date)
                    writer.writerow(act)

    def next_year(self):
        self._selected_date = roll_year(self._selected_date, 1)
        self.change_year(self._selected_date)
              
    def prev_year(self):
        self._selected_date = roll_year(self._selected_date, -1)
        self.change_year(self._selected_date)

    def change_year(self, date):
        self._ui.load_cal_grid(date.year)
        self._ui.on_over_date(self.show_date)
        self._ui.on_select_date(self.select_date)
        self._ui.set_season_label(date.year)
        self._activities = {}
        self.load_activities_from_file()
        self.color_grid()
        self.select_date(date)

    def select_date(self, date, *_):
        self._selected_date = date
        self._ui.remove_all_activities()
        self._ui.select_date(self._selected_date)
        self._ui.set_date_label(self._selected_date)
        self._ui.set_save_status_label('Saved', 'gray')
        self.activities_load_to_table()

    def show_date(self, date, tile_id):
        # print('over: {} coords {}'.format(date, tile_id))
        self._ui._cal_grid.remove_text()
        self._ui._cal_grid.set_text_to_tile(tile_id, date.day)

    def save(self):
        activities = tuple([self.sanitize_delimiter(activity)
                            for activity in self._ui.export_workouts()])
        if activities:
            self._activities[self._selected_date] = activities
        self.update_calgrid_color(self._selected_date)
        self._ui.set_save_status_label('Saved', 'gray')
        self.save_activites_to_file()

    def sum_activity_duration(self, activities) -> timedelta:
        try:
            if not activities:
                return timedelta(0)
            duration_index = self._cfg.activity_defaults_headers.index('duration')
            activity_durations = [timedelta_from_hh_mm(activity[duration_index])
                                  for activity in activities]
            return reduce(add, activity_durations)
        except ValueError:
            return timedelta(0)

    def update_calgrid_color(self, date):
        td = self.sum_activity_duration(self._activities.get(date, []))
        self._ui.color_date(date, rgb_to_hex(self._cfg.determine_color(td)))

    def activities_load_to_table(self):
        activities = self._activities.get(self._selected_date, [])
        for activity in activities:
            self._ui.add_activity(*activity)

    def add_activity(self):
        # print(self._ui.workout_type())
        sport = self._cfg.activity_defaults_by_sport[self._ui.workout_type()]
        self._ui.add_activity(self._ui.workout_type(), sport['duration'],
                              sport['distance'], sport['intensity'], sport['description'])
        self._ui.set_save_status_label('unsaved', 'red')
        # Limit activities to 10. More is unhealthy ;)
        if self._ui.workout_count() >= 10:
            self._ui.disable_add()

    def remove_activity(self):
        removed = self._ui.remove_activity(self._ui.workout_selected())
        if removed is not None:
            self._ui.workout_reset_selection()
            self._ui.set_save_status_label('unsaved', 'red')
            self._ui.enable_add()

    def sanitize_delimiter(self, activity:tuple, delimiter='|'):
        """ removes delimiters from list of activities (tuples) """
        return [attr.replace(delimiter, '') for attr in activity]

        


s = Sportsapp(datetime.now().date())

if __name__ == "__main__":
    s._ui.loop()
