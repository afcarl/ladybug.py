ladybug.py
==========

Handle CSV files using table models and queries.

## Table models
ladybug.py handles CSV files through table models. You need to define a table model for your files by subclassing `Table`.

An example
```python
class ExampleTable(Table):
    name = Field()
    salary = Field(format=int)
    department = Field()
```
    
## Table managers
Table managers are objects that contain actual tables, built from a table model. There are two ways to create a table manager:
```python
# Open a .csv file
ExampleTable.open("example.csv")

# Create an empty manager
ExampleTable.create()
```

### Working with table managers
#### .filter
Returns a subset that matches a given query
```python
table.filter(department="Management")
```

#### .column
Returns a column of a table
```python
print table.column("name")
print sum(table.column("salary"))
```
Result:
```python
['Bob', 'Rob', 'Joe', 'Maria', 'Carlos']
16900
```

#### .order_by & .reverse
`.order_by` and `.reverse` are used for changing the order of rows in a table.
```python
table.order_by("salary")
table.order_by("salary").reverse
```

#### .insert
Inserts a row into a table manager
```python
table.insert(name="Carlos", salary=6000, department="Management")
```

#### .group_by
Returns a dictionary of grouped elements.

```python
table.group_by("department", key="name")
```
Result:
```python
{'Management': ['Carlos'], 'IT': ['Bob', 'Joe'], 'Sales': ['Rob', 'Maria']}
```

It's also possible to pass the rows to a given function:
```python
table.group_by("department", key="name", function=tuple)
table.group_by("department", function=sum, key="salary")
```
Result:
```python
{'IT': ('Bob', 'Joe'), 'Sales': ('Rob', 'Maria')}
{'IT': 3500, 'Sales': 5500}
```

#### .update
Updates existing rows in a (filtered) manager. This is an in-place mutation.
```python
# Set salary for entire office
table.update(salary=2000)

# Set salary for whole IT department
table.filter(department="IT").update(salary=3000)

# Set salary for Joe alone
table.filter(department="IT", name="Joe").update(salary=2700)
```

#### .save
Save manager into a .csv file.
```python
table.save("example_output.csv")
```

#### .copy
Using `.copy` it is possible to have a copy of a (filtered) managers. This means
that you can change rows in the copy while the original remains intact.

##### Updating a copy
```python
cc_table = table.copy
print list(table.filter(name="Maria").rows)
print list(cc_table.filter(name="Maria").rows)
cc_table.filter(name="Maria").update(department="IT")
print list(table.filter(name="Maria").rows)
print list(cc_table.filter(name="Maria").rows)
```
Output:
```python
[{'salary': 2500, 'department': 'Sales', 'name': 'Maria'}]
[{'salary': 2500, 'department': 'Sales', 'name': 'Maria'}]
[{'salary': 2500, 'department': 'Sales', 'name': 'Maria'}]  # Intact
[{'salary': 2500, 'department': 'IT', 'name': 'Maria'}]  # Updated
```

## Supported dialects
ladybug.py uses `DictReader` and `DictWriter`. It's possible to use keyword arguments of those, so all dialects accepted by `DictReader` and `DictWriter` can be handled.

The following example shows how to convert a CSV file to another dialect using ladybug.py
```python
ExampleTable.open("example.csv", delimiter=",").save("example_output.csv", delimiter=";")
```