#--kind python:default
#--web true
#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param OLLAMA_TOKEN $AUTH
#--param MILVUS_HOST $MILVUS_HOST
#--param MILVUS_PORT $MILVUS_PORT
#--param MILVUS_DB_NAME $MILVUS_DB_NAME
#--param MILVUS_TOKEN $MILVUS_TOKEN
#--param S3_HOST $S3_HOST
#--param S3_PORT $S3_PORT
#--param S3_API_URL $S3_API_URL

import rag
def main(args):
  return { "body": rag.rag(args) }
