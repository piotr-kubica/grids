import json
import csv
from timedelta_util import timedelta_from_hh_mm


class Config:

    def __init__(self):
        self._config = self.read_config('config.json')
        ad_filename = self._config['app']['activity_defaults']
        self._act_defaults = self.read_activity_defaults(ad_filename)

    def read_config(self, config_file):
        with open(config_file) as json_file:
            return json.load(json_file)

    def read_activity_defaults(self, filename):
        with open(filename, 'r') as f:
            return [list(map(str.strip, row)) for row in list(csv.reader(f, delimiter='|'))]

    def activity_filename(self, date):
        return "{}_{}.csv".format(self._config['app']['csv_prefix'],
                                  date.year)

    def backup_filename(self, date):
        return "{}_{}-{}-{}.csv".format(self.backup_path,
                                        self._config['app']['csv_prefix'],
                                        date.year,
                                        date.month,
                                        date.day)
    
    def determine_color(self, td):
        """
        takes timedelta and determines color based on config file
        """
        dur_col = self._config['app']['colors_rgb']
        color_keys = sorted(dur_col.keys())
        matching_key = color_keys[0]
        for dur in color_keys:
            if timedelta_from_hh_mm(dur) <= td:
                matching_key = dur
            else:
                break
        colors = dur_col[matching_key]
        # list of str -> list of int
        return list(map(int, colors))

    @property
    def min_color(self):
        dur_col = self._config['app']['colors_rgb']
        color_keys = sorted(dur_col.keys())
        return list(map(int, dur_col[color_keys[0]]))

    @property
    def backup_path(self):
        return self._config['app']['backup_path']

    @property
    def max_table_size(self):
        return 5

    @property
    def activity_defaults_data(self):
        return self._act_defaults[1:]

    @property
    def activity_defaults_headers(self):
        return [header.strip() for header in self._act_defaults[0]]

    @property
    def activity_defaults_sports(self):
        return [ad[0] for ad in self.activity_defaults_data]

    @property
    def activity_defaults_by_sport(self):
        # skip 'sport' header and trim
        header_list = [h.strip() for h in self.activity_defaults_headers[1:]]
        # create nested dict
        # sport_header:{csv_header:csv_value}
        # ex, {run: {time: 00:30, intensity: 3}, bike:...}
        return {row[0]: dict(zip(header_list, [r.strip() for r in row[1:]]))
                for row in self.activity_defaults_data}

