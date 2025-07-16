import pandas as pd
import os
from downloadE2.download import download_data
from openpyxl import load_workbook
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Side, Border


def main():
    download_data()


if __name__ == "__main__":
    main()
