import praw
import os
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()

# Configurar credenciais
reddit = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),
                     client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
                     user_agent="meu_bot")

# Buscar posts do subreddit "vini jr"
search_term = "Flamengo"
result_limit = 15

print(f"\n--- Buscando os {result_limit} posts mais recentes sobre '{search_term}' em r/all ---")

posts_encontrados = 0
try:
    # Busca em r/all pelos posts mais recentes
    for post in reddit.subreddit("all").search(search_term, limit=result_limit, sort="new"):
        posts_encontrados += 1

        # 1. Obter nome do autor de forma segura
        author_name = "[deletado]" # Valor padrão se o autor não existir
        if post.author:
            author_name = post.author.name # Pega o nome de usuário

        # 2. Converter timestamp UTC para datetime e formatar
        #    Use datetime.fromtimestamp() para converter o float UTC
        created_dt = datetime.fromtimestamp(post.created_utc)
        formatted_time = created_dt.strftime('%H:%M:%S %Y-%m-%d UTC') # Adicionei UTC para clareza

        # Imprimir informações de forma mais organizada
        print("-" * 30) # Separador
        print(f"Subreddit: r/{post.subreddit.display_name}") # Mostra de qual sub veio
        print(f"Título: {post.title}")
        print(f"Autor: {author_name}")
        print(f"Criado em: {formatted_time}")
        print(f"Comentários: {post.num_comments}")
        print(f"Score: {post.score}") # Adicionei o score, pode ser útil
        print(f"URL: {post.url}")
        print(f"Link Reddit: https://reddit.com{post.permalink}") # Link permanente do post

        # Pequena pausa para não sobrecarregar a API do Reddit
        time.sleep(0.5) # 0.1 segundos entre cada post

# 3. Capturar exceções de forma mais específica e informativa
except praw.exceptions.PRAWException as praw_error:
    print(f"\nErro específico do PRAW: {praw_error}")
except Exception as e:
    # Captura outros erros (rede, etc.) e mostra a mensagem
    print(f"\nOcorreu um erro inesperado durante a busca: {e}")

print(f"\n--- Busca concluída. {posts_encontrados} posts processados. ---")