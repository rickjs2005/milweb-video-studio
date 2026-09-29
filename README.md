# MilWeb Video Studio

Uma skill em português para escolher a rede social, conduzir um briefing progressivo e criar conteúdo: posts, Pins, carrosséis ou vídeos com pesquisa, direção, roteiro, geração de cenas, edição, áudio e revisão. Feita para **Claude Code** e outros agentes compatíveis com o formato `SKILL.md`.

Serve tanto para um Reel de portfólio quanto para um tutorial longo, uma cena no Higgsfield ou uma correção pontual de montagem. O núcleo é independente de editor; os módulos orientam a escolha da ferramenta disponível.

## O que ela faz

- Pergunta a rede quando ela não foi informada e faz perguntas específicas aos poucos, sem repetir respostas.
- Orienta LinkedIn, Pinterest, Instagram e TikTok com posicionamento e entregas próprios.
- Pesquisa referências atuais e distingue tendência observada de ideia autoral.
- Prioriza ideias e monta calendários conforme público, materiais, tempo e orçamento.
- Analisa métricas sem confundir tempo médio com retenção ou atribuir causas sem evidência.
- Adapta linguagem para Instagram, TikTok, LinkedIn, Pinterest, YouTube, Bilibili e outras redes.
- Planeja roteiro, shot list, ritmo, transições e captura real de sites.
- Prepara geração no Higgsfield com referências, continuidade, orçamento e limite de tentativas.
- Orienta montagem com Remotion, FFmpeg, Higgsedit ou o editor do projeto.
- Trabalha voz, trilha, SFX, legendas e revisão audiovisual.
- Preserva duração e escolhas do briefing, inclusive cenas contemplativas longas.

**A skill não instala um editor, não fornece créditos e não cria conexão automática com Higgsfield.** O agente precisa ter as ferramentas correspondentes. Sem elas, ainda pode pesquisar, dirigir, roteirizar e preparar os prompts.

## Instalar no Claude Code

Com Node.js/npm, use o instalador de skills:

```bash
npx skills add rickjs2005/milweb-video-studio --skill milweb-video-studio -a claude-code -g
```

Revise as opções apresentadas. `-g` instala para uso nos seus projetos; sem essa opção, a instalação é local ao projeto. Confira se o Claude reconhece `/milweb-video-studio`. O instalador é uma ferramenta externa; veja sua [documentação](https://github.com/vercel-labs/skills).

### Alternativa manual no Windows / PowerShell

Na pasta onde você guarda seus repositórios:

```powershell
git clone https://github.com/rickjs2005/milweb-video-studio.git
if ($LASTEXITCODE -ne 0) { throw 'Falha ao clonar o repositorio.' }
$skillTarget = Join-Path $env:USERPROFILE '.claude\skills\milweb-video-studio'
if (Test-Path $skillTarget) { throw 'A skill ja existe. Compare as versoes antes de atualizar.' }
New-Item -ItemType Directory -Force (Split-Path $skillTarget) | Out-Null
Copy-Item -Recurse '.\milweb-video-studio\skills\milweb-video-studio' $skillTarget
```

### Alternativa manual no macOS / Linux

```bash
git clone https://github.com/rickjs2005/milweb-video-studio.git
mkdir -p ~/.claude/skills
if [ ! -e ~/.claude/skills/milweb-video-studio ]; then
  cp -R milweb-video-studio/skills/milweb-video-studio ~/.claude/skills/
else
  echo 'A skill já existe. Compare as versões antes de atualizar.'
fi
```

Para uso somente em um projeto, coloque a pasta da skill em `.claude/skills/milweb-video-studio/` dentro dele. Não copie a raiz inteira do repositório para a pasta de skills. Abra uma nova sessão se ela ainda não aparecer. Consulte o formato na [documentação do Claude Code](https://code.claude.com/docs/en/skills).

Se você já usa `milweb-video` ou `edicao-video-capcut`, mantenha os arquivos antigos enquanto compara as versões. Invoque esta skill pelo nome para testar; não é necessário apagar outras skills.

## Escolha da rede e perguntas progressivas

Comece com `/milweb-video-studio Quero criar conteúdo de um site meu.`

Sem uma rede definida, a skill pergunta: **“Para qual rede vamos criar: LinkedIn, Pinterest, Instagram ou TikTok?”** Depois segue com perguntas sobre objetivo, público, projeto, materiais e formato, uma por vez ou duas relacionadas. Se você já informou algo, ela não pergunta de novo. Outros destinos, como YouTube e sites, continuam disponíveis.

| Rede | Posicionamento inicial para a MilWeb | Entregas possíveis |
|---|---|---|
| LinkedIn | Autoridade e conexões profissionais | Case, aprendizado, post, documento/carrossel ou vídeo |
| Pinterest | Portfólio visual e estética sofisticada | Pin, composição de telas, série visual ou vídeo |
| Instagram | Confiança, projetos e contato comercial | Reel, carrossel, Stories e legenda |
| TikTok | Personalidade, humor, bastidores e experimentos | Ideia, roteiro e vídeo adaptado ao público |

São direções de marca, não garantias de desempenho. A pesquisa é adequada a cada destino: trends e formatos em Instagram/TikTok, discussões e cases no LinkedIn, buscas e referências visuais no Pinterest. Falta de acesso ou evidência deve ser declarada.

As quatro especialidades estão no mesmo pacote. Conteúdo estático não exige produção de vídeo; pedidos de planejamento não autorizam publicação ou geração paga.

## Primeiro teste, sem gastar créditos

No Claude Code:

```text
/milweb-video-studio
Quero planejar um vídeo de 30 a 45 segundos para TikTok e Instagram Reels.
Tema: [o que quero mostrar]. Público: [quem quero alcançar].
Tenho estas gravações ou imagens: [descreva os materiais].
Pesquise referências recentes do meu nicho e explique o que conseguiu verificar.
Proponha a abertura, o roteiro por cena, os cortes, as legendas e o áudio.
Explique o que adaptar em cada rede e como avaliar o resultado.
Nesta etapa, entregue apenas o plano. Não gere mídia nem use serviços pagos.
```

Substitua os campos entre colchetes pelo seu contexto. A skill deve separar referências verificadas de hipóteses, propor uma timeline e respeitar os materiais disponíveis. Se não conseguir pesquisar uma rede, deve declarar a limitação. O teste não autoriza geração paga; o uso do agente continua sujeito ao seu plano. Veja outros [prompts de uso](examples/prompts.md) e os [critérios de avaliação](docs/validation.md).

Para um trabalho real, informe URL ou arquivos, objetivo, público, destino, duração e orçamento quando houver geração paga. Não envie tokens ou senhas no prompt.

## Módulos

| Arquivo | Papel |
|---|---|
| [SKILL.md](skills/milweb-video-studio/SKILL.md) | Escopo, fluxo, seleção de módulos e critérios centrais |
| `social-networks.md` | Escolha da rede, perguntas progressivas e quatro especialidades sociais |
| `research.md` | Pesquisa e qualidade de evidência |
| `content-strategy.md` | Prioridades, formatos e calendário editorial |
| `performance.md` | Métricas, hipóteses e testes de conteúdo |
| `platforms.md` | Linguagem por destino e versões |
| `direction.md` | Roteiro, ritmo e transições |
| `footage.md` | Captura real e inventário de mídia |
| `higgsfield.md` | Geração, continuidade e orçamento |
| `editing.md` | Montagem, motion e motores |
| `audio.md` | Voz, música, efeitos e legendas |
| `quality.md` | Revisão técnica, perceptiva e editorial |
| `templates.md` | Briefing, shot list, fontes e QA |
| `sources.md` | Documentação e projetos de referência |

Os módulos ficam em `skills/milweb-video-studio/references/` e são carregados conforme a tarefa. Não há instalação automática de dependências nem hooks.

## Verificação técnica opcional

O único script incluído lê metadados e pode decodificar um vídeo local. Requer **Python 3.10+**, **ffprobe** e, para `--decode`, **ffmpeg** no PATH.

```bash
python skills/milweb-video-studio/scripts/media_audit.py final.mp4 --min-duration 25 --require-audio --decode
```

O resultado JSON não é aprovação estética: não confirma que a savana durou 25 segundos, que o som está bom ou que a transição funciona. Ele mede a duração global e verifica as condições técnicas solicitadas. Não altera a mídia e não usa a rede.

Para executar os testes locais, com os mesmos requisitos:

```bash
python -m unittest discover -s tests -v
```

## Escopo desta versão

Versão **0.3.0**: adiciona briefing progressivo e especialidades para LinkedIn, Pinterest, Instagram e TikTok, com pesquisa por destino e suporte a posts, Pins e carrosséis. Preserva planejamento de conteúdo, análise de resultados e critérios de evidência da versão anterior. Os módulos são instruções editoriais, não um motor autônomo de vídeo. A integração paga com Higgsfield e a execução dentro do Claude Code precisam ser testadas no ambiente do usuário. Não há promessa de viralização, “transição perfeita” ou resultado cinematográfico automático.

O conteúdo é original e usa projetos públicos como referências de estudo, sem incorporar seus arquivos. Veja [fontes](skills/milweb-video-studio/references/sources.md) e [licenças de terceiros](THIRD_PARTY.md).

## Contribuir

Abra uma issue com briefing anonimizado, comportamento observado, resultado desejado e versões das ferramentas. Para propor uma regra, explique seu contexto e exceções. Não envie vídeos privados, credenciais ou conteúdo de clientes sem autorização.

Licença [MIT](LICENSE) para os arquivos deste repositório. Serviços, ferramentas, modelos e mídias usados com a skill têm condições próprias. Projeto independente da MilWeb; não é produto oficial da Anthropic, OpenAI, Remotion ou Higgsfield.
