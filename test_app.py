from web_app import create_app
from project_builder import ProjectBuilder


def test_health_route():
    app = create_app()
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_assistant_route_is_removed():
    app = create_app()
    client = app.test_client()
    response = client.post('/api/chat', json={'message': 'Create a simple website'})
    assert response.status_code == 404


def test_builder_page_has_no_assistant_ui():
    app = create_app()
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'LLM Assistant' not in response.data
    assert b'chat-input' not in response.data
    assert b'id="editor-toggle"' in response.data
    assert b'id="editor-toggle" class="editor-toggle" type="button" aria-expanded="false" disabled' in response.data


def test_project_preview_route():
    app = create_app()
    client = app.test_client()
    builder = ProjectBuilder(output_dir='generated_projects')
    project = builder.build_from_prompt('Build a fintech dashboard website')
    response = client.get(f'/projects/{project.name}/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert client.get(f'/projects/{project.name}/style.css').status_code == 200
    assert client.get(f'/projects/{project.name}/script.js').status_code == 200


def test_generated_website_does_not_include_raw_prompt():
    prompt = 'Build a wellness website for busy parents who need gentle routines'
    builder = ProjectBuilder(output_dir='generated_projects')
    project = builder.build_from_prompt(prompt)
    html = (project / 'index.html').read_text(encoding='utf-8')

    assert prompt not in html
    assert 'gentle routines' not in html
    assert 'Make room for better habits' in html


def test_code_editor_reads_and_saves_only_project_source_files():
    app = create_app()
    client = app.test_client()
    generated = client.post('/api/generate', json={'prompt': 'Build a small code editor demo website'})
    project_name = generated.get_json()['project_name']

    files_response = client.get(f'/api/projects/{project_name}/files')
    assert files_response.status_code == 200
    assert set(files_response.get_json()['files']) == {'index.html', 'style.css', 'script.js'}

    updated_content = '<!doctype html><title>Edited site</title>'
    save_response = client.post(
        f'/api/projects/{project_name}/files/index.html',
        json={'content': updated_content},
    )
    assert save_response.status_code == 200
    assert client.get(f'/projects/{project_name}/').data.decode('utf-8') == updated_content

    rejected_file = client.post(
        f'/api/projects/{project_name}/files/README.md',
        json={'content': 'not allowed'},
    )
    assert rejected_file.status_code == 400


def test_different_prompts_create_different_templates():
    builder = ProjectBuilder(output_dir='generated_projects')
    first = builder.build_from_prompt('Build a AI startup landing page')
    second = builder.build_from_prompt('Build a wellness coaching website')

    first_html = (first / 'index.html').read_text(encoding='utf-8')
    second_html = (second / 'index.html').read_text(encoding='utf-8')

    assert first_html != second_html
    assert 'AI' in first_html or 'Neural' in first_html
    assert 'coach' in second_html.lower() or 'wellness' in second_html.lower()
