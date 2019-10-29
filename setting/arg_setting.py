from tornado.netutil import is_valid_ip
from setting.const_variables import country_union
from setting.query_setting import action_union, type_union

boolean_union = {"Y", "N"}

required_args = {
    "action", "type"
}

# request_key_type = {
#     "page": ["pageIndex", "pageSize"],
#     "sort": ["sortOrder", "sortField"],
#     # "action": ["action"],
#     "export": ["export_type", "export", "export_limit"],
#     "where": []
# }

type_validate_functions = {
    "union": lambda s, union: True if s in union else False,
    "int": lambda s: True if s.isdigit() else False,
    "ip": is_valid_ip,
    "string": lambda s: True,
    "": lambda s: True,
}

request_args = {
    "action": {
        "validate": {
            "type": "union",
            "args": action_union,
        },
        "key_type": ""
    },
    "type": {
        "validate": {
            "type": "union",
            "args": type_union,
        },
        "key_type": ""
    },
    "ip": {
        "validate": {
            "type": "ip",
        },
        "key_type": "where"
    },
    "asn": {
        "validate": {
            "type": "int"
        },
        "key_type": "where"
    },
    "country": {
        "validate": {
            "type": "union",
            "args": country_union,
        },
        "key_type": "where"
    },
    "city": {
        "validate": {
            "type": "string",
        },
        "key_type": "where"
    },
    "is_as_boundary": {
        "validate": {
            "type": "union",
            "args": boolean_union,
        },
        "key_type": "where"
    },
    "is_country_boundary": {
        "validate": {
            "type": "union",
            "args": boolean_union,
        },
        "key_type": "where"
    },
    "pageIndex": {
        "validate": {
            "type": "int",
        },
        "key_type": "page"
    },
    "pageSize": {
        "validate": {
            "type": "int",
        },
        "key_type": "page"
    },
    "sortOrder": {
        "validate": {
            "type": "",
        },
        "key_type": "sort"
    },
    "sortField": {
        "validate": {
            "type": "",
        },
        "key_type": "sort"
    },
    "export_type": {
        "validate": {
            "type": "",
        },
        "key_type": "export"
    },
    "export": {
        "validate": {
            "type": "",
        },
        "key_type": "export"
    },
    "export_limit": {
        "validate": {
            "type": "int",
        },
        "key_type": "export"
    }
}
