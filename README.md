# Website Studio

Website Studio turns a plain-language description into a polished, editable starter website.

It can:

- choose a design direction based on the website's purpose
- generate a responsive website with category-focused content
- preview the generated website in your browser
- create editable HTML, CSS, and JavaScript files

Describe who the site is for, what it should help them do, and the visual style you prefer. The description guides the design but is not printed into the generated website.

## Quick start

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the app:

   ```bash
   python app.py
   ```

## Example prompts

- Create a welcoming website for a neighborhood bakery.
- Design a portfolio site for a landscape photographer.
- Build a simple landing page for a wellness coaching service.
- Make a course website for beginner gardeners.
- Create a product website for a team task manager.

## Generated project structure

The builder creates a folder like this:

```text
generated_projects/
   neighborhood-bakery/
    index.html
    style.css
    script.js
    README.md
```

## Notes

Generated projects are saved locally in `generated_projects/` and can be edited with any code editor.
