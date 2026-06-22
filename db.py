import os
import logging
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Verifica se chaves reais válidas estão configuradas no ambiente
if (SUPABASE_URL and SUPABASE_KEY and 
    SUPABASE_URL != "sua-supabase-url-aqui" and 
    SUPABASE_KEY != "sua-supabase-anon-key-aqui"):
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        logger.warning(f"Erro ao instanciar o cliente Supabase real: {e}. Usando Mock local.")
        from supabase_mock import SupabaseMockClient
        supabase = SupabaseMockClient()
else:
    # Fallback para execução local e offline em testes
    from supabase_mock import SupabaseMockClient
    supabase = SupabaseMockClient()

