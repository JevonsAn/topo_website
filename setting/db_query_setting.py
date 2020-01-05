# -*- coding: utf-8 -*-

action_union = {"ipv4", "ipv6", "router", "pop", "gateway", "cable" , "links"}
type_union = {"node", "edge", "router_edge", "mpls_edge", "mrinfo_edge", "pchar_edge", "neighbor", "ipv4_link","ipv6_link","mpls_link","mrinfo_link","pchar_link","parsedConf_link","iffinder_link"}

action_type_to_tablename = {
    "ipv4": {
        "node": "edges.node_table",
        "edge": "edges.edge_table",
    },
    "ipv6": {
        "node": "edges._ipv6_total_node_table",
        "edge": "edges._ipv6_total_edge_table",
    },
    "router": {
        "edge": "edges.router_edge_table",
        "node": "edges.router_node_table",
        "router_edge": "edges.router_edge_table",
        "mpls_edge": "edges.router_edge_table",
        "mrinfo_edge": "edges.router_edge_table",
        "pchar_edge": "edges.router_edge_table",
    },
    "pop": {
        "edge": "edges.pop_edge_table",
        "node": "edges.pop_node_table",
    },
    "gateway": {
        "node": "edges.gateway_node_table",
        "edge": "edges.gateway_edge_table"
    },
    "cable": {
        "node": "statistics.cable_info",
        "edge": "statistics.cable_link"
    }
}

action_type_expire = {
    "router": {
        "router_edge": {
            "field": "type",
            "value": "(1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31)",
            "joiner": "in"
        },
        "mpls_edge": {
            "field": "type",
            "value": "(2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31)",
            "joiner": "in"
        },
        "mrinfo_edge": {
            "field": "type",
            "value": "(8, 9, 10, 11, 12, 13, 14, 15, 24, 25, 26, 27, 28, 29, 30, 31)",
            "joiner": "in"
        },
        "pchar_edge": {
            "field": "type",
            "value": "(4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31)",
            "joiner": "in"
        },
    },
}

arg_transform = {
    "router_type": {
        "field": "type",
        "value": {
            "1": "(1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31)"
        },
        "joiner": "in"
    }
}

tablename_to_fields = {
    "odinary_task_table": {
        "fields": {
            "in_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "out_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "is_dest": {
                "type": "char",
                "joiner": "="
            },
            "star": {
                "type": "int",
                "joiner": "="
            },
            "latency": {
                "type": "float",
                "joiner": "="
            },
            "freq": {
                "type": "int",
                "joiner": "="
            },
            "ttl": {
                "type": "varchar",
                "joiner": "="
            },
            "monitor": {
                "type": "varchar",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "in_asn": {
                "type": "int",
                "joiner": "="
            },
            "in_country": {
                "type": "varchar",
                "joiner": "="
            },
            "in_region": {
                "type": "varchar",
                "joiner": "="
            },
            "in_city": {
                "type": "varchar",
                "joiner": "="
            },
            "in_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "in_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "out_asn": {
                "type": "int",
                "joiner": "="
            },
            "out_country": {
                "type": "varchar",
                "joiner": "="
            },
            "out_region": {
                "type": "varchar",
                "joiner": "="
            },
            "out_city": {
                "type": "varchar",
                "joiner": "="
            },
            "out_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "out_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "bandwidth": {
                "type": "varchar",
                "joiner": "="
            },
            "type": {
                "type": "int",
                "joiner": "="
            },
            "misc": {
                "type": "longtext",
                "joiner": "="
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "="
            }
        }
    },
    "statistics.cable_info": {
        "fields": {
            "id": {
                "type": "varchar",
                "joiner": "="
            },
            "cable_id": {
                "type": "int",
                "joiner": "="
            },
            "name": {
                "type": "varchar",
                "joiner": "="
            },
            "length": {
                "type": "varchar",
                "joiner": "="
            },
            "rfs": {
                "type": "varchar",
                "joiner": "="
            },
            "landing_points": {
                "type": "longtext",
                "joiner": "="
            },
            "owners": {
                "type": "varchar",
                "joiner": "="
            },
            "notes": {
                "type": "varchar",
                "joiner": "="
            },
            "url": {
                "type": "varchar",
                "joiner": "="
            }
        }
    },
    "edges._ipv6_total_edge_table": {
        "fields": {
            "in_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "out_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "is_dest": {
                "type": "char",
                "joiner": "="
            },
            "star": {
                "type": "int",
                "joiner": "="
            },
            "latency": {
                "type": "float",
                "joiner": "="
            },
            "freq": {
                "type": "int",
                "joiner": "="
            },
            "ttl": {
                "type": "varchar",
                "joiner": "="
            },
            "monitor": {
                "type": "varchar",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "in_asn": {
                "type": "int",
                "joiner": "="
            },
            "in_country": {
                "type": "varchar",
                "joiner": "="
            },
            "in_region": {
                "type": "varchar",
                "joiner": "="
            },
            "in_city": {
                "type": "varchar",
                "joiner": "="
            },
            "in_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "in_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "out_asn": {
                "type": "int",
                "joiner": "="
            },
            "out_country": {
                "type": "varchar",
                "joiner": "="
            },
            "out_region": {
                "type": "varchar",
                "joiner": "="
            },
            "out_city": {
                "type": "varchar",
                "joiner": "="
            },
            "out_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "out_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "bandwidth": {
                "type": "varchar",
                "joiner": "="
            },
            "type": {
                "type": "int",
                "joiner": "="
            },
            "misc": {
                "type": "longtext",
                "joiner": "="
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "="
            }
        }
    },
    "edges.edge_table": {
        "fields": {
            "in_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "out_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "is_dest": {
                "type": "char",
                "joiner": "="
            },
            "star": {
                "type": "int",
                "joiner": "="
            },
            "latency": {
                "type": "float",
                "joiner": "="
            },
            "freq": {
                "type": "int",
                "joiner": "="
            },
            "ttl": {
                "type": "varchar",
                "joiner": "="
            },
            "monitor": {
                "type": "varchar",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "in_asn": {
                "type": "int",
                "joiner": "="
            },
            "in_country": {
                "type": "varchar",
                "joiner": "="
            },
            "in_region": {
                "type": "varchar",
                "joiner": "="
            },
            "in_city": {
                "type": "varchar",
                "joiner": "="
            },
            "in_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "in_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "out_asn": {
                "type": "int",
                "joiner": "="
            },
            "out_country": {
                "type": "varchar",
                "joiner": "="
            },
            "out_region": {
                "type": "varchar",
                "joiner": "="
            },
            "out_city": {
                "type": "varchar",
                "joiner": "="
            },
            "out_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "out_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "bandwidth": {
                "type": "varchar",
                "joiner": "="
            },
            "type": {
                "type": "int",
                "joiner": "="
            },
            "misc": {
                "type": "longtext",
                "joiner": "="
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "="
            }
        }
    },
    "edges.node_table": {
        "fields": {
            "ip": {
                "type": "varchar",
                "joiner": "="
            },
            "ip_int": {
                "type": "decimal",
                "joiner": "="
            },
            "is_host": {
                "type": "char",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "="
            },
            "asn": {
                "type": "int",
                "joiner": "="
            },
            "country": {
                "type": "varchar",
                "joiner": "="
            },
            "region": {
                "type": "varchar",
                "joiner": "="
            },
            "city": {
                "type": "varchar",
                "joiner": "="
            },
            "latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "whois": {
                "type": "varchar",
                "joiner": "="
            },
            "domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "device_info": {
                "type": "longtext",
                "joiner": "="
            },
            "degree": {
                "type": "int",
                "joiner": "="
            },
            "k_core": {
                "type": "int",
                "joiner": "="
            },
            "rtr_id": {
                "type": "varchar",
                "joiner": "="
            },
            "pop_id": {
                "type": "varchar",
                "joiner": "="
            }
        }
    },
    "edges.gateway_edge_table": {
        "fields": {
            "in_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "out_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "is_dest": {
                "type": "char",
                "joiner": "="
            },
            "star": {
                "type": "int",
                "joiner": "="
            },
            "latency": {
                "type": "float",
                "joiner": "="
            },
            "freq": {
                "type": "int",
                "joiner": "="
            },
            "ttl": {
                "type": "varchar",
                "joiner": "="
            },
            "monitor": {
                "type": "varchar",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "in_asn": {
                "type": "int",
                "joiner": "="
            },
            "in_country": {
                "type": "varchar",
                "joiner": "="
            },
            "in_region": {
                "type": "varchar",
                "joiner": "="
            },
            "in_city": {
                "type": "varchar",
                "joiner": "="
            },
            "in_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "in_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "out_asn": {
                "type": "int",
                "joiner": "="
            },
            "out_country": {
                "type": "varchar",
                "joiner": "="
            },
            "out_region": {
                "type": "varchar",
                "joiner": "="
            },
            "out_city": {
                "type": "varchar",
                "joiner": "="
            },
            "out_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "out_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "bandwidth": {
                "type": "varchar",
                "joiner": "="
            },
            "type": {
                "type": "int",
                "joiner": "="
            },
            "misc": {
                "type": "longtext",
                "joiner": "="
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "="
            }
        }
    },
    "edges.pop_edge_table": {
        "fields": {
            "in_pop_id": {
                "type": "varchar",
                "joiner": "="
            },
            "out_pop_id": {
                "type": "varchar",
                "joiner": "="
            },
            "num": {
                "type": "int",
                "joiner": "="
            }
        }
    },
    "edges.pop_node_table": {
        "fields": {
            "pop_id": {
                "type": "varchar",
                "joiner": "="
            },
            "geo": {
                "type": "varchar",
                "joiner": "="
            },
            "num": {
                "type": "int",
                "joiner": "="
            }
        }
    },
    "edges._ipv6_total_node_table": {
        "fields": {
            "ip": {
                "type": "varchar",
                "joiner": "="
            },
            "ip_int": {
                "type": "decimal",
                "joiner": "="
            },
            "is_host": {
                "type": "char",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "="
            },
            "asn": {
                "type": "int",
                "joiner": "="
            },
            "country": {
                "type": "varchar",
                "joiner": "="
            },
            "region": {
                "type": "varchar",
                "joiner": "="
            },
            "city": {
                "type": "varchar",
                "joiner": "="
            },
            "longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "whois": {
                "type": "varchar",
                "joiner": "="
            },
            "domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "device_info": {
                "type": "longtext",
                "joiner": "="
            },
            "degree": {
                "type": "int",
                "joiner": "="
            },
            "k_core": {
                "type": "int",
                "joiner": "="
            },
            "rtr_id": {
                "type": "int",
                "joiner": "="
            },
            "pop_id": {
                "type": "varchar",
                "joiner": "="
            }
        }
    },
    "statistics.cable_link": {
        "fields": {
            "landing_point_in": {
                "type": "varchar",
                "joiner": "="
            },
            "landing_point_out": {
                "type": "varchar",
                "joiner": "="
            },
            "cable": {
                "type": "varchar",
                "joiner": "="
            },
            "in_country": {
                "type": "varchar",
                "joiner": "="
            },
            "out_country": {
                "type": "varchar",
                "joiner": "="
            },
            "in_latlng": {
                "type": "varchar",
                "joiner": "="
            },
            "out_latlng": {
                "type": "varchar",
                "joiner": "="
            },
            "cable_rfs": {
                "type": "varchar",
                "joiner": "="
            },
            "cable_len": {
                "type": "varchar",
                "joiner": "="
            },
            "cable_url": {
                "type": "varchar",
                "joiner": "="
            },
            "update_time": {
                "type": "date",
                "joiner": "="
            },
            "medium": {
                "type": "char",
                "joiner": "="
            }
        }
    },
    "edges.router_edge_table": {
        "fields": {
            "in_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "out_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "star": {
                "type": "int",
                "joiner": "="
            },
            "count": {
                "type": "int",
                "joiner": "="
            },
            "monitor": {
                "type": "varchar",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "in_asn": {
                "type": "int",
                "joiner": "="
            },
            "in_country": {
                "type": "varchar",
                "joiner": "="
            },
            "in_region": {
                "type": "varchar",
                "joiner": "="
            },
            "in_city": {
                "type": "varchar",
                "joiner": "="
            },
            "in_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "in_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "in_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "out_asn": {
                "type": "int",
                "joiner": "="
            },
            "out_country": {
                "type": "varchar",
                "joiner": "="
            },
            "out_region": {
                "type": "varchar",
                "joiner": "="
            },
            "out_city": {
                "type": "varchar",
                "joiner": "="
            },
            "out_latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "out_whois": {
                "type": "varchar",
                "joiner": "="
            },
            "out_domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "bandwidth": {
                "type": "varchar",
                "joiner": "="
            },
            "type": {
                "type": "int",
                "joiner": "="
            },
            "history_seen": {
                "type": "longtext",
                "joiner": "="
            },
            "misc": {
                "type": "varchar",
                "joiner": "="
            }
        }
    },
    "edges.router_node_table": {
        "fields": {
            "ip": {
                "type": "varchar",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "="
            },
            "asn": {
                "type": "int",
                "joiner": "="
            },
            "country": {
                "type": "varchar",
                "joiner": "="
            },
            "region": {
                "type": "varchar",
                "joiner": "="
            },
            "city": {
                "type": "varchar",
                "joiner": "="
            },
            "latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "whois": {
                "type": "varchar",
                "joiner": "="
            },
            "domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "device_info": {
                "type": "longtext",
                "joiner": "="
            },
            "degree": {
                "type": "int",
                "joiner": "="
            }
        }
    },
    "edges.gateway_node_table": {
        "fields": {
            "ip": {
                "type": "varchar",
                "joiner": "="
            },
            "ip_int": {
                "type": "decimal",
                "joiner": "="
            },
            "is_host": {
                "type": "char",
                "joiner": "="
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "="
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "="
            },
            "asn": {
                "type": "int",
                "joiner": "="
            },
            "country": {
                "type": "varchar",
                "joiner": "="
            },
            "region": {
                "type": "varchar",
                "joiner": "="
            },
            "city": {
                "type": "varchar",
                "joiner": "="
            },
            "latitude": {
                "type": "varchar",
                "joiner": "="
            },
            "longitude": {
                "type": "varchar",
                "joiner": "="
            },
            "whois": {
                "type": "varchar",
                "joiner": "="
            },
            "domain": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            },
            "device_info": {
                "type": "longtext",
                "joiner": "="
            },
            "degree": {
                "type": "int",
                "joiner": "="
            },
            "k_core": {
                "type": "int",
                "joiner": "="
            },
            "rtr_id": {
                "type": "varchar",
                "joiner": "="
            },
            "pop_id": {
                "type": "varchar",
                "joiner": "="
            }
        }
    }
}

if __name__ == "__main__":
    from connection.mysql_conn import Mysql

    conn = Mysql()
    tables = set()
    new_tablename_to_fields = {}
    for action, typE in action_type_to_tablename.items():
        tables.update({typE["node"], typE["edge"]})
    for table in tables:
        conn.exe("desc %s" % table)
        r = conn.fetchall()
        new_tablename_to_fields[table] = {
            "fields": {
                d['Field']:
                    {"type": d['Type'], "joiner": '='}
                    if d['Type'].find('(') == -1
                    else {"type": d['Type'][:d['Type'].find('(')], "joiner": '='}
                for d in r
            }
        }
    conn.close()
    import json

    print("tablename_to_fields = ")
    print(json.dumps(new_tablename_to_fields, indent=4))
