from tortoise.backends.mysql import MySQLClient

from unfazed_prometheus import agent


class PrometheusMySQLClient(MySQLClient):
    @agent.monitor_database
    async def execute_insert(self, query: str, values: list) -> int:
        return await super().execute_insert(query, values)

    @agent.monitor_database
    async def execute_query(self, query: str, values: list) -> int:
        return await super().execute_query(query, values)

    @agent.monitor_database
    async def execute_query_dict(self, query: str, values: list) -> int:
        return await super().execute_query_dict(query, values)

