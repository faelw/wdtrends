import json
import os
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. CARREGAR CHAVE DE SEGURANÇA
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chave não encontrada! Verifique os Secrets do GitHub.")

# Inicializa o cliente na NOVA biblioteca do Google
client = genai.Client(api_key=api_key)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# 2. CONFIGURAÇÃO DE MERCADOS
languages = {
    "pt": {"region": "BR", "lang_name": "Português Brasileiro"},
    "en": {"region": "US", "lang_name": "Inglês Americano"},
    "es": {"region": "LATAM", "lang_name": "Espanhol Latino-americano"}
}

# 3. MÓDULO DE COLETA (Scraper Bruto)
def get_raw_data(region):
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
      ],
      "local_trends": [
         {{ "id": "l_01", "title": "Título", "micro_insights": [ {{"type": "tipo", "text": "texto do insight"}} ] }}
      ]
    }}
    """

    print(f"[{lang_code.upper()}] Solicitando Insights para a IA...")
    
    # Nova sintaxe de chamada com a biblioteca atualizada
    response = client.models.generate_content(
        model='gemini-1.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7,
        )
    )
    
    return response.text

# 5. LOOP DE EXECUÇÃO
def main():
    print("Iniciando Macro Ultra com SDK Atualizado...")
    
    for lang_code, lang_info in languages.items():
        try:
            global_raw, local_raw = get_raw_data(lang_info['region'])
            
            json_output = generate_creator_insights(lang_code, lang_info, global_raw, local_raw)
            parsed_json = json.loads(json_output)
            
            file_name = f"trends_{lang_code}.json"
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(parsed_json, f, ensure_ascii=False, indent=2)
                
            print(f"✅ Sucesso: {file_name} gerado.")
            
        except json.JSONDecodeError:
            print(f"❌ Erro de JSON em {lang_code}.")
        except Exception as e:
            print(f"❌ Erro crítico ao processar {lang_code}: {e}")

    print("\nProcesso concluído.")

if __name__ == "__main__":
    main()
