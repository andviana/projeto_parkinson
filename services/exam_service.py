from models import exam_repo

def cadastrar_exames(paciente_id, form_data):
    exam_keys = ['gds', 'moca', 'spdds', 'updrs_i', 'updrs_ii', 'updrs_iii', 'updrs_iv', 'hoehn_yahr', 'beck']
    saved_exams = []
    
    for exam_key in exam_keys:
        date_val = form_data.get(f'{exam_key}_date')
        score_val = form_data.get(f'{exam_key}_score')
        
        if date_val and score_val:
            exam_repo.insert_exam(exam_key, paciente_id, date_val, float(score_val))
            
            display_name = exam_key.upper().replace('_', ' ')
            if display_name == 'HOEHN YAHR':
                display_name = 'Hoehn & Yahr'
            saved_exams.append(display_name)
            
    return saved_exams
