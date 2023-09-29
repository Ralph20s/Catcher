import os

# Obtém o diretório da área de trabalho do usuário
desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
# Define o caminho para a pasta 'Documentos' do usuário
documents_path = os.path.join(os.path.expanduser("~"), 'Documents')
downloads_path = os.path.join(os.path.expanduser("~"), 'Downloads')
pictures_path = os.path.join(os.path.expanduser("~"), 'Pictures')

# Define o caminho para a pasta de logs dentro do diretório da área de trabalho
log_path = os.path.join(desktop_path, 'Log')

# Cria a pasta de logs se ela não existir
if not os.path.exists(log_path):
    os.makedirs(log_path)

# Cria o arquivo de log se ele não existir
log_file_path = os.path.join(log_path, 'log.txt')
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write("Logs de Alterações:\n")

paths = {'documents': documents_path,
        'downloads': downloads_path,
        'pictures': pictures_path}