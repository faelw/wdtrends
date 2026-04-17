import google.generativeai as genai
import json
import os
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURAÇÃO DA API
# Dica de Segurança: Nunca suba a chave real no GitHub!
# Use variáveis de ambiente. No terminal: export GEMINI_API_KEY="sua_chave"
# ---------------------------------------------------------
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Chave da API do Gemini não encontrada. Configure a variável de ambiente GEMINI_API_KEY.")

genai.configure(api_key=api_key)

# Usando o modelo Pro que é ideal para raciocínio complexo e formatação JSON rigorosa
model = genai.GenerativeModel('gemini-1.5-pro')
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# ---------------------------------------------------------
# DICIONÁRIO DE IDIOMAS E REGIÕES
# ---------------------------------------------------------
languages = {
    "pt": {"region": "BR", "lang_name": "Português Brasileiro"},
    "en": {"region": "US", "lang_name": "Inglês Americano"},
    "es": {"region": "LATAM", "lang_name": "Espanhol Latino-americano"}
}

# ---------------------------------------------------------
# MÓDULO DE COLETA (Scraper Simulado)
# No futuro, aqui você fará requests para o RapidAPI, X, YouTube, etc.
# ---------------------------------------------------------
def get_raw_data(region):
    # Simulando dados brutos colhidos da internet
    global_news = """
    1. Lançamento revolucionário de IA de vídeo gera debate sobre deepfakes e o fim de Hollywood.
    2. Criptomoeda cai 20% após nova regulamentação mundial surpresa.
    """
    
    local_news = {
        "BR": "1. Treta entre influenciadores gigantes no TikTok. 2. Nova lei de taxação de compras online aprovada.",
        "US": "1. Eleições presidenciais: candidato comete gafe em debate. 2. Super Bowl anuncia atração polêmica.",
        "LATAM": "1. Final da Copa Libertadores gera memes épicos. 2. Crise diplomática entre países vizinhos."
    }
    
    return global_news, local_news.get(region, "Sem dados locais")

# ---------------------------------------------------------
# O CÉREBRO: CHAMADA AO GEMINI
# ---------------------------------------------------------
def generate_creator_insights(lang_code, lang_info, global_data, local_data):
    prompt = f"""
    Atue como um estrategista de conteúdo viral para YouTube, TikTok e Canais Dark no mercado {lang_info['lang_name']} (Foco na região: {lang_info['region']}).
    
    FONTES GLOBAIS (O que o mundo fala): {global_data}
    FONTES LOCAIS (O que a região {lang_info['region']} fala): {local_data}

    Sua missão é mastigar essas informações brutas e entregar ideias de ouro prontas para criadores de conteúdo gravarem.
    Gere exatamente 2 tópicos globais e 2 tópicos locais (para este teste. No futuro serão 10 de cada).
    
    Para cada tópico, gere 10 'micro_insights' usando ESTRITAMENTE estes 'types':
    - 'title_idea': Ideia de título magnético/clickbait.
    - 'thumbnail_idea': Ideia visual para a capa.
    - 'hook': O texto para os primeiros 3 segundos de vídeo (o gancho).
    - 'angle_news': Como abordar se for canal de Notícias.
    - 'angle_dark': Como abordar se for Canal Dark (mistério, curiosidade, bizarro).
    - 'tags': 5 palavras-chave.
    - 'audience_feeling': A emoção alvo (ex: revolta, choque, curiosidade).
    - 'monetization': Ideia de venda/afiliado para o vídeo.
    - 'controversy': O ponto polêmico para gerar comentários no vídeo.
    - 'call_to_action': Como pedir inscrição/like.

    A resposta deve ser ESTRITAMENTE o JSON abaixo, no idioma {lang_info['lang_name']}:
    {{
      "region": "{lang_info['region']}",
      "language": "{lang_code}",
      "update_time": "{current_time}",
      "global_trends": [
         {{ "id": "g_01", "title": "Título do Assunto", "micro_insights": [ {{"type": "tipo_aqui", "text": "texto do insight..."}} ] }}
      ],
      "local_trends": [
         {{ "id": "l_01", "title": "Título do Assunto", "micro_insights": [ {{"type": "tipo_aqui", "text": "texto do insight..."}} ] }}
      ]
    }}
    """

    print(f"Processando tendências em {lang_info['lang_name']}...")
    
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    return response.text

# ---------------------------------------------------------
# LOOP PRINCIPAL
# ---------------------------------------------------------
def main():
    print("Iniciando Macro Ultra - Varredura e Análise...")
    
    for lang_code, lang_info in languages.items():
        try:
            # 1. Coleta os dados brutos da região
            global_raw, local_raw = get_raw_data(lang_info['region'])
            
            # 2. Envia para a IA analisar e estruturar
            json_output = generate_creator_insights(lang_code, lang_info, global_raw, local_raw)
            
            # 3. Valida se a IA realmente retornou um JSON válido
            parsed_json = json.loads(json_output)
            
            # 4. Salva no disco
            file_name = f"trends_{lang_code}.json"
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(parsed_json, f, ensure_ascii=False, indent=2)
                
            print(f"✅ Sucesso: {file_name} gerado e estruturado.")
            
        except json.JSONDecodeError:
            print(f"❌ Erro de JSON: A IA não retornou um formato válido para {lang_code}.")
        except Exception as e:
            print(f"❌ Erro ao processar {lang_code}: {e}")

    print("\nVarredura concluída. Verifique os arquivos JSON na pasta do projeto.")

if __name__ == "__main__":
    main()
