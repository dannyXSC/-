import abc


class Reader(metaclass=abc.ABCMeta):
    def __init__(self, file_name):
        pass

    @abc.abstractmethod
    def get_titles(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def get_row_number(self):
        pass

    @abc.abstractmethod
    def travel_row(self, with_title=False):
        pass
