import json, hashlib, os, base64, datetime
import argparse
import codecs
from lxml import html
from urllib import request
import codecs
from jinja2 import Environment, FileSystemLoader
from pprint import pprint as pp

doc_intro = {
    "doc-title": "XBRL Glossary Collection",
    "doc-abstract": "Terms used in XBRL collected from different sources with definition and translation.",
    "label-hide-intro-cb": "Show Glossary Only",
    "about-title": "About this document",
    "about-para-1": "<strong>XBRL</strong> (eXtensible Business Reporting Language) is an XML-based markup language used for exchanging business reports in a standard machine-readable format. <strong>XBRL</strong> is also referred to as <strong>Digital Reporting, Electronic Reporting, Structured Reporting and Tagged Reports</strong>.",
    "about-para-2": "<strong>XBRL</strong> glossary is vast, the objective of this page is to put together in one place a collection of <strong>XBRL</strong> terms extracted from multiple sources along with the translation of these terms if the translation is available.",
    "sources-used-title": "The sources used to extract the XBRL terms in this page are as follows:",
    "sources-li-1-1": "XBRL Taxonomy Development Handbook (“TDH”)",
    "sources-li-1-2": ", published by ",
    "sources-li-1-3":"The TDH has a rich glossary of 200+ terms, and, the definitions provided balances technical language with general language that non-technical readers can understand.",
    "sources-li-2-1": " on the website of ",
    "sources-li-2-2": "According to the website in describing the glossary they present \"Terms for concepts that are commonly referenced when discussing XBRL and electronic business reporting implementations. These terms are the preferred terms to be used in guidance materials.\"",
    "sources-li-3-1": "U.S. Securities and Exchange Committee (SEC)",
    "sources-li-3-2": "Definitions are short, straight to the point with “The least you need to know” approach.",
    "sources-li-4-1":"XBRL Specifications",
    "sources-li-4-2": "Precise technical definitions using technical language, meant for technical readers and software developers.",
    "translation-section-title": "Translations",
    "translation-section-1": "Select a language from the ",
    "translation-section-2": "language selector",
    "translation-section-3": "in the top right of this page or below to display terms translations in the selected language -if available. Translation of this page and the glossary can be add to this page in the form of a <code>JSON</code> file, please see github repo",
    "translation-section-4": "here",
    "translation-section-5": "for details.",
    "lang-notes-section-title": "Notes on translation for language [LANG NAME]",
    "lang-notes-section-text": "[Notes specific to a translation language presented go here]",
    "glossary-section-title": "Glossary",
    "glossary-section-1": "The terms in this glossary are extracted programmatically from the sources mentioned, unhandled errors in extraction can exist, each term has a link to its source page for reference.",
    "glossary-section-2": "Search terms using the search bar, search is based on term name only. Select language to display terms translations in the selected language if available.",
    "trans-note":"Note:",
    "title-1": "Select language to translate terms",
    "title-2": "Search English terms, searches only term name",
    "title-3": "Search translated terms, searches only term name",
    "placeholder-1": "Search English Terms..",
    "placeholder-2": "Search Translation..",
    "title-4": "Other acceptable variants",
    "title-5": "Notes on this translation.",
    "title-6": "Select A Source",
    "title-7": "Download Terms JSON file",
    "title-8": "Sort English terms alphabetically",
    "title-9": "Sort Translated terms alphabetically",
    "label-hide-defs-cb": "Hide Definitions"
}

icons = {
    'linkedin': '<svg aria-hidden="true" role="img" viewBox="0 0 448 512" style="height:1.25em;width:1.25em;vertical-align:0em;margin-left:auto;margin-right:auto;font-size:inherit;fill:darkgrey;overflow:visible;position:relative;"><path d="M416 32H31.9C14.3 32 0 46.5 0 64.3v383.4C0 465.5 14.3 480 31.9 480H416c17.6 0 32-14.5 32-32.3V64.3c0-17.8-14.4-32.3-32-32.3zM135.4 416H69V202.2h66.5V416zm-33.2-243c-21.3 0-38.5-17.3-38.5-38.5S80.9 96 102.2 96c21.2 0 38.5 17.3 38.5 38.5 0 21.3-17.2 38.5-38.5 38.5zm282.1 243h-66.4V312c0-24.8-.5-56.7-34.5-56.7-34.6 0-39.9 27-39.9 54.9V416h-66.4V202.2h63.7v29.2h.9c8.9-16.8 30.6-34.5 62.9-34.5 67.2 0 79.7 44.3 79.7 101.9V416z"/></svg>',
    'github': '<svg aria-hidden="true" role="img" viewBox="0 0 496 512" style="height:1.25em;width:0.97em;vertical-align:0em;margin-left:auto;margin-right:auto;font-size:inherit;fill:darkgrey;overflow:visible;position:relative;"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg>',
    'email': '<svg aria-hidden="true" role="img" viewBox="0 0 448 512" style="height:1.25em;width: 1.25em;vertical-align:0em;margin-left:auto;margin-right:auto;font-size:inherit;fill:darkgrey;overflow:visible;position:relative;"><path d="M400 32H48C21.49 32 0 53.49 0 80v352c0 26.51 21.49 48 48 48h352c26.51 0 48-21.49 48-48V80c0-26.51-21.49-48-48-48zM178.117 262.104C87.429 196.287 88.353 196.121 64 177.167V152c0-13.255 10.745-24 24-24h272c13.255 0 24 10.745 24 24v25.167c-24.371 18.969-23.434 19.124-114.117 84.938-10.5 7.655-31.392 26.12-45.883 25.894-14.503.218-35.367-18.227-45.883-25.895zM384 217.775V360c0 13.255-10.745 24-24 24H88c-13.255 0-24-10.745-24-24V217.775c13.958 10.794 33.329 25.236 95.303 70.214 14.162 10.341 37.975 32.145 64.694 32.01 26.887.134 51.037-22.041 64.72-32.025 61.958-44.965 81.325-59.406 95.283-70.199z"/></svg>'
}

def extract_text(elts):
    list_texts = [''.join(list(x.itertext())) for x in elts]
    t_txt = ' '.join(list_texts).replace('\n','')
    t_txt = ' '.join([x.strip() for x in t_txt.split(' ') if x])
    return t_txt

# Get terms from sources
def getTermsFromSources(sourcesFile= './json/sources.json', saveToFile='./json/langs'):
    with open(sourcesFile, 'r') as jf:
        sources = json.load(jf)
    result = dict()
    for i,s in sources.items():
        link = s["base-link"]
        print('Getting terms from {} ==> {}'.format(s['sub-type'], link))
        terms_list_xpath = s['xpath-to-terms-and-definitions']
        terms_xpath = s['xpath-to-terms']
        defs_xpath = s['xpath-to-definitions']
        is_dl = s['is-dl']
        doc_root = html.parse(request.urlopen(link)).getroot()
        list_of_terms = doc_root.xpath(terms_list_xpath)
        if is_dl:
            dds = []
            dts = []
            for d in list_of_terms:
                for t in d:
                    if t.tag == 'dd':
                        dds.append(t)
                    elif t.tag=='dt':
                        dts.append(t)
            merged_elts = []
            for x in zip(dts, dds):
                term = html.Element('term')
                for _x in x:
                    term.append(_x)
                merged_elts.append(term)
            list_of_terms = merged_elts
        
        # store term id, might need the previous term
        term_id = None    
        for t in list_of_terms:
            term_dict = dict()
            t_name = t.xpath(terms_xpath)
            term_name = extract_text(t_name)
            t_def = t.xpath(defs_xpath)
            term_def = extract_text(t_def)
            # Fix for source 3 (term is not isolated in source) one time fix
            if int(i) == 4 and not t_name and len(t_def):
                t_name = []
                for o_d in t_def:
                    if len([o_d.find('./a')]):
                        term_name += ', ' if term_name  else '' + o_d.find('./a').attrib['title'] if len([o_d.find('./a')]) else ''
                        t_name.append(html.fromstring('<span class="term">{}</span>'.format( o_d.find('./a').attrib['title'] if len([o_d.find('./a')]) else '')))
            
            # Ignore blank elements in tdh glossary section
            if int(i) == 5 and not t_name and (not term_def or 
                                        'this page intentionally left blank' in term_def or 
                                        'This glossary contains terms used within' in term_def):
                continue
            # Combine multi elements in XBRL dimension definition with previous element, one time fix
            if int(i) == 5 and not term_name and term_def and term_id:
                # get last element
                prev_elt = result[term_id]
                prev_elt['term-definition'] += '\n' + term_def
                prev_elt_html_def = html.fromstring(prev_elt['term-definition-html'])
                for _t_d in t_def:
                    prev_elt_html_def.append(html.fromstring(html.tostring(_t_d, with_tail=False)))
                prev_elt['term-definition-html'] = html.tostring(prev_elt_html_def, with_tail=False)
                continue
            t_name_parent = html.Element('term')
            for _t_n in t_name:
                if is_dl:
                    _t_n.tag = 'span'
                t_name_parent.append(html.fromstring(html.tostring(_t_n, with_tail=False)))
            t_def_parent = html.Element('definition')
            for _t_d in t_def:
                if is_dl:
                    _t_d.tag='span'
                t_def_parent.append(html.fromstring(html.tostring(_t_d, with_tail=False)))
            term_dict['term-name'] = term_name
            term_dict['term-definition'] = term_def
            term_dict['term-name-html'] = html.tostring(t_name_parent, with_tail=False)
            term_dict['term-definition-html'] = html.tostring(t_def_parent, with_tail=False)
            term_dict['source-key'] = i
            term_dict['source-group'] = s["source-group"]
            term_id = hashlib.md5(json.dumps(term_dict, default= lambda x: x.decode()).encode()).hexdigest()
            result[term_id] = term_dict

    en_dict = {
        'lang-meta': {
            'symbol': 'en',
            'name': 'English',
            'dir': 'ltr'
        },
        'intro': {k:{'en':v} for k,v in doc_intro.items()},
        'glossary': result
    }
    save_result = os.path.join(saveToFile, 'en.json')  
    with open(save_result, 'x') as rf:
        json.dump(en_dict, rf, default= lambda x: x.decode())
    print('Got items from sources and saved results to {}'.format(os.path.abspath(saveToFile)))
    return os.path.abspath(saveToFile)

def makeTranslationFile(langSymbol, langName, langDirection, translatorName=[], translatorEmail='',
                        translatorLinkedin='', translatorGithub='', saveFolder='./json/langs'):
    '''Prepares a json file with English text to be tanslated
    langSymbol: as in here http://www.lingoes.net/en/translator/langcode.htm
    langName: as in here http://www.lingoes.net/en/translator/langcode.htm
    langDirection: one of 'ltr'|'rtl' (left to right or right to left)
    optional translator info for credits, information is a dict for name (list of 1 or 2 names for names in English and in language),
    linkedin link, github link, email (all fields option), lang jason can have more than one translator object.
    '''
    with open('./json/langs/en.json', 'r') as ef:
        en_dict = json.load(ef)
    template_dict = {
        "term-name-lang": "",
        "term-name-lang-variants": [],
        "term-definition-lang": "",
        "translation-notes": ""
    }

    translate_dict = {
        'lang-meta': {
            'symbol': langSymbol,
            'name': langName,
            'dir': langDirection,
            'translated-by':[
                {
                    'name': translatorName, 
                    'email': translatorEmail, 
                    'linkedin': translatorLinkedin, 
                    'github': translatorGithub
                },
            ]
        },
        'intro': {k: {'en': v['en'], langSymbol: ''} for k, v in en_dict['intro'].items()},
        'glossary': {k: {'term-name': v['term-name'], 'term-definition': v['term-definition'], **template_dict} for k, v in en_dict['glossary'].items()}
    }

    fileName = os.path.join(saveFolder, langSymbol + '.json' )
    with codecs.open(fileName, 'x', 'utf-8') as rf:
        rf.write(json.dumps(translate_dict, ensure_ascii=False))

    print('Created language translation template @ {}'.format(
        os.path.abspath(fileName)))
    return os.path.abspath(fileName)

def makeAllLangsDict(saveFolder='./json', overWrite=False):
    en_file = './json/langs/en.json'
    langs_dir = './json/langs'
    langs_files = [f for f in os.listdir(langs_dir) if not f=='en.json']

    with open(en_file, 'r') as ef:
        en_dict = json.load(ef)

    mega_dict = {
        'langs': {'en': en_dict['lang-meta']},
        'intro': en_dict['intro'],
        'glossary': {k:{'en':v} for k,v in en_dict['glossary'].items()}
    }

    excludes = ['term-name', 'term-definition']

    for f in langs_files:
        lang_symbol = os.path.splitext(f)[0]
        lang_file = os.path.join(langs_dir, f)
        with open(lang_file, 'r') as lf:
            lang_dict = json.load(lf)

        mega_dict['langs'][lang_symbol] = lang_dict['lang-meta']
        
        for k,v in lang_dict['intro'].items():
            mega_dict['intro'][k][lang_symbol] = v[lang_symbol]

        for _k,_v in lang_dict['glossary'].items():
            mega_dict['glossary'][_k][lang_symbol] = {x:y for x,y in _v.items() if not x in excludes}
        
    fileName = os.path.join(saveFolder, 'all-langs.json')
    with codecs.open(fileName, 'w' if overWrite else 'x', 'utf-8') as rf:
        rf.write(json.dumps(mega_dict, ensure_ascii=False))
    print('Created all languages file @ {}'.format(os.path.abspath(fileName)))
    return os.path.abspath(fileName)

def encodeB64Files():
    '''Returns base64 text for css and js to be embedded in html template'''
    with open('./json/all-langs.json', 'r') as lf:
        all_langs_dict = json.dumps(json.load(lf))
    
    with open('./resources/main.css', 'r') as cf:
        css = cf.read()
    
    with open('./resources/main.js', 'r') as cf:
        js = cf.read()
    
    def doEncode(text):
        text_bytes = text.encode('ascii')
        base64_bytes = base64.b64encode(text_bytes)
        text_b64 = base64_bytes.decode('ascii')
        return text_b64

    all_langs_dict_text = 'const allLangs = ' + all_langs_dict
    
    return {'allLangs': doEncode(all_langs_dict_text), 'cssFile': doEncode(css), 'jsFile': doEncode(js)}

def makeMainPage(saveTo = './docs/xbrl-glossary-collection.html'):
    templates_folder = 'templates'
    template_name = 'main_template.html'
    
    file_loader = FileSystemLoader(templates_folder)
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)
    with open('./json/all-langs.json', 'r') as jf:
        x_text = json.load(jf)
    with open('./json/sources.json', 'r') as jf:
        sources = json.load(jf)
    with open('./json/ignored-terms.json', 'r') as jf:
        ignored = json.load(jf)

    b64Files = encodeB64Files()

    translators = []
    for lang, v in x_text['langs'].items():
        if lang == 'en':
            continue
        else:
            for translator in v['translated-by']:
                translator_dict = translator.copy()
                translator_dict['name'] = translator['name'][0] if isinstance(translator.get('name'), list) else translator.get('name', '')
                translator_dict['lang'] = lang
                translators.append(translator_dict)

    lastupdateDate = str(datetime.datetime.now().date())
    lastUpdateDateString = datetime.datetime.now().date().strftime('%B %Y')

    output = template.render(intro=x_text['intro'], 
                            dir="ltr", glossary=x_text['glossary'], 
                            lang='en', langs=x_text['langs'],
                            sources=sources,
                            icons=icons, lastupdateDate=lastupdateDate, 
                            lastUpdateDateString=lastUpdateDateString,
                            author = "Sherif M. ElGamal",
                            translators = translators,
                            ignored=ignored,
                            **b64Files
                            )
    with open(saveTo, 'w') as wf:
        wf.write(output)
    print('Created landing page @ {}'.format(os.path.abspath(saveTo)))

def mergeTranslationTemplates(oldTemplate, newTemplate, lang, outFile):
    '''Merge old with new templates of same language'''
    file_with_translations = oldTemplate
    new_template_file = newTemplate

    with open(file_with_translations, 'r') as rf:
        lang_trans = json.load(rf)

    with open(new_template_file, 'r') as rf:
        lang_template = json.load(rf)

    for k,v in lang_trans['intro'].items():
        lang_template['intro'][k][lang] = v[lang]

    for k,v in lang_trans['glossary'].items():
        for _v in lang_template['glossary'].values():
            t_name = _v['term-name']
            t_define = _v['term-definition']
            if t_name:
                if t_name == v['term-name'] and t_define == v['term-definition']:
                    _v["term-name-lang"] = v["term-name-lang"]
                    _v["term-name-lang-variants"] = v["term-name-lang-variants"]
                    _v["term-definition-lang"] = v["term-definition-lang"]
                    _v["translation-notes"] = v["translation-notes"]
                    print('hit')
                    break

    with codecs.open(outFile, 'x', 'utf-8') as rf:
        rf.write(json.dumps(lang_template, ensure_ascii=False))
    print('Saved new merged template to {}'.format(os.path.abspath(outFile)))
    return os.path.abspath(outFile)

def main():
    parser = argparse.ArgumentParser(description='All functions relating to building XBRL Glossary Page')
    # Terms stable for now
    # parser.add_argument('--get-terms', dest='getTerms', default=False, action="store_true",
    #                     help=('Whether to fetch terms from sources'))
    # parser.add_argument('--save-terms', type=str, dest='saveTermsFile', default='./json/langs',
    #                     help=('Location to save English terms extracted, defaults to ./json/langs/en.json'))
    parser.add_argument('--make-lang', dest='makeLang', default=False, action="store_true",
                        help=('Make translation file for language, information needs to be given'))
    parser.add_argument('--lang-symbol', type=str, dest='langSymbol', 
                        help=('Language symbol as in http://www.lingoes.net/en/translator/langcode.htm'))
    parser.add_argument('--lang-name', type=str, dest='langName', 
                        help=('Language name as in http://www.lingoes.net/en/translator/langcode.htm'))
    parser.add_argument('--lang-direction', type=str, dest='langDir', 
                        help=('Language direction, either ltr (left to right) or rtl'))
    parser.add_argument('--translator-name', type=list, dest='translatorName', nargs='+',
                        default=[], help=(' optional name of translator, maybe 2 names, one in English and one in language'))
    parser.add_argument('--translator-email', type=str, dest='translatorEmail',
                        help=('optional email of translator'))
    parser.add_argument('--translator-linkedin', type=str, dest='translatorLinkedin',
                        help=('optional linkedin of translator'))
    parser.add_argument('--translator-github', type=str, dest='translatorGithub',
                        help=('optional github of translator'))
    parser.add_argument('--langs-folder', type=str, dest='langsFolder', default='./json/langs/',
                        help=('optional save folder of the lang file, defaults to ./json/langs/ and file must'
                                'ultimately be saved in that folder to be included in the page'))
    parser.add_argument('--make-langs', dest='makeAllLangs', default=False, action="store_true",
                        help=('Combines all langs in one file to include in page data'))
    parser.add_argument('--make-langs-folder', type=str, dest='makeAllLangsFolder', default='./json/',
                        help=('folder to save all langs file to, defaults to ./json/ to be found when building page'))
    parser.add_argument('-o', dest='overWrite', default=False, action='store_true',
                        help=('overwrite all langs file'))
    parser.add_argument('--make-page', dest='makePage', default=False, action="store_true",
                        help=('build html page'))
    parser.add_argument('--page-save', type=str, dest='pageSave', default='./docs/xbrl-glossary-collection.html',
                        help=('HTML save location, defaults to ./docs/xbrl-glossary-collection.html'))
    parser.add_argument('--merge-trans-files', dest='mergeTrans', default=False, action="store_true",
                        help=('merge an old translation file with new one, translator info to be added manually as a new dict'))
    parser.add_argument('--old', type=str, dest='oldTemplate', help=('old translation file'))
    parser.add_argument('--new', type=str, dest='newTemplate', help=('new translation file'))
    parser.add_argument('--out', type=str, dest='outFile', help=('merged file location'))
    parser.add_argument('--lang', type=str, dest='lang', help=('lang of the merged files'))

    opts = parser.parse_args()
    if getattr(opts, 'optsgetTerms', False):
        getTermsFromSources(saveToFile=opts.saveTermsFile)
    if opts.makeLang:
        makeTranslationFile(
            langSymbol=opts.langSymbol,
            langName=opts.langName,
            langDirection=opts.langDir,
            translatorName=opts.translatorName,
            translatorEmail=opts.translatorEmail,
            translatorLinkedin=opts.translatorLinkedin,
            translatorGithub=opts.translatorGithub,
            saveFolder=opts.langsFolder
        )
    if opts.makeAllLangs:
        makeAllLangsDict(saveFolder=opts.makeAllLangsFolder, overWrite=opts.overWrite)
    if opts.makePage:
        makeMainPage(saveTo=opts.pageSave)

    if opts.mergeTrans:
        mergeTranslationTemplates(
        oldTemplate=opts.oldTemplate,
        newTemplate=opts.newTemplate,
        outFile=opts.outFile,
        lang=opts.lang
        )

if __name__ == '__main__':
    main()
