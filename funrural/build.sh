#!/bin/sh
# Gera o index.html autônomo (abre direto no navegador, funciona offline) a partir de src/body.html
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8">\n'
  printf '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
  printf '<meta name="theme-color" content="#2d3867"><link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon.svg">\n'
  printf '<style>body{margin:0}img{max-width:100%%}[hidden]{display:none!important}</style>\n</head><body>\n'
  cat src/body.html
  printf '\n</body></html>\n'
} > index.html
