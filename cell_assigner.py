"""
Cell Assigner Module
"""

__author__ = "Eric Lemmon"
__copyright__ = "Copyright 2021, Eric Lemmon"
__credits = ["Eric Lemmon, Anne Sophie Andersen"]
__version__ = "0.9"
__maintainer__ = "Eric Lemmon"
__email__ = "ec.lemmon@gmail.com"
__status__ = "Testing"


import random
import image_data_loader


class CellAssigner:
    """
    A class that manages score cell assignments.
    """
    def __init__(self, cells):
        """
        Initializes the CellAssigner
        :param cells: List of cell paths.
        """
        assert type(list()) == type(cells)
        self.cells = cells

    def __sub__(self, other):
        """
        Removes 'other' cell paths from self's cell paths, and returns a new CellAssigner object.
        :param other: Other CellAssigner object.
        :return: CellAssigner
        """
        cells = self.cells.copy()
        for cell in other.cells:
            if cell in self.cells:
                cells.remove(cell)
        return CellAssigner(cells)

    def __add__(self, other):
        """
        Adds 'other cell paths to self's cell paths and returns a new CellAssigner object.
        :param other: Other CellAssigner object
        :return: CellAssigner
        """
        cells = self.cells.copy()
        for cell in other.cells:
            if cell not in self.cells:
                cells.append(cell)
        return CellAssigner(cells)

    def select_half_of_cells_randomly(self):
        """
        Randomly removes half the cell paths from self.cells.
        :return: None
        """
        for _ in range(len(self.cells) // 2):
            self.cells.remove(random.choice(self.cells))

    def __str__(self):
        """
        Returns the list of cells as a printable string.
        :return: String
        """
        return str(self.cells)


if __name__ == "__main__":
    ca = CellAssigner(image_data_loader.get_image_paths())
    print(ca)
    ca.select_half_of_cells_randomly()
    print(ca)
    ca2 = CellAssigner(image_data_loader.get_image_paths())
    print(ca-ca2)
    ca2.select_half_of_cells_randomly()
    print(ca+ca2)
