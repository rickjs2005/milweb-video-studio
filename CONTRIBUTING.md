# Contributing

[Português](#português)

Thanks for your interest! This is a personal portfolio project maintained by [@rickjs2005](https://github.com/rickjs2005); suggestions and fixes are welcome.

1. Fork the repository and create a branch from the default branch.
2. Install and run locally:
   ```bash
   # no packages to install; requires Python 3.10+ and FFmpeg (ffprobe/ffmpeg) on PATH
   python skills/milweb-video-studio/scripts/media_audit.py --help
   ```
3. Before opening a pull request, run:
   - `python -m unittest discover -s tests -v`
4. Keep changes focused, describe what changed and why, and add screenshots for visual changes.
5. Never commit `.env` files, real customer data or credentials. Use the placeholders in `.env.example` (when present) and synthetic data in tests.

---

## Português

Obrigado pelo interesse! Este é um projeto de portfólio mantido por [@rickjs2005](https://github.com/rickjs2005); sugestões e correções são bem-vindas.

1. Faça um fork e crie uma branch a partir da branch padrão.
2. Instale e rode localmente:
   ```bash
   # no packages to install; requires Python 3.10+ and FFmpeg (ffprobe/ffmpeg) on PATH
   python skills/milweb-video-studio/scripts/media_audit.py --help
   ```
3. Antes de abrir um pull request, rode:
   - `python -m unittest discover -s tests -v`
4. Mantenha as mudanças focadas, descreva o que mudou e por quê, e inclua capturas de tela em mudanças visuais.
5. Nunca versione arquivos `.env`, dados reais de clientes ou credenciais. Use os placeholders do `.env.example` (quando existir) e dados sintéticos nos testes.
