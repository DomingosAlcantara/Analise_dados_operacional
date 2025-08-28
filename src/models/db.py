import dataset


class Database:
    def __init__(self, db_path="sqlite:///home/domingos/Documentos/Projetos Python/Monitoramento_Máquinas_Mensagens/data/monitoramento.db"):
        self.db = dataset.connect(db_path)

    def get_table(self, table_name):
        return self.db[table_name]

    def insert_record(self, table_name, record):
        table = self.get_table(table_name)
        table.insert(record)

    def query(self, query_string):
        return self.db.query(query_string)
