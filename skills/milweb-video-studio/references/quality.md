# Revisão e entrega

## Conferir em três níveis

| Nível | O que verificar | Evidência |
|---|---|---|
| Técnico | Duração, streams, resolução, fps, codec, erros de decode | ffprobe/ffmpeg e relatório |
| Perceptivo | Movimento, junções, legibilidade, som e sincronização | Reprodução e escuta reais |
| Editorial | Restrições do briefing, narrativa, prova, identidade, CTA | Timeline, material real e revisão contextual |

Um nível não substitui os outros. Arquivo existente e metadados corretos não provam vídeo bom. Quadros extraídos não comprovam fluidez; waveform ou transcrição não comprovam mixagem.

## Usar o verificador incluído

Executar a partir de qualquer pasta, apontando o caminho real da skill:

```bash
python /caminho/da/skill/scripts/media_audit.py final.mp4 --min-duration 25 --require-audio --decode
```

Requer Python 3.10+ e ffprobe; `--decode` requer ffmpeg. Não instala dependências, não acessa a rede e não modifica a mídia. Retorna JSON no stdout: código 0 indica que as verificações técnicas solicitadas passaram; 1 indica erro/requisito não atendido; 2 indica argumentos inválidos. Sem `--require-audio`, vídeo silencioso é permitido. Sem `--decode`, decodificação fica explicitamente não verificada. O timeout padrão é 120 s por subprocesso; pode ser ajustado para vídeos longos.

`--min-duration` verifica duração global, não duração da savana, de uma fala ou de qualquer segmento semântico. Verificar esses requisitos na timeline e na reprodução. O script não mede loudness, não avalia sincronização e não confirma licença, cor, estética ou parâmetros atuais de uma rede.

## Revisão final

- Comparar a versão capturada do site (desktop/mobile/ambas), enquadramento, zoom/crop e elementos adicionados com as decisões do briefing. Conferir separadamente legendas de fala, títulos/CTA e texto original da interface. Corrigir divergências; não justificar adições não combinadas como “melhor para o algoritmo”.

- Confirmar duração total e intervalos mínimos no filme final, contabilizando transições sobrepostas.
- Reproduzir o início, fim e todas as junções críticas; para aprovação final, assistir à peça completa. Em vídeos longos, amostragem pode apoiar diagnóstico, mas não equivale a revisão integral.
- Conferir quadros pretos, congelamentos, flash frames, cortes de texto, pixelização, logos e conteúdo real. Detectores automáticos geram candidatos: plano estático ou fade preto pode ser intencional.
- Ouvir voz, música, ambiente e SFX; conferir ausência de placeholders, clipping perceptível, falhas, problemas de sincronização e finais truncados.
- Conferir nomes, números, legendas e afirmações de resultados. Não fabricar prova comercial.
- Verificar aspecto, composição e área segura de cada versão. Registrar fontes das especificações atuais de export.

## Comunicar o estado honestamente

Marcar cada item como `verificado`, `falhou`, `não aplicável` ou `não verificado`, com evidência curta. Corrigir falhas verificáveis antes de encerrar.

Se reprodução/escuta estiver indisponível, entregar o arquivo como **versão para revisão**, com as verificações técnicas realizadas e a pendência explícita. Não alegar “assisti”, “ouvi” ou “aprovado integralmente” sem tê-lo feito. Não bloquear indefinidamente uma entrega útil pela ausência de ferramenta perceptiva.

Fornecer somente links/arquivos existentes. Identificar duração, formato, mudanças e limitação material. Incluir fontes/projeto quando solicitado e permitido. Não chamar um vídeo de publicado quando ele só foi exportado.

## Recorte, 3D e interfaces em camadas

- Conferir cabelo, mãos, óculos, microfone e cabos em movimento; revisar halos, cintilação e perda de partes sobre fundos claros/escuros.
- Verificar ordem de oclusão, contato, perspectiva, iluminação e estabilidade entre estados do cenário. Testar a composição além de um único frame favorável.
- Em UI reconstruída, comparar o estado final com captura real: fontes, cores, layout e conteúdo. Não chamar uma animação ilustrativa de demonstração funcional.
- Em render segmentado, conferir frames e áudio das fronteiras. Em 3D por código, verificar determinismo e assets carregados.
- Registrar separadamente: plano verificado, amostra renderizada, reprodução/escuta verificadas e produção completa. Uma prova curta não certifica todo o vídeo.
