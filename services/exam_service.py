from models import exam_repo
from services.exceptions import ValidationError
from services.utils import parse_date

def cadastrar_exames(paciente_id, form_data):
    exam_keys = ['gds', 'moca', 'spdds', 'updrs_i', 'updrs_ii', 'updrs_iii', 'updrs_iv', 'hoehn_yahr', 'beck']
    saved_exams = []
    
    for exam_key in exam_keys:
        date_val = form_data.get(f'{exam_key}_date')
        score_val = form_data.get(f'{exam_key}_score')
        
        if date_val and score_val:
            try:
                parse_date(date_val)
            except ValueError as e:
                raise ValidationError(f"Data inválida para o exame {exam_key.upper()}: {str(e)}")
                
            try:
                score_float = float(score_val)
                if score_float < 0:
                    raise ValidationError(f"A nota do exame {exam_key.upper()} não pode ser negativa.")
            except ValueError as e:
                raise ValidationError(f"A nota do exame {exam_key.upper()} deve ser um número válido.") from e
                
            exam_repo.insert_exam(exam_key, paciente_id, date_val, score_float)
            
            display_name = exam_key.upper().replace('_', ' ')
            if display_name == 'HOEHN YAHR':
                display_name = 'Hoehn & Yahr'
            saved_exams.append(display_name)
            
    return saved_exams
