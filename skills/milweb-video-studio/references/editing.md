# Montagem e motion

## Escolher o motor

| Ferramenta | Preferir para | Verificar antes |
|---|---|---|
| Remotion | Composição programática, versões, texto e UI | Versão, licença, assets e render mínimo |
| FFmpeg | Cortes, conversão, composição simples, análise | Build/filtros disponíveis e precisão temporal |
| Higgsedit | Edição e motion no ambiente Higgsfield | Ferramentas nativas e workflow presentes |
| CapCut/DaVinci/Premiere | Montagem manual e intercâmbio solicitado | Acesso real; compatibilidade do projeto/export |
| HyperFrames | HTML/CSS/GSAP com timeline controlada | Exemplo pequeno e documentação atual |
| MoviePy | Pipeline Python já existente | API da versão instalada e codecs |

Não instalar todos os motores. Preferir o projeto/ferramenta existente que cumpre o briefing. Não alegar entrega de projeto nativo CapCut sem arquivo compatível efetivamente produzido.

## Procedimento

1. Definir timeline, fps, aspecto, resolução e convenção de timestamps. Usar intervalos `[início, fim)`; converter para frames quando o motor exigir. Arredondar deliberadamente e verificar duração final.
2. Validar inputs antes do render: arquivos decodificáveis, fontes presentes, áudio e dimensões esperadas. Medir um trecho problemático primeiro.
3. Fazer corte estrutural; depois ajustar ritmo, som, cor, textos e movimento. Não mascarar falha de conteúdo com efeitos.
4. Usar motion para orientar atenção: entrada, permanência legível e saída. Curvas suaves para câmera/UI, spring apenas quando a intenção justificar. Manter hierarquia; não animar tudo simultaneamente.
5. Preservar origem de alta qualidade. Gerar versões a partir do master/projeto ou fontes, evitando sucessivas recompressões de versões já comprimidas.
6. Verificar compatibilidade real ao concatenar. `-c copy` pode cortar em keyframes e não garante precisão de quadro; para corte exato, escolher processo apropriado e verificar os limites.

## Remotion

Consultar skills/documentação oficiais para a versão do projeto. Controlar animação pelo frame/fps; usar aleatoriedade determinística quando necessária. Não depender de relógio, `Date.now()`, temporizadores ou animação CSS não sincronizada para o render.

Documentar offsets locais/globais de `Sequence`: ao aninhar, testar entrada e saída reais para evitar contagem duplicada. Precarregar assets pelo mecanismo documentado; não renderizar enquanto fontes ou mídia ainda carregam. Usar caminhos portáveis e travar versões no lockfile.

Medir custo de blur, sombras, `backdrop-filter`, partículas e 3D. Reduzir complexidade do trecho problemático antes de simplesmente aumentar recursos. Se renderizar em partes, garantir estado determinístico, continuidade de áudio, frames de fronteira e compatibilidade dos segmentos.

Não aplicar `-g 1` como cura universal: GOP intra pode aumentar muito o arquivo. Usar apenas quando uma necessidade de acesso a frames/intermediário justificar, e documentar o trade-off.

## Cor e imagem

Conferir níveis, balanço, exposição, consistência e transformação de cor entre fontes. Não aplicar LUT que destrua tons de pele ou produto. Verificar gamma, range e HDR/SDR conforme origem/destino; não “corrigir” um problema de interpretação de cor com grading arbitrário.

## Entrega editável

Organizar fontes autorizadas, referências relativas, código/timeline, fontes e instruções mínimas de reprodução. Excluir caches, credenciais e mídia sem direito de redistribuição. Informar dependências externas e versões; um MP4 não é um projeto editável.

## Composição avançada

Para recorte de pessoa, troca de fundo, cenários construídos em etapas, objetos 3D ou site montado em camadas, ler [compositing-vfx.md](compositing-vfx.md). Separar assets, máscaras, oclusão e movimentos antes da implementação. Executar prova curta do efeito de maior risco quando houver autorização de produção; preservar a fase de planejamento quando somente ela for solicitada.
