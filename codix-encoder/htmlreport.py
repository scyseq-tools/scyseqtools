from string import Template

def to_html_report(specs):

    #{'date': 'Mon Feb 13 08:02:19 2023', 
    #'project': 'Mon beau projet', 
    #'description': 'Ceci est une description', 
    #'period': 10.0, 
    #'codes': {
    #    'code1': ['symb1', 'symb2', 'symb3'], 
    #    'code2': ['symb1', 'symb2', 'symb3']
    #}, 
    #'sites': {
    #    'toto': ['code1'], 
    #    'tutu': ['code1', 'code2'], 
    #    'titi': ['code2']
    #}
    #}
    tmpl = """<!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>${Title}</title>
      </head>
      <body>
        ${Body}
      </body>
    </html>"""

    main_html = Template(tmpl)
    header_html = Template('<h1>${titre}</h1>')
    date_html = Template('<p><strong>Defined on:</strong> <em>${date}</em></p>')
    description_html = Template('<h1>Description</h1> <p>${description}</p>')
    timing_html = Template('<p><strong>${timing} coding</strong></p>')
    codes_html = Template('<p><strong>${code}:</strong> ${symbols}</p>')
    sites_html = Template('<p><strong>${site}:</strong> ${codes}</p>')

    main = ' '.join(["Coding framework for", specs['project']])
    titre = header_html.safe_substitute(titre = main)
    date = date_html.safe_substitute(specs)
    description = description_html.safe_substitute(specs)

    if specs['period'] is None:
        time_code = "Continuous"
        timing = timing_html.safe_substitute(timing = time_code)
    else:
        time_code = "Regular"
        timing = timing_html.safe_substitute(timing = time_code)
        timing += '<p><strong>Interval: </strong> %5.3f seconds</p>' % specs['period']

    header = '\n'.join([titre, date, description, timing])

    codes = ['<h1>Codes</h1>']
    for c, v in specs['codes'].items():
        codes.append(codes_html.safe_substitute(code = c, symbols = str(v)))

    code = '\n'.join(codes)

    sites = ['<h1>Sites</h1>']
    for s, v in specs['sites'].items():
        sites.append(sites_html.safe_substitute(site = s, codes = str(v)))
 
    site = '\n'.join(sites)

    body = '\n'.join([header, code, site])

    return main_html.safe_substitute(Title=main, Body=body)

