from .model import Model

DATABASE_FILE = "../database/database.db"


class Ervaringsdeskundige(Model):
    def load_queries(self, path):
        queries = {}
        query_name = None
        parameters = []

        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                # print(f"Processing line: {line}")
                if line.startswith('-- [') and line.endswith(']'):
                    if query_name and parameters:
                        queries[query_name] = ' '.join(parameters).rstrip(';')
                    query_name = line[4:-1]
                    parameters = []
                elif query_name:
                    if line:
                        parameters.append(line)

            if query_name and parameters:
                queries[query_name] = ' '.join(parameters).rstrip(';')

        return queries
