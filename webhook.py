import http.server
import socketserver
import os
import subprocess
import re
import uuid

PORT = 8080
RANDOM_PATH_FOR_WEBHOOK = os.environ.get('RANDOM_PATH_FOR_WEBHOOK', uuid.uuid4().hex)
class WebhookHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == f'/{RANDOM_PATH_FOR_WEBHOOK}':
            try:
                repo_url = os.environ['REPO_URL']
                repo_name = get_repo_name(repo_url)
                image_name = f"{repo_name}:latest"
                container_name = repo_name

                if os.path.isdir(f'/app/{repo_name}'):
                    subprocess.run(['git', '-C', f'/app/{repo_name}', 'pull'], check=True)
                else:
                    subprocess.run(['git', 'clone', repo_url, f'/app/{repo_name}', '--depth', '1'], check=True)

                subprocess.run(['docker', 'build', '-t', image_name, f'/app/{repo_name}'], check=True)
                new_container_name = f"{container_name}_new"
                subprocess.run(['docker', 'run', '-d', '--name', new_container_name, image_name], check=True)
                subprocess.run(['docker', 'stop', container_name], check=False)
                subprocess.run(['docker', 'rm', container_name], check=False)
                subprocess.run(['docker', 'rename', new_container_name, container_name], check=True)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Deploiement reussi')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Erreur : {str(e)}'.encode())
        else:
            self.send_response(404)
            self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.wfile.write(b'')
        self.end_headers()

def get_repo_name(repo_url):
    match = re.search(r'/([^/]+)\.git$', repo_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Impossible d'extraire le nom du depot")

with socketserver.TCPServer(("", PORT), WebhookHandler) as httpd:
    print(f"Serveur en ecoute sur le port {PORT}", flush=True)
    print(f"Webhook disponible sur http://localhost:{PORT}/{RANDOM_PATH_FOR_WEBHOOK}", flush=True)
    httpd.serve_forever()