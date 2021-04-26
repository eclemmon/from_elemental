"""
Section Manager Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"

class SectionManager:
    def __init__(self, sections):
        self.sections = dict(zip(range(1, len(sections)+1), sections))
        self.current_section = 1

    def next(self):
        self.current_section += 1

    def get_current_section_name(self):
        return self.sections[self.current_section][0]

    def get_current_section_timing(self):
        return self.sections[self.current_section][1]

    def set_current_section(self, key):
        if key < len(self.sections):
            self.current_section = key
        else:
            print("key must be less than {}, and an integer".format(len(self.sections)))

    def get_total_timing(self):
        total_seconds = 0
        for val in self.sections.values():
            total_seconds += val[1]
        return total_seconds

    def start_from_section(self, section_value):
        timing = 0
        for i in range(1, section_value):

            timing += self.sections[i][1]
        self.current_section = section_value
        return timing


if __name__ == "__main__":
    sections = [("Cosmic", 40),
                ("Element Introduction", 90),
                ("Life Forms", 90),
                ("Emergence of Individuals", 40),
                ("Emergence of collective", 40),
                ("Conflict between collective and individual", 50),
                ("INCISION", 10),
                ("Trancendence: COSMIC RE-FRAMED", 60)]
    sm = SectionManager(sections)
    print(sm.get_total_timing())
    print(sm.sections)
    print(sm.get_current_section_name())
    sm.next()
    print(sm.get_current_section_name())
    sm.set_current_section(4)
    print(sm.get_current_section_name())
    print(sm.get_current_section_timing())
    print(sm.start_from_section(5))
    print(sm.get_current_section_name())
    sm.set_current_section(20)
