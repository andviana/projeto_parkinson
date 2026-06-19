import sqlite3
import uuid
import datetime

class SupabaseMockClient:
    def __init__(self, db_path='parkinson_local.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela grupos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grupos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Tabela pacientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id TEXT PRIMARY KEY,
                nome_completo TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                sexo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela vinculos_grupo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vinculos_grupo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente TEXT NOT NULL,
                id_grupo INTEGER NOT NULL,
                data_inicio TEXT NOT NULL,
                data_fim TEXT,
                FOREIGN KEY (id_paciente) REFERENCES pacientes (id),
                FOREIGN KEY (id_grupo) REFERENCES grupos (id)
            )
        ''')
        
        # Tabelas de exames clínicos
        for exam in ['gds', 'moca', 'spdds', 'updrs_i', 'updrs_ii', 'updrs_iii', 'updrs_iv', 'hoehn_yahr', 'beck']:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {exam} (
                    id_exame TEXT PRIMARY KEY,
                    id_paciente TEXT NOT NULL,
                    data_exame TEXT NOT NULL,
                    nota_final REAL NOT NULL,
                    FOREIGN KEY (id_paciente) REFERENCES pacientes (id)
                )
            ''')

        # Novas tabelas de Ficha de Dados Clínicos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sintomas_dominio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS localizacoes_dominio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sigla TEXT UNIQUE NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados_clinicos (
                id_paciente TEXT PRIMARY KEY,
                tempo_inicio_sintomas_anos INTEGER,
                resposta_motora TEXT CHECK (resposta_motora IN ('nenhuma melhora', 'pouca melhora', 'melhora parcial', 'melhora total')),
                tolerancia_levodopa TEXT CHECK (tolerancia_levodopa IN ('sem problemas', 'teve dificuldade', 'intolerancia')),
                uso_regular_cafe INTEGER DEFAULT 0,
                frequencia_por_dia INTEGER DEFAULT 0,
                cirurgia_dp INTEGER DEFAULT 0,
                abuso_substancia INTEGER DEFAULT 0,
                qual_substancia TEXT,
                ancestrais TEXT,
                familiar_com_dp TEXT CHECK (familiar_com_dp IN ('sim', 'não', 'não sabe')) DEFAULT 'não',
                qual_familiar_dp TEXT,
                familiar_com_tremor TEXT CHECK (familiar_com_tremor IN ('sim', 'não', 'não sabe')) DEFAULT 'não',
                qual_familiar_tremor TEXT,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_paciente) REFERENCES pacientes (id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados_clinicos_sintomas (
                id_paciente TEXT,
                id_sintoma INTEGER,
                PRIMARY KEY (id_paciente, id_sintoma),
                FOREIGN KEY (id_paciente) REFERENCES dados_clinicos (id_paciente) ON DELETE CASCADE,
                FOREIGN KEY (id_sintoma) REFERENCES sintomas_dominio (id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados_clinicos_localizacoes (
                id_paciente TEXT,
                id_localizacao INTEGER,
                PRIMARY KEY (id_paciente, id_localizacao),
                FOREIGN KEY (id_paciente) REFERENCES dados_clinicos (id_paciente) ON DELETE CASCADE,
                FOREIGN KEY (id_localizacao) REFERENCES localizacoes_dominio (id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados_complementares (
                id_paciente TEXT PRIMARY KEY,
                telefone TEXT NOT NULL,
                dominio_manual TEXT CHECK (dominio_manual IN ('destro(a)', 'sinistro(a)')) NOT NULL,
                cor TEXT CHECK (cor IN ('pardo(a)', 'branco(a)', 'negro(a)', 'amarelo(a)')) NOT NULL,
                estado_civil TEXT CHECK (estado_civil IN ('solteiro(a)', 'casado(a)', 'separado(a)', 'viuvo(a)', 'divorciado(a)')) NOT NULL,
                escolaridade TEXT CHECK (escolaridade IN ('fundamental incompleto', 'fundamental completo', 'medio incompleto', 'medio completo', 'superior incompleto', 'superior completo', 'pós graduação')) NOT NULL,
                atividade_profissional TEXT CHECK (atividade_profissional IN ('aposentado(a)', 'desempregado(a)', 'trabalhador(a) ativo(a)', 'auxilio doença', 'beneficiario(a)', 'amparo social')) NOT NULL,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_paciente) REFERENCES pacientes (id) ON DELETE CASCADE
            )
        ''')

        # Seed sintomas de domínio se vazio
        cursor.execute("SELECT COUNT(*) FROM sintomas_dominio")
        if cursor.fetchone()[0] == 0:
            for s in ['bradicinesia', 'rigidez', 'tremor', 'instabilidade postural', 'fraqueza muscular', 'formigamento', 'outros']:
                cursor.execute("INSERT INTO sintomas_dominio (nome) VALUES (?)", (s,))

        # Seed localizacoes de domínio se vazio
        cursor.execute("SELECT COUNT(*) FROM localizacoes_dominio")
        if cursor.fetchone()[0] == 0:
            for loc in ['MSD', 'MIE', 'MSE', 'MS', 'MI', 'MID', 'QUEIXO', 'CABEÇA', 'OUTRO']:
                cursor.execute("INSERT INTO localizacoes_dominio (sigla) VALUES (?)", (loc,))
            
        # Seed usuários se vazio
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            from werkzeug.security import generate_password_hash
            cursor.execute("INSERT INTO usuarios (username, password_hash, role) VALUES (?, ?, ?)",
                           ('admin', generate_password_hash('Institutoviv@'), 'admin'))
            cursor.execute("INSERT INTO usuarios (username, password_hash, role) VALUES (?, ?, ?)",
                           ('clinico', generate_password_hash('clinico'), 'usuario'))
            
        # Seed grupos se vazio
        cursor.execute("SELECT COUNT(*) FROM grupos")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO grupos (nome) VALUES (?)", ('Grupo de Fisioterapia Viva',))
            cursor.execute("INSERT INTO grupos (nome) VALUES (?)", ('Acompanhamento Fonoaudiológico',))
            cursor.execute("INSERT INTO grupos (nome) VALUES (?)", ('Terapia Ocupacional Cognitiva',))
            
            # Seed pacientes de exemplo
            p1_id = str(uuid.uuid4())
            p2_id = str(uuid.uuid4())
            p3_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO pacientes (id, nome_completo, data_nascimento, sexo, tipo) VALUES (?, ?, ?, ?, ?)",
                           (p1_id, 'Carlos Alberto de Souza', '1958-05-12', 'M', 'PD'))
            cursor.execute("INSERT INTO pacientes (id, nome_completo, data_nascimento, sexo, tipo) VALUES (?, ?, ?, ?, ?)",
                           (p2_id, 'Maria Eduarda Santos', '1962-11-24', 'F', 'HC'))
            cursor.execute("INSERT INTO pacientes (id, nome_completo, data_nascimento, sexo, tipo) VALUES (?, ?, ?, ?, ?)",
                           (p3_id, 'Roberto Linhares da Silva', '1970-08-03', 'M', 'PR'))
            
            # Seed vínculos de grupo
            cursor.execute("INSERT INTO vinculos_grupo (id_paciente, id_grupo, data_inicio) VALUES (?, 1, '2026-01-15')", (p1_id,))
            cursor.execute("INSERT INTO vinculos_grupo (id_paciente, id_grupo, data_inicio) VALUES (?, 1, '2026-02-20')", (p2_id,))
            cursor.execute("INSERT INTO vinculos_grupo (id_paciente, id_grupo, data_inicio) VALUES (?, 2, '2026-03-01')", (p3_id,))
            
        conn.commit()
        conn.close()

    def table(self, name):
        return QueryBuilder(self.db_path, name)


class QueryBuilder:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.select_fields = '*'
        self.filters = []
        self.order_by_col = None
        self.order_by_desc = False
        self.limit_val = None

    def select(self, fields='*'):
        self.select_fields = fields
        return self

    def eq(self, field, value):
        self.filters.append((field, '=', value))
        return self

    def neq(self, field, value):
        self.filters.append((field, '!=', value))
        return self

    def order(self, column, desc=False):
        self.order_by_col = column
        self.order_by_desc = desc
        return self

    def limit(self, value):
        self.limit_val = value
        return self

    def insert(self, data):
        self.insert_data = data
        return self

    def update(self, data):
        self.update_data = data
        return self

    def delete(self):
        self.delete_op = True
        return self

    def execute(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Operação de Insert
        if hasattr(self, 'insert_data'):
            records = self.insert_data if isinstance(self.insert_data, list) else [self.insert_data]
            inserted_rows = []
            
            for record in records:
                # Garante UUID se não fornecido
                if 'id' not in record and self.table_name == 'pacientes':
                    record['id'] = str(uuid.uuid4())
                if 'id_exame' not in record and self.table_name in ['gds', 'moca', 'spdds', 'updrs_i', 'updrs_ii', 'updrs_iii', 'updrs_iv', 'hoehn_yahr', 'beck']:
                    record['id_exame'] = str(uuid.uuid4())

                columns = list(record.keys())
                placeholders = ', '.join(['?'] * len(columns))
                sql = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                cursor.execute(sql, list(record.values()))
                
                primary_key = 'id' if 'id' in record else ('id_exame' if 'id_exame' in record else columns[0])
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE {primary_key} = ?", (record[primary_key],))
                    
                desc_info = cursor.description
                row = cursor.fetchone()
                row_dict = dict(zip([col[0] for col in desc_info], row))
                inserted_rows.append(row_dict)
                
            conn.commit()
            conn.close()
            
            class Response:
                def __init__(self, data):
                    self.data = data
            return Response(inserted_rows)

        # Operação de Update
        if hasattr(self, 'update_data'):
            set_clause = ', '.join([f"{k} = ?" for k in self.update_data.keys()])
            params = list(self.update_data.values())
            
            where_clause = ""
            if self.filters:
                where_clause = " WHERE " + " AND ".join([f"{f[0]} {f[1]} ?" for f in self.filters])
                params.extend([f[2] for f in self.filters])
                
            sql = f"UPDATE {self.table_name} SET {set_clause}{where_clause}"
            cursor.execute(sql, params)
            conn.commit()
            
            select_sql = f"SELECT * FROM {self.table_name}{where_clause}"
            cursor.execute(select_sql, [f[2] for f in self.filters])
            desc_info = cursor.description
            rows = cursor.fetchall()
            updated_rows = [dict(zip([col[0] for col in desc_info], r)) for r in rows]
            conn.close()
            
            class Response:
                def __init__(self, data):
                    self.data = data
            return Response(updated_rows)

        # Operação de Delete
        if hasattr(self, 'delete_op'):
            where_clause = ""
            params = []
            if self.filters:
                where_clause = " WHERE " + " AND ".join([f"{f[0]} {f[1]} ?" for f in self.filters])
                params.extend([f[2] for f in self.filters])
                
            select_sql = f"SELECT * FROM {self.table_name}{where_clause}"
            cursor.execute(select_sql, params)
            desc_info = cursor.description
            rows = cursor.fetchall()
            deleted_rows = [dict(zip([col[0] for col in desc_info], r)) for r in rows]
            
            sql = f"DELETE FROM {self.table_name}{where_clause}"
            cursor.execute(sql, params)
            conn.commit()
            conn.close()
            
            class Response:
                def __init__(self, data):
                    self.data = data
            return Response(deleted_rows)

        # Operação de Select
        params = []
        where_clause = ""
        if self.filters:
            where_clause_parts = []
            for f in self.filters:
                where_clause_parts.append(f"{f[0]} {f[1]} ?")
                params.append(f[2])
            where_clause = " WHERE " + " AND ".join(where_clause_parts)
            
        sql = f"SELECT {self.select_fields} FROM {self.table_name}{where_clause}"
        
        if self.order_by_col:
            sql += f" ORDER BY {self.order_by_col}"
            if self.order_by_desc:
                sql += " DESC"
                
        if self.limit_val:
            sql += f" LIMIT {self.limit_val}"
            
        cursor.execute(sql, params)
        desc_info = cursor.description
        rows = cursor.fetchall()
        data = [dict(zip([col[0] for col in desc_info], r)) for r in rows]
        conn.close()
        
        class Response:
            def __init__(self, data):
                self.data = data
        return Response(data)
