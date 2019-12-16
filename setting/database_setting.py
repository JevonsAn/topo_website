NEO4J_URI = "bolt://10.10.11.150:7687"
NEO4J_USER = "neo4j"
NEO4J_PWD = "root"

databases = {
    "edges": {
        "host": "10.10.11.150",
        "user": "root",
        "passwd": "1q2w3e4r",
        "db": "edges",
        "port": 3306
    },
    "api": {
        "host": "10.10.11.150",
        "user": "root",
        "passwd": "1q2w3e4r",
        "db": "api",
        "port": 3306
    },
    "bgp": {
        "host": "10.10.11.151",
        "user": "root",
        "passwd": "1q2w3e4r",
        "db": "tp_bgp_data",
        "port": 3306
    },
    "tasks": {
        "host": "10.10.11.150",
        "user": "root",
        "passwd": "1q2w3e4r",
        "db": "statistics",
        "port": 3306
    },
    "statistics": {
        "host": "10.10.11.150",
        "user": "root",
        "passwd": "1q2w3e4r",
        "db": "statistics",
        "port": 3306
    }
}

REDIS_HOST = "10.10.11.150"
REDIS_PORT = 6379
