import google.generativeai as genai
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 1. CARREGAR CHAVE DE SEGURANÇA
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chave não encontrada! Verifique se o arquivo .env existe e está correto.")

genai.configure(api_key=api_key)

# Usando o modelo Pro (ideal para textos longos e JSON complexo)
model = genai.GenerativeModel('gemini-1.5-pro')
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# 2. CONFIGURAÇÃO DE MERCADOS
languages = {
    "pt": {"region": "BR", "lang_name": "Português Brasileiro"},
    "en": {"region": "US", "lang_name": "Inglês Americano"},
    "es": {"region": "LATAM", "lang_name": "Espanhol Latino-americano"}
}

# 3. MÓDULO DE COLETA (Scraper Bruto)
def get_raw_data(region):
    # No ambiente de produção, conecte APIs do X, TikTok, Google Trends aqui.
    # Esta é a base de dados simulada para a IA ler e expandir.
    global_news = """
    - Lançamento revolucionário de IA de vídeo gera debate sobre deepfakes.
    - Criptomoeda cai 20% após nova regulamentação mundial surpresa.
    - Nova missão espacial anunciada com datas para colonização.
    - CEO de big tech faz declaração polêmica sobre o futuro do trabalho.
    - Vazamento massivo de dados afeta milhões de usuários globalmente.
    """
    
    local_news = {
        "BR": "- Treta gigante entre influenciadores no TikTok BR.\n- Nova lei de taxação aprovada no congresso.\n- Meme do momento dominando as redes.\n- Final de reality show quebra recorde de votos.",
        "US": "- Eleições: candidato comete gafe ao vivo.\n- Super Bowl anuncia atração principal.\n- Empresa americana demite 10 mil funcionários.\n- Nova trend de dança domina as escolas.",
        "LATAM": "- Crise diplomática entre países vizinhos.\n- Final da Copa Libertadores gera confusão.\n- Artista latino bate recorde no Spotify.\n- Protestos em massa por conta da economia."
    }
    
    return global_news, local_news.get(region, "Sem dados locais detalhados no momento.")

# 4. O MOTOR DA IA (Gerador de Insights)
def generate_creator_insights(lang_code, lang_info, global_data, local_data):
    prompt = f"""
    Atue como um estrategista de conteúdo viral para YouTube, TikTok e Canais Dark no mercado {lang_info['lang_name']} (Foco na região: {lang_info['region']}).
    
    FONTES GLOBAIS: {global_data}
    FONTES LOCAIS: {local_data}

    Sua missão é criar um JSON contendo 30 tendências no total, divididas em duas categorias:
    - 15 tópicos em 'global_trends'
    - 15 tópicos em 'local_trends'
    
    Para CADA UM dos 30 tópicos, gere ESTRITAMENTE 10 'micro_insights' práticos usando estas chaves 'type':
    1. 'title_idea': Ideia de título magnético/clickbait.
    2. 'thumbnail_idea': Ideia visual para a capa do vídeo.
    3. 'hook': Roteiro dos primeiros 3 segundos de vídeo (o gancho).
    4. 'angle_news': Abordagem para canal de Notícias.
    5. 'angle_dark': Abordagem para Canal Dark (mistério, bizarro).
    6. 'tags': 5 palavras-chave separadas por vírgula.
    7. 'audience_feeling': A emoção alvo que o vídeo deve causar.
    8. 'monetization': Ideia de produto/afiliado para vender no vídeo.
    9. 'controversy': O ponto polêmico para gerar debate nos comentários.
    10. 'call_to_action': Como pedir inscrição ou like de forma orgânica.

    O retorno DEVE ser APENAS o JSON válido abaixo, no idioma {lang_info['lang_name']}:
    {{
      "region": "{lang_info['region']}",
      "language": "{lang_code}",
      "update_time": "{current_time}",
      "global_trends": [
         {{ "id": "g_01", "title": "Título", "micro_insights": [ {{"type": "tipo", "text": "texto do insight"}} ] }}
         // ... continue até g_15
      ],
      "local_trends": [
         {{ "id": "l_01", "title": "Título", "micro_insights": [ {{"type": "tipo", "text": "texto do insight"}} ] }}
         // ... continue até l_15
      ]
    }}
    """

    print(f"[{lang_code.upper()}] Solicitando 30 Trends e 300 Insights para o Gemini. Aguarde...")
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    return response.text

# 5. LOOP DE EXECUÇÃO
def main():
    print("Iniciando Macro Ultra - Varredura Massiva...")
    
    for lang_code, lang_info in languages.items():
        try:
            # Pega os dados simulados
            global_raw, local_raw = get_raw_data(lang_info['region'])
            
            # Gera os dados com a IA
            json_output = generate_creator_insights(lang_code, lang_info, global_raw, local_raw)
            
            # Valida e converte para dicionário Python
            parsed_json = json.loads(json_output)
            
            # Salva no disco formatado
            file_name = f"trends_{lang_code}.json"
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(parsed_json, f, ensure_ascii=False, indent=2)
                
            print(f"✅ Sucesso: {file_name} gerado (30 trends processadas).")
            
        except json.JSONDecodeError:
            print(f"❌ Erro de JSON: O Gemini cortou a resposta no meio para {lang_code} (provável limite de tokens).")
        except Exception as e:
            print(f"❌ Erro crítico ao processar {lang_code}: {e}")

    print("\nProcesso concluído. Arquivos salvos na pasta raiz.")

if __name__ == "__main__":
    main()
