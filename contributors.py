import json
import urllib2

def get(url):
    request = urllib2.Request(url)
    result = None

    try:
        result = urllib2.urlopen(request)
        json_result = json.loads(result.read())
        return json_result
    except Exception, e:
        print str(e.read())

def extract_contributors(json_data):
    contributors = []
    for contributor in json_data:
        contributors.append(str(contributor['login']))

    return contributors

def extract_info(json_data):
    info = {}

    try:
        info['name'] = json_data['name']
        info['login'] = json_data['login']
        info['company'] = json_data['company']
        info['blog'] = json_data['blog']
        info['location'] = json_data['location']
        info['email'] = json_data['email']
    except Exception, e:
        None

    return info

def rax_affiliation(json_data):
    words = ['rax', 'rack', 'racker', 'rackspace']
    contributors_info = {}

    for info in json_data:
        for word in words:
            for key in info:
                try:
                    if word in info[key].lower():
                        if info['login'] not in contributors_info:
                            contributors_info[info['login']] = info
                except Exception, e:
                    None

    return contributors_info

owner = "openstack"
repos = ['savanna', 'savanna-dashboard', 'savanna-extra',
'savanna-image-elements', 'python-savannaclient']
url = "https://api.github.com"
client = "?client_id=XXXXXXXXXXXXXXXXXXXX&client_secret=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"

for repo in repos:
    print "\n################################################################"
    print "Owner/Repo: %s / %s" % (owner, repo)
    print "----------------------------------------------------------------\n"
    temp_url = url + "/repos/%s/%s/contributors%s" % (owner, repo, client)
    json_data = get(temp_url)
    contributors = extract_contributors(json_data)

    all_info = []
    for contributor in contributors:
        temp_url = url + "/users/%s%s" % (contributor, client)
        json_data = get(temp_url)
        info = extract_info(json_data)
        all_info.append(info)
        print info

    rax_affiliations = rax_affiliation(all_info)
    print "\n\n----------------------------------------------------------------"
    print "Rackspace Affiliation: %s | Count = %d" % (rax_affiliations, len(rax_affiliations))
    print "\n\n################################################################"
