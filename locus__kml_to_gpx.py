import re, copy, os, md5, requests, subprocess, sys, glob, argparse

from lxml import etree
from bs4 import BeautifulSoup
from lxml.etree import CDATA
from zipfile import ZipFile

parser = argparse.ArgumentParser(description="Convert google kml to gpx format with locus extensions")

parser.add_argument('-i', '--in',  dest='kml', help='source kml file')
parser.add_argument('-o', '--out', dest='gpx', help='write result to gpx file')
parser.add_argument('-d', '--dir', dest='dir', help='attachment directory (local)', default='attachments')
parser.add_argument('-z', '--zip', dest='zip', help='pack all to zip')

args = parser.parse_args()

if args.kml is None or args.gpx is None:
    parser.print_help()
    sys.exit(1)

gpx_tmpl = etree.parse("template.gpx")
gpx_root = gpx_tmpl.getroot()
wpt_tmpl = gpx_tmpl.getroot().findall('{http://www.topografix.com/GPX/1/1}wpt')[0]
gpx_root.remove(wpt_tmpl)

kml = etree.parse(args.kml)

try:
    os.makedirs(args.dir)
except:
    pass

nss = {'namespaces':{'ns': 'http://www.opengis.net/kml/2.2'}}
nssg = {'namespaces':{'ns': 'http://www.topografix.com/GPX/1/1'}}

files = []

names = set()

def choose_unique_name(name, names):
    new_name = name 
    i = 1
    while new_name in names:
        new_name = name + "_" + str(i)
        i += 1
    return new_name 

def extract_urls(s):
    return re.findall(r'(http[s]?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=\(\)]*))', s)

def download_attachement(url, fpath):
    cmd = [os.environ['CUTYCAPT'] + '/CutyCapt', 
        '--delay=3000', 
        '--url=%s' % url, 
        '--out=%s' % fpath, 
        '--print-backgrounds=on', 
        '--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36"']
    
    if not os.path.exists(fpath):            
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)

for pm in kml.xpath('//ns:Placemark', **nss):
    name = pm.xpath('ns:name', **nss)[0].text
    name = choose_unique_name(name, names)
    names.add(name)
    print name
    lon, lat, nop = pm.xpath('ns:Point/ns:coordinates', **nss)[0].text.split(',')
    
    desc = ''
    try:
        desc = pm.xpath('ns:description', **nss)[0].text
    except:
        print 'no desc!'      

    styleUrl = pm.xpath('ns:styleUrl', **nss)[0].text
    sm = kml.xpath("//ns:StyleMap[@id='%s']" % styleUrl[1:], **nss)[0]
    norm = sm.xpath("ns:Pair/ns:key[text()[contains(., 'normal')]]", **nss)[0]
    norm_id = norm.getparent().xpath('ns:styleUrl', **nss)[0].text
    st = kml.xpath("//ns:Style[@id='%s']" % norm_id[1:], **nss)[0]
    icon = st.xpath("ns:IconStyle/ns:Icon/ns:href", **nss)[0].text
    fpath = '%s/%s' % (args.dir, icon.rpartition('/')[-1])
    if not os.path.exists(fpath):
        if 'http' not in icon:    
            with open(icon) as f:
                content = f.read()
        else:   
            r = requests.get(icon)
            content = r.content
        with open(fpath, 'w') as f: f.write(content)
    files += [fpath]    

    wpt = copy.deepcopy(wpt_tmpl)
    wpt.xpath('ns:name', **nssg)[0].text = name
    wpt.attrib['lat'] = lat
    wpt.attrib['lon'] = lon
    wpt.xpath('.//locus:icon', namespaces={'locus': 'http://www.locusmap.eu'})[0].text = icon
    wpt_link_tmpl = wpt.xpath('ns:link', **nssg)[0]
    wpt.remove(wpt_link_tmpl)

    urls = [url[0] for url in extract_urls(desc)]
    for url in sorted(set(urls), key=lambda f: len(f)):
        print url
        url_hash = md5.md5()
        url_hash.update(url)
        norm_name = re.sub(r'[^a-zA-Z0-9]', '_', url) + '_' + url_hash.hexdigest()[:4]
        fpath = './%s/%s.pdf' % (args.dir, norm_name)
        files += [fpath]
        download_attachement(url, fpath)

        link = copy.deepcopy(wpt_link_tmpl)
        link.attrib['href'] = fpath
        link.xpath('ns:text', **nssg)[0].text = url
        link.remove(link.xpath('ns:text', **nssg)[0])
        wpt.append(link)

        html_url = '<a href="%s">%s</a>' % (url, url,)
        desc = desc.replace(url, html_url)

    wpt.xpath('ns:desc', **nssg)[0].text = CDATA(desc)
    gpx_root.append(wpt)


gpx_xml = etree.tostring(gpx_tmpl, encoding='utf-8')
with open(args.gpx  , 'w') as f: 
    f.write(gpx_xml)


if not args.zip is None:
    with ZipFile(args.zip, 'w') as zip_file:
        zip_file.write(args.gpx)
        for fn in set(files):            
            zip_file.write(fn, fn)



