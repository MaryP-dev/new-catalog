import os
import re

# Папка с документами (можно настроить)
docs_folder = '1s-dokumentooborot'

# Регулярка для поиска тега (можно уточнить)
tag_pattern = re.compile(r'<view\s+display="List"\s*/>')

def get_page_list(folder_path, current_file):
    """Возвращает HTML-список всех .md файлов в папке, кроме текущего."""
    items = []
    for f in os.listdir(folder_path):
        if f.endswith('.md') and f != current_file:
            name = os.path.splitext(f)[0]
            # Формируем ссылку: имя файла без расширения (Jekyll превратит в .html)
            link = f"/new-catalog/{os.path.basename(folder_path)}/{name}"
            title = name.replace('-', ' ').title()  # Заголовок из имени файла
            items.append(f'<li><a href="{link}">{title}</a></li>')
    if not items:
        return ''  # если других страниц нет, можно вернуть пустую строку или заглушку
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

def process_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if tag_pattern.search(content):
                    print(f'Processing {filepath}')
                    new_content = tag_pattern.sub(get_page_list(root, file), content)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == '__main__':
    process_files()
