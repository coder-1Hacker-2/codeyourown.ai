import hashlib
import re
from pathlib import Path


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "project"


class ProjectBuilder:
    TEMPLATE_THEMES = {
        "saas": {
            "eyebrow": ["Workflow OS", "Productivity Layer", "Growth Engine", "AI Ops"],
            "stats": ["8x faster launches", "99.9% uptime", "2.4x more conversions"],
            "cta": ["Book a demo", "Start free", "See pricing", "Launch now"],
            "features": [
                ("Smart automation", "Replace repetitive work with one-click systems."),
                ("Team alignment", "Keep product, marketing, and ops in sync."),
                ("Live insights", "Track what matters in real time."),
            ],
        },
        "ai": {
            "eyebrow": ["Neural stack", "Generative engine", "Model layer", "AI workflow"],
            "stats": ["150k automations", "4.8/5 user rating", "Trusted by builders"],
            "cta": ["Try the AI", "Deploy now", "Explore demo", "Build with us"],
            "features": [
                ("Prompt orchestration", "Turn raw ideas into polished product flows."),
                ("Agent workflow", "Let AI handle repetitive execution paths."),
                ("Smart routing", "Send work to the right model, instantly."),
            ],
        },
        "portfolio": {
            "eyebrow": ["Selected work", "Case studies", "Creative studio", "Design portfolio"],
            "stats": ["12+ launches", "Award winning", "Global clients"],
            "cta": ["View work", "Hire me", "Book intro", "See projects"],
            "features": [
                ("Storytelling", "Design systems that explain your value."),
                ("Strategy", "Simple product narratives that convert."),
                ("Delivery", "Launch-ready experiences from concept to deploy."),
            ],
        },
        "health": {
            "eyebrow": ["Better habits", "Daily performance", "Human wellness", "Coach OS"],
            "stats": ["92% retention", "3x more consistency", "14-day reset"],
            "cta": ["Get started", "Try the plan", "Join now", "Start coaching"],
            "features": [
                ("Personal tracking", "See your progress in one view."),
                ("Actionable routines", "Guidance built around your week."),
                ("Community support", "Stay accountable with shared goals."),
            ],
        },
        "education": {
            "eyebrow": ["Learn faster", "Skill engine", "Course platform", "Learning hub"],
            "stats": ["36 lessons", "Expert led", "Track growth"],
            "cta": ["Explore courses", "Enroll now", "Start learning", "See syllabus"],
            "features": [
                ("Structured tracks", "Break complex topics into practical milestones."),
                ("Live feedback", "Get clear action steps and coaching."),
                ("Portfolio building", "Show your growth with evidence-backed work."),
            ],
        },
    }
    COLOR_PALETTES = [
        ("#0b1320", "#d7ffe8", "#34d399", "#10b981"),
        ("#05120c", "#dcffe8", "#4ade80", "#86efac"),
        ("#090d16", "#e2fff0", "#2dd4bf", "#5eead4"),
        ("#0b0f17", "#f0fffb", "#22c55e", "#16a34a"),
        ("#121717", "#f5fff8", "#6ee7b7", "#34d399"),
    ]
    SECTION_VARIATIONS = [
        "split-banner",
        "floating-card",
        "feature-grid",
        "story-panel",
        "testimonial-focus",
    ]

    def __init__(self, output_dir: str = "generated_projects") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def build_from_prompt(self, prompt: str) -> Path:
        project_name = self._to_project_name(prompt)
        project_folder = self.output_dir / project_name
        project_folder.mkdir(exist_ok=True)

        self._write_web_project(project_folder, prompt)
        return project_folder

    def _to_project_name(self, prompt: str) -> str:
        words = re.findall(r"[a-zA-Z0-9]+", prompt)
        name = "-".join(words[:5]).lower()
        return slugify(name) or "my-project"

    def _choose_template_variant(self, prompt: str) -> dict:
        prompt_key = prompt.lower()
        category = "saas"
        for key, config in self.TEMPLATE_THEMES.items():
            if key in prompt_key:
                category = key
                break
        if any(word in prompt_key for word in ["portfolio", "designer", "creative", "art", "brand"]):
            category = "portfolio"
        if any(word in prompt_key for word in ["fitness", "wellness", "health", "coach", "trainer"]):
            category = "health"
        if any(word in prompt_key for word in ["school", "course", "learn", "education", "academy"]):
            category = "education"
        if any(word in prompt_key for word in ["ai", "agent", "chatbot", "ml", "model", "automation"]):
            category = "ai"

        digest = hashlib.md5(prompt.encode("utf-8")).hexdigest()
        palette_index = int(digest[:2], 16) % len(self.COLOR_PALETTES)
        layout_index = int(digest[2:4], 16) % len(self.SECTION_VARIATIONS)
        theme = self.TEMPLATE_THEMES[category]
        stat_index = int(digest[4:6], 16) % len(theme["stats"])
        cta_index = int(digest[6:8], 16) % len(theme["cta"])
        feature_group = theme["features"]

        return {
            "category": category,
            "palette": self.COLOR_PALETTES[palette_index],
            "layout": self.SECTION_VARIATIONS[layout_index],
            "eyebrow": theme["eyebrow"][stat_index % len(theme["eyebrow"])],
            "stat": theme["stats"][stat_index],
            "cta": theme["cta"][cta_index],
            "features": feature_group,
        }

    def _write_web_project(self, folder: Path, prompt: str) -> None:
        variant = self._choose_template_variant(prompt)
        title = self._title_from_prompt(prompt)
        primary_bg, text_color, accent, accent_soft = variant["palette"]
        feature_cards = "\n".join(
            f"<article><h3>{name}</h3><p>{desc}</p></article>" for name, desc in variant["features"]
        )
        layout_main = self._layout_markup(variant["layout"])
        html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{title}</title>
  <link rel=\"stylesheet\" href=\"style.css\" />
</head>
<body>
  <div class=\"page-shell\">
    <header class=\"hero\" style=\"--bg:{primary_bg};--text:{text_color};--accent:{accent};--accent-soft:{accent_soft};\">
      <nav>
        <div class=\"brand\">{title}</div>
        <div class=\"nav-actions\">
          <a href=\"#features\">Features</a>
          <a href=\"#journey\">Why us</a>
          <button>{variant['cta']}</button>
        </div>
      </nav>
      <div class=\"hero-content\">
        <div class=\"hero-copy\">
          <p class=\"eyebrow\">{variant['eyebrow']}</p>
          <h1>{title}</h1>
          <p class=\"lead\">A more thoughtful way to move from idea to action.</p>
          <div class=\"actions\">
            <button class=\"primary\">{variant['cta']}</button>
            <button class=\"secondary\">View demo</button>
          </div>
          <div class=\"mini-stats\">
            <span>{variant['stat']}</span>
          </div>
        </div>
        <div class=\"hero-panel\">
          <div class=\"panel-card large\">{title}</div>
          <div class=\"panel-stack\">
            <div class=\"panel-card\">Live workflow</div>
            <div class=\"panel-card pill\">Fast launch</div>
          </div>
        </div>
      </div>
    </header>

    <main>
      <section id=\"features\" class=\"features\">
        <div class=\"section-heading\">
          <p class=\"eyebrow\">Why teams choose it</p>
          <h2>Built to feel premium and easy to use.</h2>
        </div>
        <div class=\"feature-grid\">
          {feature_cards}
        </div>
      </section>

      <section id=\"journey\" class=\"journey\">
        {layout_main}
      </section>
    </main>
  </div>
  <script src=\"script.js\"></script>
</body>
</html>
"""

        css = f"""* {{ box-sizing: border-box; }}
:root {{
  --bg: {primary_bg};
  --bg-2: #0f172a;
  --text: {text_color};
  --accent: {accent};
  --accent-soft: {accent_soft};
  --panel: rgba(9, 19, 14, 0.8);
  --panel-border: rgba(255,255,255,0.08);
}}

body {{
  margin: 0;
  font-family: Arial, sans-serif;
  background: radial-gradient(circle at top, rgba(16, 185, 129, 0.14), transparent 28%), linear-gradient(135deg, var(--bg), #020b07 45%, #030c08 100%);
  color: var(--text);
}}

.page-shell {{
  min-height: 100vh;
}}

.hero {{
  padding: 22px 7vw 48px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), transparent 30%), var(--bg);
}}

nav {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}}

.brand {{
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: 0.06rem;
}}

.nav-actions {{
  display: flex;
  gap: 20px;
  align-items: center;
}}

.nav-actions a {{
  color: var(--text);
  text-decoration: none;
  opacity: 0.8;
}}

button {{
  border: none;
  border-radius: 999px;
  padding: 12px 18px;
  font-weight: 700;
  background: var(--accent);
  color: #031b12;
  cursor: pointer;
}}

.secondary {{
  background: transparent;
  color: var(--text);
  border: 1px solid rgba(255,255,255,0.2);
}}

.hero-content {{
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  align-items: center;
  gap: 24px;
}}

.eyebrow {{
  text-transform: uppercase;
  letter-spacing: 0.16rem;
  font-size: 0.76rem;
  color: var(--accent-soft);
}}

.hero-copy h1 {{
  margin: 10px 0 14px;
  font-size: clamp(2.2rem, 5vw, 4rem);
}}

.lead {{
  max-width: 620px;
  color: rgba(255,255,255,0.78);
  font-size: 1.08rem;
}}

.actions {{
  display: flex;
  gap: 14px;
  margin-top: 26px;
  flex-wrap: wrap;
}}

.mini-stats {{
  margin-top: 18px;
  display: inline-flex;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
}}

.hero-panel {{
  display: grid;
  gap: 18px;
}}

.panel-card {{
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--panel-border);
  border-radius: 18px;
  padding: 22px;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 700;
}}

.panel-card.large {{
  min-height: 200px;
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.18), rgba(15, 23, 42, 0.6));
}}

.panel-stack {{
  display: flex;
  gap: 18px;
}}

.panel-card.pill {{
  min-height: unset;
  flex: 1;
}}

section {{
  padding: 52px 7vw;
}}

.section-heading {{
  margin-bottom: 32px;
}}

.section-heading h2 {{
  font-size: clamp(1.8rem, 4vw, 3rem);
  margin: 10px 0 0;
}}

.feature-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}}

.feature-grid article {{
  background: rgba(7, 21, 12, 0.75);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 16px 36px rgba(10, 21, 14, 0.2);
}}

.feature-grid h3 {{
  margin-top: 0;
}}

.journey {{
  padding-top: 8px;
}}

.split-banner {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 26px;
  align-items: center;
}}

.split-banner .copy-block, .split-banner .visual-block {{
  background: rgba(7, 21, 12, 0.78);
  border-radius: 20px;
  padding: 28px;
  border: 1px solid rgba(255,255,255,0.07);
}}

.visual-block {{
  min-height: 220px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, rgba(52, 211, 153, 0.12), rgba(15, 23, 42, 0.7));
}}

@media (max-width: 760px) {{
  .hero-content, .split-banner {{
    grid-template-columns: 1fr;
  }}

  .nav-actions {{
    display: none;
  }}
}}
"""

        js = """document.querySelector('button')?.addEventListener('click', () => {
  window.scrollTo({ top: document.body.scrollHeight * 0.2, behavior: 'smooth' });
});
"""

        (folder / "index.html").write_text(html, encoding="utf-8")
        (folder / "style.css").write_text(css, encoding="utf-8")
        (folder / "script.js").write_text(js, encoding="utf-8")
        (folder / "README.md").write_text(
          f"# {title}\n\nA generated website project. Open index.html to preview it.\n",
          encoding="utf-8",
        )

    def _layout_markup(self, layout: str) -> str:
        if layout == "split-banner":
            return """<div class=\"split-banner\">\n  <div class=\"copy-block\">\n    <p class=\"eyebrow\">Built for clarity</p>\n    <h2>Beautiful, intuitive experience for real users.</h2>\n    <p>Thoughtful layouts, clear actions, and smooth messaging help users understand your product in seconds.</p>\n  </div>\n  <div class=\"visual-block\">\n    <div class=\"panel-card large\">UI map</div>\n  </div>\n</div>"""
        if layout == "floating-card":
            return """<div class=\"split-banner\">\n  <div class=\"visual-block\">\n    <div class=\"panel-card large\">Conversion deck</div>\n  </div>\n  <div class=\"copy-block\">\n    <p class=\"eyebrow\">Highly usable</p>\n    <h2>Clean layouts preserve momentum.</h2>\n    <p>Each section feels intentional, so visitors can read, trust, and act without friction.</p>\n  </div>\n</div>"""
        if layout == "feature-grid":
            return """<div class=\"copy-block\">\n  <p class=\"eyebrow\">Aesthetic by design</p>\n  <h2>Everything is organized and easy to scan.</h2>\n  <p>The content hierarchy is carefully balanced so it feels premium while remaining effortless to navigate.</p>\n</div>"""
        if layout == "story-panel":
            return """<div class=\"split-banner\">\n  <div class=\"copy-block\">\n    <p class=\"eyebrow\">Built for trust</p>\n    <h2>People know what to do next.</h2>\n    <p>Clear messaging, less noise, and strong positioning help users move from interest to action.</p>\n  </div>\n  <div class=\"visual-block\">\n    <div class=\"panel-card large\">Storyflow</div>\n  </div>\n</div>"""
        return """<div class=\"split-banner\">\n  <div class=\"copy-block\">\n    <p class=\"eyebrow\">Launch-ready</p>\n    <h2>Polished enough to impress, simple enough to trust.</h2>\n    <p>Every section supports a clear product story and helps users stay engaged without confusion.</p>\n  </div>\n  <div class=\"visual-block\">\n    <div class=\"panel-card large\">Product focus</div>\n  </div>\n</div>"""

    def _title_from_prompt(self, prompt: str) -> str:
      titles = {
        "saas": "A clearer way to work",
        "ai": "Intelligence, made useful",
        "portfolio": "Work worth remembering",
        "health": "Make room for better habits",
        "education": "Learn what moves you forward",
      }
      return titles[self._choose_template_variant(prompt)["category"]]
