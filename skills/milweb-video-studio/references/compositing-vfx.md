# Composição, cenários virtuais e animação de sites

## Decompor a referência antes de escolher a ferramenta

Separar o resultado visível do processo presumido. Um vídeo final não comprova software, modelo, tempo gasto, edição ao vivo ou ausência de intervenção humana. Registrar em cada trecho: intervalo, acesso visual/sonoro, efeito observado, hipótese técnica, materiais necessários e risco. Frames permitem descrever composição e mudanças amostradas; não comprovam fluidez ou sincronia musical.

Para referência fornecida, analisar primeiro o arquivo autorizado; não exigir busca de trends para um diagnóstico técnico pontual. Se houver desenvolvimento de conceito novo, seguir research.md. Não instalar ferramentas apenas para imitar uma alegação de “100% IA”.

## Escolher a menor complexidade que atende à intenção

| Objetivo | Caminho inicial | Quando aumentar a complexidade |
|---|---|---|
| Texto, fotos, cards e telas em movimento | Camadas 2D com timing controlado | Movimento relativo em profundidade justificar 2.5D |
| Câmera percorrendo fotos/mapas | Planos em profundidades distintas e câmera moderada | Necessidade real de volume, luz ou oclusão |
| Objeto girando ou com interior exposto | Geometria 3D ou vistas ilustradas claramente identificadas | Usar 3D para mudanças de perspectiva e cortes consistentes |
| Pessoa diante de novo cenário | Gravação + máscara temporal + fundo | Refinar máscara/rotoscopia quando bordas falharem |
| Cenário sendo construído | Estrutura, superfícies, objetos e luz em etapas | 3D quando parallax, sombras e câmera exigirem |
| Site sendo montado | Elementos reais em camadas + captura final | 3D só para composição espacial útil; preservar UI |

Usar Remotion para composição por código quando disponível, com @remotion/three/Three.js para 3D compatível; Blender pode produzir planos 3D que entram como mídia na montagem. Usar FFmpeg para processamento e composição adequados ao build. Seguir o editor existente quando ele resolver a tarefa. Não instalar todos os motores nem prometer projeto nativo CapCut sem acesso/export válido. Conferir API e versão antes de implementar.

## Recorte de pessoa e troca de fundo

1. Inspecionar movimento de câmera, cabelo, dedos, óculos, microfone/cabos, blur, contraste e objetos que cruzam o corpo. Usar gravação original; material comprimido ou já montado pode limitar a máscara.
2. Selecionar método conforme fonte e ferramentas: chroma key para fundo adequado; segmentação temporal para fundo comum; máscaras/rotoscopia para correções. Não chamar um filtro FFmpeg de recorte por IA sem modelo real. Máscaras de objetos de uma cena 3D não extraem automaticamente uma pessoa de vídeo comum.
3. Produzir máscara alinhada quadro a quadro ou intermediário com transparência suportada. Validar FPS, resolução, duração, offsets, convenção de alpha e bordas; não assumir que MP4 comum preserva transparência.
4. Compor fundo → elementos atrás → pessoa/objetos preservados → elementos à frente → textos. Separar máscaras adicionais se mãos precisarem cruzar elementos virtuais. Definir oclusão deliberadamente.
5. Ajustar escala, horizonte, perspectiva, cor, direção de luz, nitidez e granulação. Não alterar rosto ou identidade para esconder falhas. Sombras de contato só quando fizerem sentido espacial.
6. Conferir bordas sobre fundo claro e escuro e reproduzir trechos com movimento rápido. Corrigir cintilação, halos, partes amputadas e vazamento do fundo antes de aumentar a duração.
7. Se o recorte não for viável, propor composição com a gravação em janela, enquadramento alternativo ou nova captura. Não apresentar substituição como equivalente aprovado sem explicar a mudança.

## Cenário construído em etapas

Planejar estado inicial e final, câmera e profundidades. Fazer uma sequência coerente: base/grid → estrutura → superfícies → objetos → iluminação. Tratar a ordem como receita adaptável, não efeito obrigatório.

Manter pessoa e câmera estáveis quando a intenção for transformar só o ambiente. Evitar mudanças de perspectiva entre estados. Se usar imagens geradas, conferir alinhamento antes de animar: imagens distintas não garantem continuidade. Não inventar objetos ocultos a partir de uma captura como se fossem recuperados do original.

Manter entradas legíveis e um foco por momento. Animar construção, posição ou máscaras conforme a geometria; um fade isolado pode ser suficiente se coerente, mas não prova montagem volumétrica.

## Objetos 3D, cortes e diagramas

Definir se o objeto é ilustrativo, técnico ou fiel a produto real. Usar geometrias, texturas e modelos com origem conhecida. Para interiores/camadas, modelar ou usar assets apropriados; não inferir estrutura factual de aparência externa. Verificar nomes, proporções e afirmações científicas quando houver finalidade educativa.

Fixar câmera, pivôs, escala, luzes e ordem de entrada. Para Remotion, controlar animação pelo frame e tempo local da composição, com aleatoriedade determinística. Não depender de relógio real ou avanço acumulativo que mude ao buscar outro frame. Testar frames fora de ordem para verificar consistência quando houver simulação/animação 3D.

Conferir legibilidade de rótulos, oclusão pela pessoa, colisões e transparências. Preferir um render intermediário reutilizável quando simplificar a montagem sem prejudicar o resultado.

## Site montado em camadas

1. Inspecionar o site real ou fontes fornecidas. Definir viewport e frame final antes dos efeitos.
2. Inventariar fundo, imagem, tipografia, navegação, cards, botões e elementos mobile. Se só houver screenshot, identificar recortes/reconstruções aproximadas; não alegar extração de camadas originais.
3. Quando houver código autorizado, preparar a captura em cópia local isolada; não alterar produção, publicar nem modificar o repositório do site por consequência da edição.
4. Organizar progressão visual: estrutura de layout → mídia → tipografia → componentes → interação. Adaptar ao projeto; não afirmar que essa é a ordem real de desenvolvimento.
5. Alinhar o estado final à captura original e transicionar para gravação do site funcionando. Uma reconstrução animada não comprova responsividade, navegação ou funcionalidades.
6. Conferir fontes, cores, proporções, texto real e carregamento. Manter desktop reconhecível em 9:16; não recortar partes importantes só para preencher o quadro.
7. Produzir versão sem apresentador quando desejado. Não adicionar narração, legendas, CTA ou música que o usuário excluiu.

## Prova curta e orçamento de render

Quando edição/produção complexa estiver autorizada, construir primeiro uma amostra do efeito de maior risco, por exemplo 5–15 s; respeitar duração específica do usuário. A amostra deve conter o recorte, movimento ou transição realmente difícil, não apenas uma abertura fácil.

Conferir CPU/GPU/RAM disponíveis sem assumir aceleração. Começar com preview reduzido, concorrência conservadora e assets leves. Medir tempo e pico de memória quando possível; rotular projeções de custo/tempo como estimativas. Em máquina limitada, usar proxies, pré-render de camadas e render segmentado determinístico com fronteiras verificadas. Não usar 4K/60 fps por padrão.

Antes de escalar: verificar alinhamento temporal, bordas, oclusão, texto, continuidade e áudio quando aplicável. Renderizar um pequeno recorte em resolução final para validar bordas finas. Se houver falha, corrigir a causa e repetir o trecho afetado; evitar tentativas infinitas e respeitar orçamento.

Se a amostra passar e a produção completa já estiver autorizada, continuar sem pedir confirmação extra. Se só o teste tiver sido solicitado, entregar o teste. Sem reprodução/escuta, registrar limites e entregar para revisão, sem alegar aprovação perceptiva completa.

## Registro mínimo por efeito

| Trecho | Observação / hipótese | Camadas e fontes | Ferramenta/versão | Máscara/oclusão | Movimento e timing | Risco e teste | Resultado |
|---|---|---|---|---|---|---|---|

Manter código/timeline, assets autorizados, offsets e parâmetros do efeito no projeto. Não incluir gravação do criador de referência ou arquivos privados em distribuição pública da skill.

## Fontes técnicas

Consultar versões correspondentes ao projeto; estas referências sustentam possibilidades técnicas, não identificam o processo usado em um vídeo de terceiros.

- Remotion, animação por frame: https://www.remotion.dev/docs/the-fundamentals
- Remotion, 3D: https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/remotion-markup/3d.md
- Blender, máscaras de render 3D: https://docs.blender.org/manual/en/4.2/compositing/types/mask/cryptomatte.html
