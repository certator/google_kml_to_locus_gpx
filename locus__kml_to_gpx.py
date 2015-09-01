import re, copy, os, md5
from lxml import etree
from bs4 import BeautifulSoup
from lxml.etree import CDATA
import subprocess 

#urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)



#template = etree.parse("template.gpx")

#with open('template.gpx') as f: s = f.read()
#tmpl = BeautifulSoup(s, 'lxml')

#with open('doc.kml') as f: s = f.read()
#kml = BeautifulSoup(s, 'html.parser')

tmpl = etree.parse("template.gpx")
troot = tmpl.getroot()
wpt_tmpl = tmpl.getroot().findall('{http://www.topografix.com/GPX/1/1}wpt')[0]
troot.remove(wpt_tmpl)

kml = etree.parse('doc.kml')

try:
    os.makedirs('attachments')
except:
    pass


nss = {'namespaces':{'ns': 'http://www.opengis.net/kml/2.2'}}
nssg = {'namespaces':{'ns': 'http://www.topografix.com/GPX/1/1'}}

for pm in kml.xpath('//ns:Placemark', **nss):
    name = pm.xpath('ns:name', **nss)[0].text
    print name
    lon, lat, nop = pm.xpath('ns:Point/ns:coordinates', **nss)[0].text.split(',')
    
    desc = ''
    try:
        desc = pm.xpath('ns:description', **nss)[0].text
    except:
        print 'no desc!'
        pass

    styleUrl = pm.xpath('ns:styleUrl', **nss)[0].text
    sm = kml.xpath("//ns:StyleMap[@id='%s']" % styleUrl[1:], **nss)[0]
    norm = sm.xpath("ns:Pair/ns:key[text()[contains(., 'normal')]]", **nss)[0]
    norm_id = norm.getparent().xpath('ns:styleUrl', **nss)[0].text
    st = kml.xpath("//ns:Style[@id='%s']" % norm_id[1:], **nss)[0]
    icon = st.xpath("ns:IconStyle/ns:Icon/ns:href", **nss)[0].text
    fpath = 'attachments/%s' % icon.rpartition('/')[-1]
    if not os.path.exists(fpath):
        r = requests.get(icon)
        with open(fpath, 'w') as f: f.write(r.content)
    #icon = fpath

    wpt = copy.deepcopy(wpt_tmpl)
    wpt.xpath('ns:name', **nssg)[0].text = name
    wpt.attrib['lat'] = lat
    wpt.attrib['lon'] = lon
    wpt.xpath('.//locus:icon', namespaces={'locus': 'http://www.locusmap.eu'})[0].text = icon
    wpt_link_t = wpt.xpath('ns:link', **nssg)[0]
    wpt.remove(wpt_link_t)

    urls = [u[0] for u in re.findall(r'(http[s]?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*))', desc)]
    for u in sorted(set(urls), key=lambda f: len(f)):
        print u
        m = md5.md5()
        m.update(u)
        norm_name = re.sub(r'[^a-zA-Z0-9]', '_', u) + '_' + m.hexdigest()[:4]
        fpath = './attachments/%s.pdf' % norm_name
        if not os.path.exists(fpath):
            subprocess.check_output(['/home/kos/dev/3rdparty/cutycapt-code/CutyCapt/CutyCapt', '--delay=300', '--url=%s' % u, '--out=%s' % fpath], stderr=subprocess.STDOUT)
        hu = '<a href="%s">%s</a>' % (u, u,)
        desc = desc.replace(u, hu)
        link = copy.deepcopy(wpt_link_t)
        link.attrib['href'] = fpath
        link.xpath('ns:text', **nssg)[0].text = u
        link.remove(link.xpath('ns:text', **nssg)[0])
        wpt.append(link)
        #	<link href="./attach/meteor1.pdf" />

    wpt.xpath('ns:desc', **nssg)[0].text = CDATA(desc)


    troot.append(wpt)


s1 = etree.tostring(tmpl, encoding='utf-8')
with open('out.gpx', 'w') as f: f.write(s1)


