from tornado.netutil import is_valid_ip
from setting.const_variables import country_union
from setting.db_query_setting import action_union, type_union


def validate_args(args, required_args, request_args):
    flag = True
    msg = ""
    # 验证必需参数是否存在
    for arg in required_args:
        if arg not in args:
            return False, "必需参数 %s 不存在" % arg
    # 验证每个参数是否合法
    for arg in args:
        if arg not in request_args:
            return False, "参数 %s 不是合法参数" % arg
        validate_func = type_validate_functions[request_args[arg]["validate"]["type"]]
        value = args[arg]
        extra_args = request_args[arg]["validate"].get("args", {})
        result = False
        if extra_args:
            result = validate_func(value, extra_args)
        else:
            result = validate_func(value)
        if not result:
            return False, "参数 %s 的值不合法" % arg
    return flag, msg


boolean_union = {"Y", "N"}

db_required_args = {
    "action", "type"
}

graph_required_args = {
    "action"
}

type_validate_functions = {
    "union": lambda s, union: True if s in union else False,
    "int": lambda s: True if s.isdigit() else False,
    "ip": is_valid_ip,
    "string": lambda s: True,
    "": lambda s: True,
}

db_request_args = {
    "action": {
        "validate": {
            "type": "union",
            "args": action_union,
        },
        "key_type": "",
        "joiner": "="
    },
    "type": {
        "validate": {
            "type": "union",
            "args": type_union,
        },
        "key_type": "",
        "joiner": "="
    },
    "ip": {
        "validate": {
            "type": "ip",
        },
        "key_type": "where",
        "joiner": "="
    },
    "asn": {
        "validate": {
            "type": "int"
        },
        "key_type": "where",
        "joiner": "="
    },
    "country": {
        "validate": {
            "type": "union",
            "args": country_union,
        },
        "key_type": "where",
        "joiner": "="
    },
    "city": {
        "validate": {
            "type": "string",
        },
        "key_type": "where",
        "joiner": "="
    },
    "is_as_boundary": {
        "validate": {
            "type": "union",
            "args": boolean_union,
        },
        "key_type": "where",
        "joiner": "="
    },
    "is_country_boundary": {
        "validate": {
            "type": "union",
            "args": boolean_union,
        },
        "key_type": "where",
        "joiner": "="
    },
    "pageIndex": {
        "validate": {
            "type": "int",
        },
        "key_type": "page",
        "joiner": "="
    },
    "pageSize": {
        "validate": {
            "type": "int",
        },
        "key_type": "page",
        "joiner": "="
    },
    "sortOrder": {
        "validate": {
            "type": "union",
            "args": {"ascending", "descending"}
        },
        "key_type": "sort",
        "joiner": "="
    },
    "sortField": {
        "validate": {
            "type": "",
        },
        "key_type": "sort",
        "joiner": "="
    },
    "export_type": {
        "validate": {
            "type": "union",
            "args": {"json", "csv", "xml"}
        },
        "key_type": "export",
        "joiner": "="
    },
    "export": {
        "validate": {
            "type": "",
        },
        "key_type": "export",
        "joiner": "="
    },
    "export_limit": {
        "validate": {
            "type": "int",
        },
        "key_type": "export",
        "joiner": "="
    },
    "router_type": {
        "validate": {
            "type": "int",
        },
        "key_type": "where",
        "joiner": "="
    },
    "in_out_ip": {
        "validate": {
            "type": "ip",
        },
        "key_type": "where",
        "joiner": "="
    },
    "in_out_asn": {
        "validate": {
            "type": "int"
        },
        "key_type": "where",
        "joiner": "="
    },
    "in_out_country": {
        "validate": {
            "type": "union",
            "args": country_union,
        },
        "key_type": "where",
        "joiner": "="
    },
    "in_out_city": {
        "validate": {
            "type": "string",
        },
        "key_type": "where",
        "joiner": "="
    },
    "in_pop_id": {
        "validate": {
            "type": "string",
        },
        "key_type": "where",
        "joiner": "="
    },
    "out_pop_id": {
        "validate": {
            "type": "string",
        },
        "key_type": "where",
        "joiner": "="
    },
    "pop_id": {
        "validate": {
            "type": "string",
        },
        "key_type": "where",
        "joiner": "="
    },
    "geo": {
        "validate": {
            "type": "string",
        },
        "key_type": "where",
        "joiner": "="
    },
    "in_out_pop_id": {
        "validate": {
            "type": "string",
        },
        "key_type": "where",
        "joiner": "="
    },
}

graph_request_args = {
    "action": {
        "validate": {
            "type": "union",
            "args": {"3hops"},
        },
        "key_type": "",
        "joiner": "="
    },
    "type": {
        "validate": {
            "type": "union",
            "args": {"ipv4", "ipv6"},
        },
        "key_type": "",
        "joiner": "="
    },
    "ip": {
        "validate": {
            "type": "ip",
        },
        "key_type": "where",
        "joiner": "="
    },
    "pageIndex": {
        "validate": {
            "type": "int",
        },
        "key_type": "page",
        "joiner": "="
    },
    "pageSize": {
        "validate": {
            "type": "int",
        },
        "key_type": "page",
        "joiner": "="
    },
    "sortOrder": {
        "validate": {
            "type": "",
        },
        "key_type": "sort",
        "joiner": "="
    },
    "sortField": {
        "validate": {
            "type": "",
        },
        "key_type": "sort",
        "joiner": "="
    },
    "export_type": {
        "validate": {
            "type": "",
        },
        "key_type": "export",
        "joiner": "="
    },
    "export": {
        "validate": {
            "type": "",
        },
        "key_type": "export",
        "joiner": "="
    },
    "export_limit": {
        "validate": {
            "type": "int",
        },
        "key_type": "export",
        "joiner": "="
    },
}
