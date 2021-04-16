import subprocess
import re
import json

p = subprocess.Popen(
    # "where chkdsk.exe",
    "curl https://api.ratesapi.io/api/2021-04-01",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)

retval = p.wait()
print(retval)

if p and p.stdout:
    r = re.compile(r'\{"(.*)"\}')
    response_text = p.stdout.read().decode('UTF-8')
    match = r.search(response_text)
    if match:
        rates = json.loads("{\"" + match.groups()[0] + "\"}")
        print(rates["rates"]["JPY"])


