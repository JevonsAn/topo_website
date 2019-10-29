from neo4j import GraphDatabase
from setting.database_setting import NEO4J_PWD, NEO4J_URI, NEO4J_USER


class Neo4jDriver(object):

    def __init__(self):
        self._driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PWD))

    def close(self):
        self._driver.close()

    def execute_and_get_one(self, cql):
        with self._driver.session() as session:
            return session.read_transaction(self._get_one_by_cql, cql)

    @staticmethod
    def _get_one_by_cql(tx, cql):
        result = tx.run(cql)
        return result.single()[0]

    def execute_and_get_all(self, cql):
        with self._driver.session() as session:
            return session.read_transaction(self._get_all_by_cql, cql)

    @staticmethod
    def _get_all_by_cql(tx, cql):
        result = tx.run(cql)
        return result.data()

    def get_node_count(self):
        with self._driver.session() as session:
            return session.read_transaction(self._select_count_of_nodes)

    @staticmethod
    def _select_count_of_nodes(tx):
        result = tx.run("MATCH (n:node) RETURN count(n) LIMIT 1")
        return result.value()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


if __name__ == '__main__':
    neo4j_conn = Neo4jDriver()
    result = neo4j_conn.execute_and_get_all("MATCH (n:node) RETURN count(n) LIMIT 1")
    print(result)
    # for r in result:
    #     print(r.graph)
    neo4j_conn.close()
