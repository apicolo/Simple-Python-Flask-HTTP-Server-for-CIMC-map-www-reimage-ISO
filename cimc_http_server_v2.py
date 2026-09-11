import os
from flask import Flask, send_from_directory, request, Response, render_template_string

app = Flask(__name__)
SHARE_DIR = os.path.abspath("./iso_share")

# Modelo de página HTML simples para listar os arquivos no navegador
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CIMC ISO Share Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }
        h2 { color: #005c8a; border-bottom: 2px solid #005c8a; padding-bottom: 10px; }
        ul { list-style-type: none; padding: 0; }
        li { background: white; margin: 10px 0; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }
        a { color: #007aa3; text-decoration: none; font-weight: bold; font-size: 16px; }
        a:hover { text-decoration: underline; }
        .size { color: #666; font-size: 14px; }
        .empty { color: #888; font-style: italic; }
    </style>
</head>
<body>
    <h2>📁 Arquivos Disponíveis para o Cisco CIMC (map-www)</h2>
    {% if files %}
        <ul>
        {% for file in files %}
            <li>
                <a href="/{{ file.name }}">{{ file.name }}</a>
                <span class="size">{{ file.size }} GB</span>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p class="empty">Nenhum arquivo encontrado na pasta 'iso_share'. Coloque suas ISOs lá dentro!</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def list_files():
    """Lista todos os arquivos dentro da pasta iso_share quando acessar a raiz '/'"""
    files_list = []
    if os.path.exists(SHARE_DIR):
        for filename in os.listdir(SHARE_DIR):
            file_path = os.path.join(SHARE_DIR, filename)
            if os.path.isfile(file_path):
                size_gb = round(os.path.getsize(file_path) / (1024**3), 2)
                files_list.append({'name': filename, 'size': size_gb})
    
    return render_template_string(HTML_TEMPLATE, files=files_list)

@app.route('/<path:filename>', methods=['GET', 'HEAD'])
def serve_iso(filename):
    file_path = os.path.join(SHARE_DIR, filename)
    
    # 1. Trata arquivo inexistente
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print(f"[ERRO] Arquivo solicitado nao existe: {filename}")
        return "Arquivo Nao Encontrado", 404

    file_size = os.path.getsize(file_path)

    # 2. Trata a requisição HEAD do CIMC (Checagem de tamanho e disponibilidade)
    if request.method == 'HEAD':
        print(f"[INFO] CIMC enviou checagem HEAD para: {filename}")
        response = Response(status=200)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Length'] = file_size
        response.headers['Accept-Ranges'] = 'bytes'
        return response

    # 3. Trata a requisição GET do CIMC / Navegador (Download/Streaming da ISO)
    print(f"[INFO] Iniciou o streaming de: {filename} ({file_size / (1024**3):.2f} GB)")
    return send_from_directory(SHARE_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(SHARE_DIR):
        os.makedirs(SHARE_DIR)
        print(f"[INIT] Pasta '{SHARE_DIR}' criada. Coloque suas ISOs dentro dela.")

    print("[STATUS] Iniciando servidor HTTP na porta 80...")
    app.run(host='0.0.0.0', port=80, debug=False)
