from Reader.Reader import Reader
import xlrd


class XLS_Reader(Reader):

    def __init__(self, file_name):
        super().__init__(file_name)
        self.wb = xlrd.open_workbook(file_name)
        self.sht = self.wb.sheet_by_index(0)
        self.rows = self.sht.nrows
        self.cols = self.sht.ncols

    def get_titles(self):
        return self.sht.row_values(0)

    def close(self):
        self.wb.release_resources()

    def get_row_number(self):
        return self.rows

    def travel_row(self, with_title=False):
        num_rows = self.rows
        begin_row = 0 if with_title else 1
        for cur_row in range(begin_row, num_rows):
            row_data = self.sht.row_slice(cur_row)
            result = []
            for col in range(self.cols):
                ctype = row_data[col].ctype
                cell = row_data[col].value
                if ctype == 2 and cell % 1 == 0:  # 如果是整形
                    result.append(int(cell))
                elif ctype == 3:
                    # 转成datetime对象
                    datatime_result = xlrd.xldate_as_datetime(cell, self.wb.datemode)
                    str_result = datatime_result.strftime('%Y-%d-%m %H:%M:%S')
                    result.append(str_result)
                else:
                    result.append(cell)
            yield result
