# Presenter 🎦

Introducing **Presenter**: The State-of-the-Art Multi-Agent AI Tool that can:

- [x] **Create beautiful presentations** for any given topic
- [x] **Render intuitive & visually appealing diagrams** for slides when needed (using Mermaid)
- [x] **Write scripts** for every slide 📜
- [x] **Render & View interactive presentations in HTML** 💻 (using markdown-slides & reveal.js)
- [x] **Intuitive speaker view with scripts** (reveal.js)
- [x] **Export presentations to PDF** 🖨️ (using DeckTape)
- [x] **Generate audio narrations** from speech 🎙️ (using ElevenLabs)
- [x] **Render full video presentations** 🎥 with all the slides and voiceover (using FFmpeg)

## Video Overview of the multi-agent setup

[![]()]()

## Tools Used

- [LlamaIndex](https://www.llamaindex.ai/) Workflows to orchestrate the entire multi-agent setup
- [markdown-slides](https://github.com/dadoomer/markdown-slides) and reveal.js for rendering & viewing the presentation
- [Mermaid](https://github.com/mermaid-js/mermaid) to render the diagrams
- [DeckTape](https://github.com/astefanutti/decktape) to export the presentation to PDF
- [ElevenLabs](https://elevenlabs.io/) API to create audio narration for the slides
- [FFmpeg](https://www.ffmpeg.org/) to render the full presentation with voiceover

## How to use

- Clone the repo

```bash

```

- Install dependencies

```bash
pip install -r requirements.txt
```

- Create `.env` file and add `OPENAI_API_KEY` and `TAVILY_API_KEY`

```bash
cp .env.example .env
```

- Run the workflow with the topic to research

```bash
python run.py ""
```
