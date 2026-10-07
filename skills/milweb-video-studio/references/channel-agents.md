# Coordenação dos agentes por canal

## Entrada e divisão

A skill principal coordena. Um site ou projeto fornece a matéria-prima comum, mas cada canal recebe uma proposta própria. Acionar apenas os canais pedidos; “Instagram” não dispara cinco agentes. Quando o usuário pedir um pacote sem selecionar canais, esclarecer os destinos em uma rodada curta.

| Agente | Direção inicial MilWeb | Entrega conforme briefing |
|---|---|---|
| milweb-pinterest | Design e portfólio visual | Imagem conceitual/editorial, mockup com UI real ou série de Pins |
| milweb-tiktok | Personalidade, humor dev, bastidores e trends pertinentes | Premissa e montagem próprias, com site reconhecível |
| milweb-instagram | Apresentação de projetos, confiança e interesse comercial | Reel, carrossel ou Stories com direção combinada |
| milweb-linkedin | Raciocínio, problema resolvido e autoridade profissional | Case/post/documento ou vídeo com evidência real |
| milweb-youtube-shorts | Descoberta, resultado ou aprendizado breve | Short autônomo, compreensível sem outros posts |

Essas direções são pontos de partida, não restrições fixas. O briefing e as preferências do usuário prevalecem. Vídeos longos ficam fora deste pacote: usar long-form.md, sem distribuir o episódio entre estes cinco agentes.

## Briefing comum e delegação

1. Coordenador reúne projeto, público, objetivo, URLs/arquivos, identidade, fatos verificados, materiais que podem ser usados e decisões já respondidas. Resolve lacunas comuns uma vez.
2. Registra por canal formato, intenção, estilo, duração quando aplicável, desktop/mobile, enquadramento, áudio, legendas e texto. Campo desconhecido é pendente, não decisão delegada.
3. Encaminha ao especialista: pedido exato, briefing comum, decisões específicas, referências/evidências disponíveis, escopo (pesquisa/plano/produção), ferramentas reais, pasta de saída exclusiva e limites de custo/tempo. Não assumir que o subagente vê a conversa.
4. Especialistas devolvem dúvidas ao coordenador, que agrupa repetições e pergunta uma ou duas relacionadas por rodada. Eles não inventam respostas para evitar perguntar.
5. Pesquisa e planejamento independentes podem ocorrer em paralelo. Capturas compartilhadas, edição no mesmo projeto/browser e render pesado têm um responsável por vez. Não duplicar gravações ou gastar o mesmo orçamento em vários agentes.
6. Coordenador integra as propostas e executa apenas a fase autorizada. Distribui produção por canal quando houver ferramentas, briefing e materiais suficientes. Nenhum agente publica nem gasta fora da autorização recebida.

## Contrato de retorno

Cada especialista devolve: intenção da peça; proposta própria; evidência consultada e nível de acesso; perguntas ainda necessárias; materiais reutilizados e faltantes; plano executável ou arquivos reais conforme escopo; verificações feitas e pendentes. Diferenciar texto da publicação de texto queimado na imagem/vídeo.

Coordenador verifica que não houve inclusão automática de mobile, legendas, CTA, narrador ou música; que o conteúdo real não foi inventado; e que as peças têm diferenças de narrativa/composição justificadas. Resolver conflitos com o briefing antes de entregar.

## Execução real e instalação

Há cinco definições nativas no repositório em .claude/agents/milweb-*.md. No Claude Code, elas dependem de milweb-video-studio instalada; os arquivos de agentes precisam estar em .claude/agents do projeto ou em ~/.claude/agents. Instalar só a skill não instala automaticamente esses arquivos. Não afirmar que agentes foram ativados no computador do usuário sem verificar.

Em ambientes com delegação, usar o agente nomeado disponível ou criar um subagente com o contrato e as instruções do canal. Não criar recursivamente equipes: os especialistas retornam ao coordenador. Sem delegação real, aplicar os perfis sequencialmente e informar isso, sem inventar agentes em execução.

Não fixar modelo, esforço ou mecanismo de aprovação nos perfis; herdar o ambiente e respeitar seus limites.
