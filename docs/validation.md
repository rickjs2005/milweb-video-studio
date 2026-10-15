# Histórico de validação

## Versão 0.7.0 — 15/10/2026

Fluxo executável para análise local, composição por referência, render HyperFrames, comparação, voz local, ASR e legendas. Esta revisão gerou arquivos de vídeo reais, além de atualizar as instruções.

- Validador estrutural da skill aprovado; metadados regenerados pelo gerador oficial. `python -m unittest discover -s tests -v`: **17 testes aprovados**, sem rede/modelos nos testes de integração.
- Testes cobrem preservação dos originais/anotações, acentos/espaços, injeção de conteúdo como JSON, bloqueio de escape de template e de render vazio, decode/loudness, proporções distintas, legendas queimadas com escala correta em retrato e regressão de fps inteiro/fracionário.
- Demo original de motion: **10,000 s, 1080×1920, 30 fps, H.264, áudio AAC**. Render final em Linux, GPU por software, 1 worker: 58,3 s, com fonte local; não é previsão de desempenho em outro computador. Check: zero erros em lint/runtime/layout/motion/contraste; dois avisos de estrutura monolítica das cenas.
- Decode completo do demo aprovado; sem intervalos pretos/silêncio detectados. Som sintético medido em −17,88 LUFS e −7,17 dBTP. Quadros do MP4 inspecionados, incluindo entradas, composição final e transição entre cenas. Reprodução integral e escuta perceptiva não foram verificadas.
- Kokoro ONNX 0.6.1 com modelo int8 local e voz `pf_dora`, pt-BR: gerou 6,953 s de fala. faster-whisper 1.2.1, modelo `small` em CPU, transcreveu corretamente as duas frases do teste e gerou SRT/JSON com palavras/timestamps. O modelo `tiny` errou parte da segunda frase; ASR continua exigindo revisão. Não foi usado serviço de voz ou transcrição pago.
- Um agente em contexto separado recebeu uma referência sintética de 2 s e o novo texto “Aprender, um passo de cada vez”. Executou análise, escreveu composição própria, preservou o fundo/áudio e entregou **MP4 de 2,000 s, 320×180, 12 fps, 24 quadros**, com frase legível em duas linhas. Check sem erros/avisos; comparação por cenas e quadro do MP4 inspecionados. Decode aprovado, áudio presente, −18,78 LUFS e −16,23 dBTP.
- O teste independente encontrou a rejeição de `--fps 12.0` pelo HyperFrames. O wrapper foi corrigido para passar inteiro/fração canônica, e o agente repetiu o render com `canvas.fps=12.0`, sem workaround. A prévia Studio ao vivo falhou neste ambiente; a saída MP4 foi validada. O player local de revisão não depende dessa prévia Studio.

As referências reais do usuário continuavam inacessíveis neste ambiente. Os demos sintéticos validam o fluxo técnico; não provam fidelidade aos vídeos originais, qualidade perceptiva de áudio nem execução dentro do Claude Code/Windows. Os modelos ficam fora do repositório; nenhuma integração ou reconstrução do CRM foi realizada.

## Versão 0.6.0 — 07/10/2026

Cinco definições de subagentes para Claude Code, coordenação por canal, YouTube Shorts, vídeo longo independente e estudo de referência orientado por evidências.

- Links relativos dos arquivos alterados conferidos contra a árvore do repositório; cinco definições de agentes presentes, com name/description/skills e sem modelo/permissão fixados.
- Definições seguem os campos e locais documentados em https://code.claude.com/docs/en/sub-agents, consultada em 07/10/2026.
- Um agente em contexto separado leu seis arquivos no commit de revisão e respondeu a três cenários: pacote de cinco redes com restrições explícitas; duas referências inacessíveis; episódio independente de 12 minutos.
- O pacote recebeu propostas distintas sem refazer perguntas respondidas; desktop inteiro, ausência de voz/texto e proibição de pesquisa foram preservados. Referências inacessíveis ficaram pendentes, sem cenas inventadas. O longo iniciou briefing próprio, sem Shorts ou cinco agentes sociais.
- Ajustada a redação do perfil Instagram para explicitar a exceção de pesquisa proibida pelo usuário.

Esta validação cobre leitura de instruções e primeiras respostas de planejamento. Não executou os agentes dentro de Claude Code, gravação, geração, render, instalação em Windows nem comparação audiovisual. A versão instalada no computador do usuário não foi alterada. O script de mídia não mudou; seus testes anteriores não foram repetidos.

### Referências enviadas nesta revisão

- https://www.tiktok.com/@ivanxuugarcia/video/7691379990612430112
- https://www.tiktok.com/@rikibosso/video/7692145103363738912

As páginas foram tentadas por leitura web e reprodução no navegador. A reprodução retornou erro para ambos; nenhum trecho audiovisual foi observado. Os links permanecem referências pendentes de mídia acessível. Não fundamentam afirmações de técnicas, ritmo, som, qualidade alcançada ou superioridade. O módulo de estudo define o procedimento a aplicar quando os arquivos estiverem disponíveis.

## Versão 0.5.1 — 30/09/2026

Regras explícitas de captura desktop/mobile, enquadramento e elementos acrescentados. Validador estrutural e diff sem erros. Nenhum script de mídia foi alterado.

Um agente em contexto separado recebeu dois cenários, sem respostas esperadas e sem mídia ou produção:
- Reel vertical com captura nova e layout não informado: perguntou desktop/mobile/ambos antes de gravar.
- Plano com gravação desktop inteira, sem voz/texto e com áudio original: preservou a composição com margens, sem propor legendas nem troca para mobile. Declarou a ausência do arquivo e a dependência da duração para fechar o plano.

Verificação de primeiras respostas, sem execução de captura/edição e sem avaliação audiovisual.

## Versão 0.5.0 — 30/09/2026

Atualização de instruções para briefing criativo e diagnóstico de insatisfação. O script de mídia não mudou; testes técnicos anteriores não foram repetidos.

- Validador estrutural aprovado e links locais conferidos.
- Um agente em contexto separado leu a skill e respondeu a três cenários independentes, sem respostas esperadas, pesquisa externa, edição, render ou serviços pagos.
- Pedido vago “Quero um Reel do meu site”: perguntou sobre a intenção do vídeo, sem iniciar um roteiro.
- Feedback “não gostei… ficou estranho”, sem arquivo: perguntou o ponto de insatisfação, sem alegar inspeção da mídia ou inventar causa.
- Briefing completo de Reel de 30 s: entregou plano que soma 30 s, preservando ritmo calmo, desktop antes de mobile, ausência de narrador e de oferta, sem perguntas redundantes.

Este ensaio verifica primeiras respostas e planejamento. Não valida uma conversa inteira de briefing, a execução dentro do Claude Code nem a qualidade estética de um vídeo renderizado.

## Versão 0.4.0 — 29/09/2026

Atualização de instruções e documentação para composição em camadas, recorte, cenários virtuais, 3D e construção visual de sites. O script de mídia não mudou; os testes técnicos de 0.1.0 não foram repetidos.

- Validador estrutural aprovado na skill instalada; links internos e blocos Markdown conferidos.
- Um agente em contexto separado recebeu a skill e um pedido apenas de plano: Reel de 30 s, apresentador com câmera em movimento e mãos diante do rosto, captura única do hero, notebook com 8 GB e sem ferramentas pagas.
- O plano preservou 30 s, separou hipótese técnica de alegação de edição ao vivo, identificou riscos de recorte e manteve a captura como demonstração visual, sem inventar navegação. Propôs camadas 2D, proxies, uma prova futura do trecho difícil e alternativa caso a máscara falhasse. Não gerou mídia nem executou render.

Esse ensaio valida comportamento de planejamento. Não confirma qualidade de recorte, desempenho de render, reconstrução 3D ou resultado audiovisual final. Esses itens precisam ser verificados com mídia e ferramentas reais no projeto de produção.

## Versão 0.2.0 — 28/09/2026

Mudança de instruções e documentação: pesquisa com nível de inspeção, estratégia/calendário, métricas e proteção de informações na captura. O script de mídia não foi alterado; os oito resultados técnicos abaixo pertencem à validação de 0.1.0 e não foram repetidos nesta revisão.

- Validador estrutural aprovado na skill instalada.
- Links locais e fechamento dos blocos Markdown verificados.
- Dois cenários novos executados por agentes com contexto separado, sem geração, publicação ou pesquisa externa:

| Entrada de teste | Resultado observado |
|---|---|
| Dois posts fictícios com formatos/durações e idades diferentes; médias de visualização sem curva; um viral anterior | Distinguiu média, índice relativo e retenção; recusou inferências sobre primeiros 3 s, horário e punição; propôs comparação com janelas equivalentes |
| Relatório baseado em miniaturas, busca por mais curtidos e comparação de dois países; duas horas de produção e ausência de versão antiga | Separou tema de ritmo não observado; rejeitou declínio e generalização geográfica; propôs três peças com 120 min estimados e sem inventar antes/depois |

Esses testes verificam comportamento de planejamento/análise, não execução de vídeo ou desempenho real em redes sociais. Os dados e afirmações fornecidos nos cenários são entradas de teste, não fatos adotados pela skill. O relatório recebido do usuário não foi publicado; foram incorporadas regras gerais escritas para este projeto.

## Versão 0.1.0 — 27/09/2026

Executada em 27/09/2026. Estes resultados descrevem o que foi testado; não certificam a qualidade de todo vídeo futuro.

## Estrutura

- Frontmatter `name`/`description` e nome da skill passaram no validador estrutural.
- Núcleo organizado por escopo e referências carregadas conforme a tarefa.
- Arquivos de publicação e exemplos separados da pasta instalável.

## Script de mídia

Oito testes de integração passaram com mídia sintética gerada localmente:

1. Arquivo válido com áudio, decode completo, caminho com espaços/acentos e hash do original preservado.
2. Rejeição de áudio ausente quando obrigatório.
3. Aceitação de vídeo silencioso quando áudio não é obrigatório.
4. Rejeição de duração menor que o mínimo solicitado.
5. Rejeição de duração maior que o máximo solicitado.
6. Erro legível para arquivo inexistente.
7. Rejeição de arquivo corrompido.
8. Rejeição de argumentos negativos, não finitos ou intervalo invertido.

Reprodução: `python -m unittest discover -s tests -v` com Python e FFmpeg disponíveis. Os testes geram e removem apenas seus arquivos temporários. Não usam rede nem serviços pagos.

## Cenários editoriais executados

Dois agentes em contextos separados receberam a skill e solicitações de planejamento, sem respostas esperadas. Não tiveram autorização para gerar mídia ou gastar créditos.

| Pedido | Comportamento observado |
|---|---|
| Roteiro/prompts de 60 s, mínimo 25 s de savana antes do site, hero ainda ausente | Timeline de 60 s, 44 s de savana, hero como referência pendente e interface real prevista; sem geração |
| Tutorial de oito minutos e versão LinkedIn de 90 s, com pausas naturais | Capítulos totalizando oito minutos, estrutura própria para LinkedIn e preservação das pausas; sem impor duração curta |

Os tempos de cada tomada generativa ainda precisam ser adaptados ao modelo disponível na produção. O teste de planejamento não verificou catálogo, execução ou cobrança do Higgsfield.

## Testar no seu Claude Code

1. Instalar e invocar `/milweb-video-studio` com um exemplo de planejamento.
2. Conferir se o agente acessa as referências correspondentes e respeita escopo/duração.
3. Enviar um vídeo curto e pedir apenas análise; conferir se informa o que foi realmente visto, ouvido e medido.
4. Pedir um ajuste pontual e verificar se preserva o restante do trabalho.
5. Para geração paga, fornecer orçamento e limite de tentativas antes da execução.

Ainda não verificados nesta versão: instalação executada em Windows real; execução dentro do Claude Code; render completo em Remotion/Higgsedit; geração paga no Higgsfield; qualidade perceptiva de um filme produzido de ponta a ponta. A validação técnica local não substitui esses testes.
