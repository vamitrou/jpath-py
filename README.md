# jpath-py
XPath-like querying for JSON. Written in python


Example: 

```python
d={
    "students": [
        {
            "name": "bob",
            "projects": [
                {
                    "name": "banana"
                },
                {
                    "name": "apple"
                }
            ]
        },
        {
            "name": "alice",
            "projects": [
                {
                    "name": "orange"
                }
            ]
        }
    ]
}

from jpathpy import jpath

# get me the second project's name of the first student
print jpath.get_dict_value(d, "students[0]/projects[1]/name")
>> apple

# get me all the project objects of the first student
print jpath.get_dict_valut(d, "students[0]/projects/*")
>> [{'name': 'banana'}, {'name': 'apple'}]

# get me all the project names of all the students
print jpath.get_dict_value(d, "students/*/projects/*/name")
>> [['banana', 'apple'], ['orange']]
```
