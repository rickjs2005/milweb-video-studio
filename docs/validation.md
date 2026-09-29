# Histórico de validação

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
