# MilWeb Video Studio

**English** | [Português](README.pt-BR.md)

> **Type:** internal tool published as an open project — a skill (Markdown instructions + one Python media-audit script) for Claude Code. There is no web application or demo, so there is no presentation image.

A Portuguese-language skill that helps choose the social network, runs a progressive briefing and creates content: posts, Pins, carousels or videos with research, direction, script, scene generation, editing, audio and review. Built for **Claude Code** and other agents compatible with the `SKILL.md` format.

> The skill instructions, prompts and agent definitions are written in Portuguese (pt-BR). This README is an English summary; the [Portuguese README](README.pt-BR.md) is the reference text.

It works for a portfolio Reel, a long tutorial, a Higgsfield scene or a one-off edit fix. The core is editor-agnostic; the modules guide the choice of whichever tool is available.

## What it does

- Asks for the network when it was not given and asks specific questions gradually, without repeating answered ones.
- Investigates intent, style, reference, pacing, audio and how to show the website before scripting or editing.
- Separates vertical video from mobile capture and respects framing, caption and text choices, with no automatic per-network additions.
- Diagnoses what the user disliked and what to keep before redoing a video.
- Coordinates five specialists: Pinterest, TikTok, Instagram, LinkedIn and YouTube Shorts, with a shared briefing and their own proposals.
- Treats long videos as independent projects, with their own research, script and timeline.
- Studies references by segment and compares samples on concrete criteria, without promising to beat an unverified video.
- Researches current references and distinguishes observed trends from original ideas.
- Prioritizes ideas and builds calendars according to audience, materials, time and budget.
- Analyzes metrics without confusing average watch time with retention or attributing causes without evidence.
- Adapts language for Instagram, TikTok, LinkedIn, Pinterest, YouTube, Bilibili and other networks.
- Plans script, shot list, pacing, transitions and real website capture.
- Prepares Higgsfield generation with references, continuity, budget and attempt limits.
- Plans presenter cut-outs, layered virtual sets, 3D animation and websites being assembled on screen.
- Defines a short proof of the riskiest effect before rendering a full complex production.
- Guides editing with Remotion, FFmpeg, Higgsedit or the project's editor.
- Handles voice, music, SFX, captions and audiovisual review.
- Preserves duration and briefing choices, including long contemplative scenes.

**The skill does not install an editor, does not provide credits and does not create an automatic connection to Higgsfield.** The agent needs the corresponding tools. Without them, it can still research, direct, script and prepare prompts.

## Install in Claude Code

With Node.js/npm, use the skills installer:

```bash
npx skills add rickjs2005/milweb-video-studio --skill milweb-video-studio -a claude-code -g
```

Review the options shown. `-g` installs for use across your projects; without it, the install is local to the project. Check that Claude recognizes `/milweb-video-studio`. The installer is an external tool; see its [documentation](https://github.com/vercel-labs/skills).

### Manual alternative on Windows / PowerShell

In the folder where you keep your repositories:

```powershell
git clone https://github.com/rickjs2005/milweb-video-studio.git
if ($LASTEXITCODE -ne 0) { throw 'Falha ao clonar o repositorio.' }
$skillTarget = Join-Path $env:USERPROFILE '.claude\skills\milweb-video-studio'
if (Test-Path $skillTarget) { throw 'A skill ja existe. Compare as versoes antes de atualizar.' }
New-Item -ItemType Directory -Force (Split-Path $skillTarget) | Out-Null
Copy-Item -Recurse '.\milweb-video-studio\skills\milweb-video-studio' $skillTarget
```

### Manual alternative on macOS / Linux

```bash
git clone https://github.com/rickjs2005/milweb-video-studio.git
mkdir -p ~/.claude/skills
if [ ! -e ~/.claude/skills/milweb-video-studio ]; then
  cp -R milweb-video-studio/skills/milweb-video-studio ~/.claude/skills/
else
  echo 'A skill já existe. Compare as versões antes de atualizar.'
fi
```

For a single project, place the skill folder at `.claude/skills/milweb-video-studio/` inside it. Do not copy the whole repository root into the skills folder. Open a new session if it does not show up yet. See the format in the [Claude Code documentation](https://code.claude.com/docs/en/skills).

If you already use `milweb-video` or `edicao-video-capcut`, keep the old files while you compare versions. Invoke this skill by name to test it; there is no need to delete other skills.

## Network choice and progressive questions

Start with `/milweb-video-studio Quero criar conteúdo de um site meu.` ("I want to create content about a website of mine.")

Without a defined network, the skill asks which network to create for: LinkedIn, Pinterest, Instagram, TikTok or YouTube Shorts. Choosing the network is only the start. For video, it investigates goal, audience, visual style, references, pacing, website presentation, audio and materials, one question at a time or two related ones. Questions adapt to what is actually missing; a complete briefing or delegated choices let it move on directly. It does not ask again for anything already provided. Other destinations, such as YouTube and websites, remain available.

| Network | Initial positioning for MilWeb | Possible deliverables |
|---|---|---|
| LinkedIn | Authority and professional connections | Case, lesson, post, document/carousel or video |
| Pinterest | Visual portfolio and refined aesthetics | Pin, screen composition, visual series or video |
| Instagram | Trust, projects and business contact | Reel, carousel, Stories and caption |
| TikTok | Personality, humor, behind the scenes and experiments | Idea, script and audience-adapted video |
| YouTube Shorts | Discovery and short demonstration | Short with one complete idea |

These are brand directions, not performance guarantees. Research fits each destination: trends and formats on Instagram/TikTok, discussions and cases on LinkedIn, searches and visual references on Pinterest. Lack of access or evidence must be stated.

The five specialties share the skill. Long-form YouTube follows an independent project. Static content does not require video production; planning requests do not authorize publishing or paid generation.

## Per-network agents in Claude Code

The definitions are in [.claude/agents](.claude/agents). There are five agents: `milweb-pinterest`, `milweb-tiktok`, `milweb-instagram`, `milweb-linkedin` and `milweb-youtube-shorts`. The main skill coordinates the briefing, deliverables and review. It triggers only the requested channels, shares materials and avoids duplicated recordings/spending.

Install the skill first. The agent files must be in `.claude/agents/` of the project where you use Claude Code, or in `~/.claude/agents/` for all projects. The skill install command above does not install these agents automatically. When using Claude Code at the root of this cloned repository, the files are already in the project location; in another project, copy the five files to the matching folder, preserving existing files.

On Windows, after cloning the repository and opening PowerShell at its root, the global copy can be done like this:

```powershell
$milwebAgentSource = Join-Path (Get-Location) '.claude\agents'
$milwebAgentTarget = Join-Path $env:USERPROFILE '.claude\agents'
$milwebAgentFiles = Get-ChildItem $milwebAgentSource -Filter 'milweb-*.md'
if ($milwebAgentFiles.Count -ne 5) { throw 'Esperados cinco agentes. Confira a pasta do repositorio.' }
foreach ($milwebAgentFile in $milwebAgentFiles) {
  if (Test-Path (Join-Path $milwebAgentTarget $milwebAgentFile.Name)) {
    throw 'Ja existe um agente com esse nome. Compare os arquivos antes de atualizar.'
  }
}
New-Item -ItemType Directory -Force $milwebAgentTarget | Out-Null
$milwebAgentFiles | Copy-Item -Destination $milwebAgentTarget
```

These instructions follow the [official subagents documentation](https://code.claude.com/docs/en/sub-agents). They do not set a fixed model, expanded permissions or automatic publishing. The skill remains usable without subagents, applying the profiles sequentially and stating that mode. Installation and execution on the user's computer still need to be verified.

## First test, without spending credits

In Claude Code (the prompt is in Portuguese, like the skill):

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

It asks for a 30–45 s plan for TikTok and Instagram Reels, with topic, audience and available materials, verified references, opening, scene-by-scene script, cuts, captions, audio and per-network adaptations — plan only, no media generation or paid services. Replace the bracketed fields with your context. The skill should separate verified references from hypotheses, propose a timeline and respect the available materials. If it cannot research a network, it should state the limitation. The test does not authorize paid generation; agent usage remains subject to your plan. See more [usage prompts](examples/prompts.md) and the [evaluation criteria](docs/validation.md) (both in Portuguese).

For real work, provide URL or files, goal, audience, destination, duration and budget when paid generation is involved. Do not put tokens or passwords in the prompt.

## Modules

| File | Role |
|---|---|
| [SKILL.md](skills/milweb-video-studio/SKILL.md) | Scope, flow, module selection and core criteria |
| `social-networks.md` | Network choice, progressive questions and five social specialties |
| `creative-brief.md` | Creative direction before editing and dissatisfaction diagnosis |
| `channel-agents.md` | Shared briefing, five specialists and execution coordination |
| `reference-study.md` | Segment analysis, effects plan and quality comparison |
| `long-form.md` | Long episodes as independent projects |
| `research.md` | Research and evidence quality |
| `content-strategy.md` | Priorities, formats and editorial calendar |
| `performance.md` | Metrics, hypotheses and content tests |
| `platforms.md` | Per-destination language and versions |
| `direction.md` | Script, pacing and transitions |
| `footage.md` | Real capture and media inventory |
| `higgsfield.md` | Generation, continuity and budget |
| `compositing-vfx.md` | Cut-out, layers, virtual sets, 3D, website building and short proof |
| `editing.md` | Editing, motion and engines |
| `audio.md` | Voice, music, effects and captions |
| `quality.md` | Technical, perceptual and editorial review |
| `templates.md` | Briefing, shot list, sources and QA |
| `sources.md` | Documentation and reference projects |

The modules live in `skills/milweb-video-studio/references/` and are loaded as the task requires. There is no automatic dependency installation and no hooks.

## Optional technical check

The only included script reads metadata and can decode a local video. It requires **Python 3.10+**, **ffprobe** and, for `--decode`, **ffmpeg** on PATH.

```bash
python skills/milweb-video-studio/scripts/media_audit.py final.mp4 --min-duration 25 --require-audio --decode
```

The JSON result is not aesthetic approval: it does not confirm that the savanna lasted 25 seconds, that the sound is good or that the transition works. It measures the overall duration and checks the requested technical conditions. It does not modify the media and does not use the network.

To run the local tests, with the same requirements:

```bash
python -m unittest discover -s tests -v
```

## Scope of this version

Version **0.6.0** adds five per-channel agent definitions, coordination with a shared briefing, YouTube Shorts, an independent flow for long videos and reference study with sample comparison. It keeps the desktop/mobile, framing and caption rules, and the advanced compositing flow for cut-outs, virtual sets, 2.5D/3D animation and websites assembled in layers, with a short proof, review criteria and render planning on limited machines. It keeps per-network briefing, posts, Pins, carousels and video production. These are procedures and execution criteria; no segmentation model or ready-made 3D scene is included. The modules are editorial instructions, not an autonomous video engine. The paid Higgsfield integration and execution inside Claude Code need to be tested in the user's environment. There is no promise of going viral, a "perfect transition" or an automatic cinematic result.

The content is original and uses public projects as study references, without bundling their files. See [sources](skills/milweb-video-studio/references/sources.md) and [third-party licenses](THIRD_PARTY.md).

## Contributing

Open an issue with an anonymized briefing, observed behavior, desired result and tool versions. To propose a rule, explain its context and exceptions. Do not send private videos, credentials or client content without authorization. See [CONTRIBUTING.md](CONTRIBUTING.md).

The script tests run on GitHub Actions ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) with Python 3.13 and FFmpeg.

## Security

Do not open public issues for security problems. See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE) license for the files in this repository. Services, tools, models and media used with the skill have their own terms. Independent MilWeb project; not an official product of Anthropic, OpenAI, Remotion or Higgsfield.
