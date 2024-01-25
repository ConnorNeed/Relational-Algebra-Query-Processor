import copy
tableid = 1000
class Table:
    def __init__(self, rows, columns, column_names, table_name):
        self.rows = rows
        self.columns = columns
        self.data = [["N/A"] * columns for _ in range(rows)]
        self.table_name = str(table_name)
        self.column_names = column_names
        global tableid
        if(table_name == tableid):
            tableid += 1

    def set_value(self, row, column, value):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.data[row][column] = value
        else:
            raise Exception("Invalid row or column index")

    def get_value(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.data[row][column]
        else:
            raise Exception("Invalid row or column index")

    def display(self):
        header = f"Table: {self.table_name}\n" + "|".join(f"{col:15}" for col in self.column_names)
        print(header)
        for row in self.data:
            row_str = "|".join(f"{value:15}" for value in row)
            print(row_str)
        print()

    def add_row(self, values):
        if len(values) != self.columns:
            raise Exception(f"Invalid number of values for the row ({values})")
        self.data.append(values)
        self.rows += 1

    def get_rows(self, orgValues, evalStatement):
        filtered_data = []
        for i in range(len(self.data)):
            values = copy.deepcopy(orgValues)
            for j in range(len(values)):
                if values[j] in self.column_names:
                    values[j] = self.data[i][self.column_names.index(values[j])]
            if(eval(evalStatement)):
                filtered_data.append(self.data[i])
        return copy.deepcopy(self._create_table_with_data(filtered_data,self.column_names))

    def get_columns(self, column_names):
        if not set(column_names).issubset(self.column_names):
            raise Exception("Invalid column names")
        indices = [self.column_names.index(col) for col in column_names]
        selected_data = [[row[i] for i in indices] for row in self.data]
        return copy.deepcopy(self._create_table_with_data(selected_data, column_names))

    def join(self, other_table):
        joined_data = [row1 + row2 for row1, row2 in zip(self.data, other_table.data)]
        joined_column_names = self.column_names + [(f"{other_table.table_name}.{col}" if col in self.column_names else f"{col}") for col in other_table.column_names]
        newTable = self._create_table_with_data(joined_data, column_names=joined_column_names)
        newTable.table_name = self.table_name + " x " + other_table.table_name
        return copy.deepcopy(newTable)

    def dup1(self, times):
        duplicated_data = [row for row in self.data for _ in range(times)]
        return copy.deepcopy(self._create_table_with_data(duplicated_data, self.column_names))

    def dup2(self, times):
        duplicated_data = self.data * times
        return copy.deepcopy(self._create_table_with_data(duplicated_data, self.column_names))

    def _create_table_with_data(self, data, column_names):
        new_table = Table(rows=len(data), columns=len(column_names), column_names=column_names, table_name=self.table_name)
        new_table.data = data
        return new_table
    def len(self):
        return self.rows
    def union(self, other_table):
        if len(self.column_names) != len(other_table.column_names):
            raise Exception("Tables have different column names. Unable to perform union.")

        union_data = self.data + [row for row in other_table.data if row not in self.data]
        newTable = self._create_table_with_data(union_data, self.column_names)
        newTable.table_name = self.table_name + " U " + other_table.table_name
        return copy.deepcopy(newTable)

    def intersect(self, other_table):
        if len(self.column_names) != len(other_table.column_names):
            raise Exception("Tables have different column names. Unable to perform intersection.")

        intersect_data = [row for row in self.data if row in other_table.data]
        newTable = self._create_table_with_data(intersect_data, self.column_names)
        newTable.table_name = self.table_name + " intersect " + other_table.table_name
        return copy.deepcopy(newTable)

    def setMinus(self, other_table):
        if len(self.column_names) != len(other_table.column_names):
            raise Exception("Tables have different column names. Unable to perform set difference.")

        set_minus_data = [row for row in self.data if row not in other_table.data]
        newTable = self._create_table_with_data(set_minus_data, self.column_names)
        newTable.table_name = self.table_name + " - " + other_table.table_name
        return copy.deepcopy(newTable)