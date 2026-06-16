from db import supabase

def get_exams_by_patient_and_table(table_name, paciente_id):
    res = supabase.table(table_name).select('*').eq('id_paciente', paciente_id).execute()
    return res.data


def insert_exam(table_name, paciente_id, data_exame, nota_final):
    data = {
        'id_paciente': paciente_id,
        'data_exame': data_exame,
        'nota_final': nota_final
    }
    res = supabase.table(table_name).insert(data).execute()
    return res.data[0] if res.data else None
