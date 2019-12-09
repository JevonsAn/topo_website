from connection.neo4j_conn import Neo4jDriver
from model.usual_query import Query
import time


class GraphQuery(object):
    """
        此模块功能：
        1.拼接cql语句
        2.管理neo4j连接，后续可做连接池
    """

    def __init__(self):
        self.conn = Neo4jDriver()

    async def search3hops(self, ip):
        cql = 'MATCH (cs:node {ip:"%s"}) CALL apoc.path.expandConfig(cs,{relationshipFilter:"edge",maxLevel:3,' \
              'bfs:true}) YIELD path WITH RELATIONSHIPS(path) as el unwind el as e RETURN startNode(e).ip as i, ' \
              'endNode(e).ip as o, properties(e) as e limit 100' % ip
        links = self.conn.execute_and_get_all(cql)
        ip_link_set = []
        for r in links:
            in_ip = r['i']
            out_ip = r['o']
            ip_link_set.append("(\"%s\", \"%s\")" % (in_ip, out_ip))
        query = Query("edge_table", [("(in_ip, out_ip)", "(%s)" % ", ".join(ip_link_set), "in")])
        query_result = await query.search()
        query_result = {(d["in_ip"], d["out_ip"]): d for d in query_result["data"]}
        result = []
        for r in links:
            in_ip = r['i']
            out_ip = r['o']
            result.append(query_result[(in_ip, out_ip)])
        return result

    async def search(self, action, args):
        start_time = time.clock()
        result = []
        if action == "3hops":
            ip = args["ip"]
            result = await self.search3hops(ip)

        return {
            "data": list(result),
            "itemsCount": len(result),  # count_result[0]["count(*)"],
            "time": round(time.clock() - start_time)
        }

    def __del__(self):
        if self.conn:
            self.conn.close()
