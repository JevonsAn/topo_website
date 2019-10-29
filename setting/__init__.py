from setting.arg_setting import request_args, type_validate_functions
from setting.query_setting import action_type_to_tablename, tablename_to_fields

# 验证 request_args 是否合法
for k, v in request_args.items():
    # 判断类型是否合法
    if not isinstance(v, dict):
        raise TypeError("setting.arg_setting 中 request_args 每个参数都应该是 dict 类型")

    # 验证字段是否完整
    if "validate" not in v:
        raise ValueError("setting.arg_setting 中 request_args 每个参数必须含有 validate 字段")
    if "key_type" not in v:
        raise ValueError("setting.arg_setting 中 request_args 每个参数必须含有 key_type 字段")

    # 验证 validate 是否合法
    valid = v["validate"]
    if "type" not in valid:
        raise ValueError("setting.arg_setting 中 request_args 每个参数的 validate 字段必须含有 type 字段")
    if valid["type"] not in type_validate_functions:
        raise ValueError("%s字段的 validate 字段的 type 字段不在 type_validate_functions 中" % k)

func_type = type(lambda s: True)
# 验证 type_validate_functions 是否合法
for v in type_validate_functions.values():
    if isinstance(v, func_type):
        raise TypeError("setting.arg_setting 中 type_validate_functions 每个value都应该是函数")

# 验证 action_type_to_tablename 中的表是否和 tablename_to_fields 对应
used_tablename_union = [vv in tablename_to_fields for v in action_type_to_tablename.values() for vv in v.values()]
from functools import reduce

if not reduce(lambda x, y: x and y, used_tablename_union):
    raise ValueError("setting.query_setting 中 action_type_to_tablename 中的每个表都应在 tablename_to_fields 中出现")
