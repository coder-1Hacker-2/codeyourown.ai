import argparse

from project_builder import ProjectBuilder


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a project from a natural-language prompt or launch the local AI UI.")
    parser.add_argument("--prompt", help="Project description such as 'Create a space game with a score and enemies'.")
    parser.add_argument("--output-dir", default="generated_projects", help="Folder where generated projects are saved.")
    parser.add_argument("--no-llm", action="store_true", help="Skip using the LLM wrapper and just generate the project skeleton.")
    parser.add_argument("--serve", action="store_true", help="Start the browser-based frontend and local LLM chat interface.")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.serve:
        from web_app import app
        app.run(host=args.host, port=args.port, debug=True)
        return 0

    prompt = args.prompt or input("Describe the project you want to build: ").strip()
    if not prompt:
        print("No project description was provided.")
        return 1

    builder = ProjectBuilder(output_dir=args.output_dir)
    project_path = builder.build_from_prompt(prompt)

    print(f"Project created successfully at: {project_path}")
    print("Open the generated HTML files in a browser to view the result.")
    print("You can also edit the files directly to customize the project.")

    if not args.no_llm:
        try:
            from llm_client import LLMClient

            client = LLMClient()
            summary = client.chat([
                {"role": "user", "content": f"Turn this idea into a short project summary: {prompt}"}
            ])
            print(f"\nAI summary: {summary}\n")
        except Exception as exc:
            print(f"LLM not available. Using local template generation instead. ({exc})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
