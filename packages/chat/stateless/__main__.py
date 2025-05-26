#--kind python:default
#--web true
#TODO:E2.1
#--param AUTH $AUTH
#--param HOST $OLLAMA_HOST
#END TODO

import stateless
def main(args):
  return { "body": stateless.stateless(args) }
