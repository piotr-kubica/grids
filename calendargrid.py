from tkinter import Canvas, Frame
import calendar
from datetime import datetime


class CalendarGrid(Frame):
    MONTH_RANGE = range(1, 13)
    POS_0 = 1
    
    def __init__(self, parent=None, tile_size=22,
                 bg='#d9d9d9', tile_bg='#f2f2f2', outline='#d0d0d0', separator='black',):
        Frame.__init__(self, parent)
        self._calgrid = Canvas(self, bg=bg, bd=0,
                               width=54*tile_size+2, height=7*tile_size+2)
        self._tbg = tile_bg
        self._tsize = tile_size
        self._toutline = outline
        self._tsepar = separator
        self._date_tile = {}
        self._tile_date = {}
        self._selected = None
        self._text = None

    def pack(self, **options):
        super().pack(options)
        self._calgrid.pack()
        
    def create_grid_year(self, year):
        # clear canvas
        self._calgrid.delete("all")
        for month in CalendarGrid.MONTH_RANGE:
            dates_and_tiles = self._create_grid_tiles(year, month)
            self._create_grid_separ(year, month)
            self._bind_tile_and_date(dates_and_tiles)
            
    def bind_tiles_callback(self, callback=None, event_trigger='<Button-1>'):
        def _callback(event):
            canvas = event.widget
            current_item = canvas.find_withtag("current")
            tile_id = current_item[0]
            if callback:
                callback(self._tile_date[tile_id], tile_id)
        self._calgrid.tag_bind("tile", event_trigger, _callback)

    def tile(self, date):
        return self._date_tile[date]

    def date(self, tile):
        return self._tile_date[tile]

    def set_tile_color_rgb(self, date, color_hex: tuple):
        t = self.tile(date)
        self._calgrid.itemconfig(t, fill=color_hex)

    def selected(self, date):
        if self._selected:
            self._calgrid.delete(self._selected)
            self._selected = None
        tile_id = self._date_tile.get(date, None)
        if tile_id:
            coords = self._calgrid.coords(tile_id)
            # create rectangle around tile from lines
            self._selected = self._calgrid.create_line(
                coords[0], coords[1],
                coords[2], coords[1],
                coords[2], coords[3],
                coords[0], coords[3],
                coords[0], coords[1],
                fill="green", width=2)

    def set_text_to_tile(self, tile_id, text, offset_x=10, offset_y=8):
        tile_coords = self._calgrid.coords(tile_id)
        if self._text is None:
            pos = tile_coords[0] + offset_x, tile_coords[1] + offset_y
            # disable state required to disable catching events
            self._text = self._calgrid.create_text(pos, text=text, state='disabled')
        else:
            self._calgrid.coords(self._text, (tile_coords[0], tile_coords[1]))

    def remove_text(self):
        if self._text:
            self._calgrid.delete(self._text)
            self._text = None

    # private
    def _weeknr_weekday_date(self, year, month):
        c = calendar.Calendar()
        return [(d.isocalendar()[1], d.weekday(), d)
                for d in c.itermonthdates(year, month)]

    def _pos_tile_date(self, year, month):
        """
        calculates widget grid positions by returning (row,col,date)
        triple for given month, one week per column
        """
        for (week_nr, week_day, date) in self._weeknr_weekday_date(year, month):
            if (month == date.month):
                if (month == 1 and (week_nr == 52 or week_nr == 53)):
                    yield (0, week_day, date)
                elif (month == 12 and week_nr == 1):
                    yield (53, week_day, date)
                else:
                    yield (week_nr, week_day, date)

    def _pos_separ(self, year, month):
        last_day = calendar.monthrange(year, month)[1]
        first_date = datetime(year=year, month=month, day=1)
        last_date = datetime(year=year, month=month, day=last_day)
        first_weekday, last_weekday = first_date.weekday(), last_date.weekday()
        fnr = first_date.isocalendar()[1]
        lnr = last_date.isocalendar()[1]
        first_weeknr = 0 if (fnr == 52 or fnr == 53) else fnr
        last_weeknr = 53 if lnr == 1 else lnr
        points = []
        if first_weekday == 0:
            first_pos = (first_weeknr, 0)
            points.extend(first_pos)
        else:
            first_pos = (first_weeknr + 1, 0)
            points.extend(first_pos)
            points.extend((first_weeknr + 1, first_weekday))
            points.extend((first_weeknr, first_weekday))
        points.extend((first_weeknr, 7))
        if last_weekday == 6:
            points.extend((last_weeknr + 1, 7))
        else:
            points.extend((last_weeknr, 7))
            points.extend((last_weeknr, last_weekday + 1))
            points.extend((last_weeknr + 1, last_weekday + 1))
        points.extend((last_weeknr + 1, 0))
        points.extend(first_pos)
        return points
            
    def _create_tile(self, x0, y0, x1, y1):
        tile_id = self._calgrid.create_rectangle(x0, y0, x1, y1, outline=self._toutline,
                                                 tags=("tile",), activeoutline='green',
                                                 fill=self._tbg)
        # each tile has a tag with its id
        self._calgrid.addtag_withtag(str(tile_id), tile_id)
        return tile_id

    def _create_grid_tiles(self, year, month):
        dates_and_tiles = []
        for col, row, date in self._pos_tile_date(year, month):
            tile = self._create_tile(CalendarGrid.POS_0 + self._tsize * col,
                                     CalendarGrid.POS_0 + self._tsize * row,
                                     CalendarGrid.POS_0 + self._tsize * (col + 1),
                                     CalendarGrid.POS_0 + self._tsize * (row + 1))
            dates_and_tiles.append((date, tile))
        return dates_and_tiles

    def _create_grid_separ(self, year, month):
        coords = [CalendarGrid.POS_0 + self._tsize * p
                  for p in self._pos_separ(year, month)]
        return self._calgrid.create_line(coords, tags=("separ",))

    def _bind_tile_and_date(self, dates_and_tiles):
        for date, tile in dates_and_tiles:
            self._date_tile[date] = tile
            self._tile_date[tile] = date
