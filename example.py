from ladybug.model import Table, Field


class ExampleTable(Table):
    columns = ("name", "salary", "department")

    name = Field()
    salary = Field(format=int)
    department = Field()

table = ExampleTable.open("example.csv")
print table.group_by("department")
print table.group_by("department", function=sum, key="salary")
