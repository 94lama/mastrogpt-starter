#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param AUTH $AUTH
#--param S3_HOST $S3_HOST
#--param S3_PORT $S3_PORT

import form
def main(args):
  return { "body": form.form(args) }
