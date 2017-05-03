# jpath-py
XPath-like querying for JSON. Written in python


Example: 

```
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
        }
    ]
}

from jpathpy import jpath

print jpath.get_dict_value(d, "students[0]/projects[1]/name")
>> apple
```
