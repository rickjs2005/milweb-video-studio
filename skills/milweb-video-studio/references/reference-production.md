# Produzir a partir de um vídeo de referência

## Conteúdo

1. Entrada e decisões
2. Ferramentas locais
3. Análise e adaptação
4. Construção e revisão
5. Voz e legendas
6. Uso com CRM e assinatura

## 1. Entrada e decisões

Usar este fluxo quando o pedido for “faça um vídeo como este, com meu conteúdo”, “recrie esta animação”, ou concluir a implementação dessa capacidade. A referência atual é a direção criativa principal. Extrair dela composição, movimento, ritmo e presença de texto/voz, respeitando as mudanças explicitadas no pedido. Não importar proibições ou preferências de produções anteriores como regras permanentes. Distinguir títulos de design de legendas de fala.

Quando “igual” abranger o vídeo inteiro, registrar os elementos observados a preservar. Não acrescentar uma rodada de escolhas já resolvidas pela referência. Perguntar somente por conteúdo novo essencial ausente ou por ambiguidade que mude a peça inteira. Se houver várias referências, esclarecer qual governa qual aspecto apenas quando não estiver definido. Nunca presumir que a peça é de divulgação da MilWeb ou que vídeos de redes diferentes têm a mesma direção.

Separar a animação exibida dentro de uma tela da filmagem externa dessa tela; usar o alvo declarado pelo usuário. Sem alvo claro, fazer uma pergunta curta. Não escolher por ele somente para destravar um teste.

Em pedido de implementação da skill, validar as ferramentas com uma demonstração identificada. Uma demonstração técnica não prova fidelidade a referências inacessíveis. Não condicionar a implementação de ferramentas à escolha de um vídeo definitivo.

## 2. Ferramentas locais

Requisitos básicos: Python 3.10+, FFmpeg/ffprobe. Render HTML: Node 22+, HyperFrames e navegador local. Voz e ASR são opcionais. Os scripts não fazem chamadas a APIs de IA nem acionam geração paga. Downloads iniciais de pacotes/modelos ainda precisam de internet.

Nos comandos abaixo, substituir literalmente `SKILL_DIR` pelo caminho absoluto da pasta real desta skill, entre aspas se houver espaços. Usar argumentos separados e caminhos absolutos quando houver dúvida; os exemplos abaixo usam `python`, compatível com o lançador configurado no ambiente do usuário.

```bash
python SKILL_DIR/scripts/studio.py doctor
python SKILL_DIR/scripts/studio.py new videos/meu-projeto --reference referencia.mp4 --brief briefing.txt --duration 20 --width 1080 --height 1920 --fps 30
npm --prefix videos/meu-projeto install
node videos/meu-projeto/node_modules/hyperframes/bin/hyperframes.mjs browser ensure
python SKILL_DIR/scripts/studio.py analyze referencia.mp4 --out videos/meu-projeto/analysis/ref-01
```

`new` cria `project.json`, `content.json`, `reference-map.json`, `composition.html.in`, dependências fixadas e diretórios locais. O HTML inicial é um esqueleto; substituir o marcador `MILWEB_UNAUTHORED_SCAFFOLD` e escrever as cenas antes dos checks/render. `--fps` aceita número ou fração, como `30000/1001`. `--demo` escolhe explicitamente uma demonstração própria de 10 segundos em 9:16, com animação e som sintético; não é o template padrão para vídeos de clientes. Para outra duração/proporção, criar o demo primeiro e retimar/redesenhar suas cenas.

A fonte Inter variável é instalada junto das dependências do projeto e referenciada localmente, para evitar buscar fontes durante o render. Usar fontes locais autorizadas nas composições finais e preservar seus termos de licença.

Para um link público fornecido, usar `studio.py fetch URL --out referencias` se yt-dlp já estiver disponível. Não enviar cookies nem tentar contornar login/bloqueios. Se não houver mídia acessível, registrar o bloqueio e pedir o arquivo uma vez. Os caminhos retornados são os arquivos realmente baixados. Guardar vídeos privados fora do repositório público.

Para cada reanálise, escolher diretório novo: o script recusa sobrescrever anotações existentes. Não analisar arquivos de cliente dentro da pasta pública da skill.

## 3. Análise e adaptação

Ler `analysis.json`, a folha de contato e as sequências densas ao redor dos eventos. A varredura usa diferenças visuais em baixa resolução e uma grade temporal; não detecta automaticamente a semântica de um movimento. Mudança de quadro pode ser animação contínua, câmera ou corte. Aumentar `--sample-fps`, reduzir `--threshold` ou escolher `--start`/`--end` para investigar um trecho; não confundir ausência de eventos com ausência de movimento.

Abrir `review.html` para reprodução em velocidade normal e reduzida quando houver capacidade. Ouvir o áudio quando disponível. Preencher `observed` e `hypotheses` separadamente, com timestamps e o nível de acesso realizado. Revisão por imagens permanece distinta de reprodução; transcrição não prova mixagem ou sincronização musical.

Preencher `reference-map.json` com cenas executáveis, sem nota automática de “semelhança”:

```json
{
  "schema": "milweb.reference-map/1",
  "scenes": [{
    "reference_range": [0, 2],
    "output_range": [0, 2.5],
    "observed": "Preencher após ver o trecho real",
    "preserve": {"composition": "", "movement": "", "timing": "", "sound": ""},
    "replace": {"text": "Conteúdo fornecido", "assets": []},
    "recipe": {"source": "", "implementation": "", "adaptation": ""},
    "acceptance": "Qual movimento e quadro permitem verificar a adaptação?"
  }]
}
```

Quando o conteúdo novo mudar comprimento de texto, número de elementos ou aspecto, recalcular layout e duração legível. Não simplesmente trocar palavras mantendo coordenadas que deixam o texto cortado. Converter frames de uma receita para segundos usando o fps dela antes de transferir o movimento.

## 4. Construção e revisão

Carregar apenas a skill externa necessária e ler sua receita e implementação concreta antes de adaptar. Não instalar todas as coleções nem usar seus defaults estéticos para substituir a referência:

- [HyperFrames core](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-core/SKILL.md): contrato de composição e timeline pausada.
- [HyperFrames animation](https://github.com/heygen-com/hyperframes/blob/main/skills/hyperframes-animation/SKILL.md): regras, transições e adaptadores; ler a regra escolhida e seu código.
- [Video Shotcraft: card progressivo](https://github.com/Vincentwei1021/video-shotcraft/blob/main/references/shots/ui-entrance/product-card-progressive-assemble.md) e [TSX correspondente](https://github.com/Vincentwei1021/video-shotcraft/blob/main/demos/ui-entrance/product-card-progressive-assemble/ProductCardProgressiveAssemble.tsx): referência de coreografia, não um estilo universal.
- [Charlie Hills](https://github.com/charlie947/motion-graphics-skills): identidade, efeitos e loops; distinguir a skill que escreve prompts daquela que constrói efeitos.
- [iart motion design](https://github.com/iart-ai/motion-design-skills): selecionar direção, composição ou sincronização conforme o efeito observado.
- [gitethanwoo/video-editing](https://github.com/gitethanwoo/video-editing) e [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill): complementar análise e processamento quando necessário.

Escrever a composição própria em `composition.html.in` e o conteúdo em `content.json`. O render prepara `index.html`, substituindo `{{WIDTH}}`, `{{HEIGHT}}`, `{{FPS}}`, `{{DURATION}}` e `{{CONTENT}}`. A injeção de conteúdo é JSON escapado; usar `textContent` para texto. Não editar só `index.html`: ele é gerado novamente. Referenciar assets locais com caminhos relativos. O runtime é uma timeline GSAP pausada registrada na composição; não usar relógio de parede nem aleatoriedade não determinística.

```bash
python SKILL_DIR/scripts/studio.py check videos/meu-projeto
python SKILL_DIR/scripts/studio.py snapshot videos/meu-projeto --at 0.5,2,4
python SKILL_DIR/scripts/studio.py render videos/meu-projeto --name previa.mp4 --quality draft --workers 1
python SKILL_DIR/scripts/studio.py verify videos/meu-projeto/renders/previa.mp4 --duration 20 --out videos/meu-projeto/renders/qc.json
python SKILL_DIR/scripts/studio.py compare referencia.mp4 videos/meu-projeto/renders/previa.mp4 --map videos/meu-projeto/reference-map.json --out videos/meu-projeto/renders/comparacao-01
```

Antes da prévia, retimar o projeto para conter o trecho de maior risco; não reduzir `data-duration` cortando a referência ao acaso. Inspecionar as imagens e reproduzir o resultado quando possível. Corrigir o desvio principal e continuar até o render completo quando já autorizado. Ajustar workers à memória e ao tempo medidos; 1 é um início conservador, não uma regra universal.

`check` verifica a composição. `verify` faz decode e mede loudness/true peak, intervalos pretos e silêncio quando aplicável. Um silêncio ou plano preto pode ser intencional. `compare --map` usa intervalos correspondentes; sem mapa, a comparação é apenas temporal normalizada e não comprova movimento equivalente. Nenhuma medição substitui revisão editorial ou auditiva.

Entregar MP4, projeto com fontes/assets autorizados, configuração de conteúdo, versões e instruções reproduzíveis. Marcar os itens que realmente passaram. Não alegar “igual ao vídeo” a partir de checks técnicos ou imagens isoladas. Para projetos existentes em Remotion, preservar esse motor e usar suas skills oficiais; o wrapper HyperFrames não converte TSX automaticamente.

## 5. Voz e legendas

Instalar somente se o briefing exigir: `python -m pip install kokoro-onnx==0.6.1 soundfile==0.14.0 faster-whisper==1.2.1`. Instalar modelos separadamente, fora do repositório. A [implementação Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx) usa pesos/vozes locais. Conferir o idioma e a voz disponíveis no arquivo de vozes escolhido.

```bash
python SKILL_DIR/scripts/speech.py narrate roteiro.txt --model MODELOS/kokoro-v1.0.int8.onnx --voices MODELOS/voices-v1.0.bin --voice pf_dora --language pt-br --out videos/meu-projeto/assets/voz.wav
python SKILL_DIR/scripts/speech.py transcribe videos/meu-projeto/assets/voz.wav --model small --language pt --out videos/meu-projeto/assets/legendas.srt
python SKILL_DIR/scripts/speech.py captions videos/meu-projeto/renders/final.mp4 --srt videos/meu-projeto/assets/legendas.srt --out videos/meu-projeto/renders/legendado.mp4
```

ASR usa somente modelos já presentes por padrão; `--download-model` permite explicitamente obter o modelo público na primeira execução. Não há fallback para API. Revisar palavras, números, nomes e negações antes de embutir. Os timestamps de faster-whisper não são alinhamento forçado; usar WhisperX ou outra ferramenta de alinhamento quando a precisão exigir, respeitando hardware/modelos.

O burn-in SRT calcula a fonte conforme o canvas e fixa a resolução ASS para evitar letras gigantes em vídeo vertical. `--size` permite informar pixels da saída. Conferir a área reservada às legendas no layout; esse comando não copia automaticamente o estilo de legendas animadas da referência.

Medir a duração da narração gerada antes de encaixar a timeline. Adicionar a voz como `<audio id="voz" src="assets/voz.wav" data-start="..." data-duration="...">` conforme o contrato do motor. Não cortar o fim da fala para caber. Para legendas animadas ou layout específico, usar os timestamps JSON na composição; o burn-in SRT é um caminho simples, não reprodução automática de qualquer estilo.

## 6. Uso com CRM e assinatura

`project.json` é a entrada persistente: briefing, referência, canvas, áudio e IDs opcionais de cliente/projeto. Um CRM pode exportar essa estrutura; a skill/CLI local executa o trabalho e retorna arquivos e JSON para registrar no CRM. Não reconstruir o CRM nem criar um servidor novo por consequência de um pedido de vídeo.

Usar a skill no Codex/Claude Code já autenticado pelo método escolhido pelo usuário. O trabalho do agente continua sujeito aos limites do plano. Os scripts não extraem credenciais desses programas e não transformam a assinatura numa chave de API para um backend hospedado. Referências oficiais: [Codex authentication](https://learn.chatgpt.com/docs/auth), [Codex non-interactive](https://learn.chatgpt.com/docs/non-interactive-mode), [Claude Code authentication](https://code.claude.com/docs/en/authentication).
