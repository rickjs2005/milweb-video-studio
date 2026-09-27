# Produção no Higgsfield

## Conectar intenção e capacidade

Descobrir as ferramentas realmente instaladas: MCP, CLI oficial ou interface permitida. Ler as instruções do workflow nativo adequado. Não presumir que a integração disponível no ChatGPT esteja também disponível no Claude Code. Sem acesso, produzir roteiro, prompts, referências e plano de montagem; identificar a execução pendente.

Consultar catálogo atual para modelo, duração por geração, aspecto, resolução, áudio, referências, controles de câmera e custo. Não fixar nomes de modelos ou chamadas copiadas de versões antigas. Resolver presets nomeados pelo mecanismo oficial antes de substituir por geração genérica. Usar Higgsedit para edição/motion nativos somente quando a ferramenta existir.

## Preparar a geração

1. Converter shot list em tomadas viáveis. Se o filme exceder a duração permitida por geração, dividir em cenas planejadas; não confundir duração de cada clipe com duração final.
2. Definir sujeito, ambiente, ação, composição, câmera, luz, textura e som. Fixar características que precisam persistir entre cenas.
3. Preparar imagens de referência autorizadas. Para transição a uma interface real, obter o quadro de destino antes de gerar a aproximação.
4. Registrar custo estimado quando disponível, quantidade, teto autorizado e limite de tentativas. Uma autorização de orçamento permanece válida; não pedir novamente a cada clipe. Sem teto para execução paga, preparar tudo e pedir apenas essa decisão antes do gasto. Não prometer custo zero se ele for desconhecido.
5. Gerar primeiro o trecho de maior risco. Inspecionar identidade, anatomia, física, movimento, texto e encaixe antes de multiplicar cenas. Reaproveitar tomadas aprovadas.
6. Registrar IDs, parâmetros, modelo/versão quando expostos, prompts, referências, duração e custos reportados. Não guardar tokens ou URLs privadas assinadas em repositório público.

## Estrutura de prompt

```text
Intenção: [o que a tomada precisa comunicar]
Sujeito e continuidade: [características estáveis e referência]
Ambiente/luz: [local, hora, atmosfera e direção da luz]
Composição inicial: [escala, posição, horizonte]
Ação: [uma ação principal executável]
Câmera: [movimento, direção e velocidade]
Composição final: [posição/escala para conectar à tomada seguinte]
Tempo/aspecto: [compatíveis com o modelo escolhido]
Som: [ambiente/fala/silêncio, somente se suportado]
Restrições: [defeitos concretos a evitar; sem lista genérica infinita]
```

Usar a língua de prompt adequada à ferramenta, preservando textos e falas no idioma solicitado. Não prometer que negative prompts, seed ou first/last frame existam em todo modelo. Se a ferramenta não aceitar um controle, adaptar o plano explicitamente.

## Recuperar falhas

Identificar uma causa provável e alterar poucos parâmetros por tentativa. Não regenerar tudo por um defeito local. Registrar tentativas; não ultrapassar teto de custo/quantidade. Se o limite não foi definido, não assumir repetições ilimitadas: pedir um teto para novas gerações pagas ou entregar a melhor alternativa já autorizada.

Imagens e vídeo gerados não dispensam montagem, desenho sonoro, revisão e verificação de direitos. Não afirmar que um arquivo foi renderizado só porque uma geração foi solicitada; aguardar estado concluído e verificar o output.
