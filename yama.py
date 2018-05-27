from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from bs4 import BeautifulSoup
import dateutil.parser
import datetime

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def get_template_names():
    return [name[:-5] for name in os.listdir("templates") if os.path.isfile(os.path.join("templates", name)) and name.endswith(".html")]

def get_category_files(cat):
    out = []
    files = [os.path.join("content", cat, name) for name in os.listdir(os.path.join("content", cat)) if os.path.isfile(os.path.join("content", cat, name)) and name.endswith(".html")]
    for f in files:
        contents = Path(f).read_text()
        soup = BeautifulSoup(contents, 'html.parser')
        h1 = soup.find_all('h1')
        if len(h1) > 0:
            title = h1[0].text.strip()
        else:
            title = "Untitled"

        date = soup.find_all('span', {'id':'date'})
        if len(date) > 0:
            d = dateutil.parser.parse(date[0].text.strip())
        else:
            d = datetime.datetime.fromtimestamp(Path(f).stat().st_ctime)
        out.append({'filename': f, 'contents': contents, 'title': title, 'date': d})
    out.sort(key=lambda item:item['date'], reverse=True)
    return out

def render(file_dict):
    return file_dict['contents']

def generate():
    env = Environment(loader=FileSystemLoader('templates'))

    categories = get_immediate_subdirectories("content")
    ts = get_template_names()
    files_done = []
    for cat in categories:
        print(cat)
        if cat in ts:
            print("yes")
            # there is a template file for this category
            if not os.path.exists(os.path.join("output", cat)):
                os.makedirs(os.path.join("output", cat))
            category_files = get_category_files(cat)
            print(category_files)
            
            files_done.append({'category': cat, 'files': category_files})
    print("files done:")
    print(files_done)

    def category_list(name):
        o = ""
        for cl in files_done:
            if cl['category'] == name:
                o += "<ul>"
                for f in cl['files']:
                    o += "<li><a href=\"/"+cl['category']+"/"+os.path.basename(f['filename'])+"\">"+f['title']+"</a> <span id=\"date\">("+f['date'].date().isoformat()+")</span></li>\n"
                o += "</ul>"
                return o
            #else:
            #    return "[category "+name+" not found!]"    
    print(category_list("essay"))

    for cl in files_done:
        template = env.get_template(cl['category']+".html")
        template.globals['category_list'] = category_list
        for f in cl['files']:
            output_from_parsed_template = template.render(title=f['title'], text=f['contents'])
            print(output_from_parsed_template)

            with open(os.path.join("output", cl['category'], os.path.basename(f['filename'])), 'w') as the_file:
                the_file.write(output_from_parsed_template)

    template = env.get_template("index.html")
    template.globals['category_list'] = category_list
    output_from_parsed_template = template.render(title="Ue Kuniyoshi")
    with open(os.path.join("output", "index.html"), 'w') as the_file:
        the_file.write(output_from_parsed_template)

generate()
