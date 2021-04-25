import random
import image_data_loader


class CellAssigner:
    def __init__(self, cells):
        assert type(list()) == type(cells)
        self.cells = cells

    def __sub__(self, other):
        cells = self.cells.copy()
        for cell in other.cells:
            if cell in self.cells:
                cells.remove(cell)
        return CellAssigner(cells)

    def select_half_of_cells_randomly(self):
        for _ in range(len(self.cells) // 2):
            self.cells.remove(random.choice(self.cells))

    def __str__(self):
        return str(self.cells)

    def get_list_of_cells(self):
        return str(self.cells.split())


if __name__ == "__main__":
    ca = CellAssigner(image_data_loader.get_image_paths())
    print(ca)
    ca.select_half_of_cells_randomly()
    print(ca)
    ca2 = CellAssigner(image_data_loader.get_image_paths())
    print(ca-ca2)
