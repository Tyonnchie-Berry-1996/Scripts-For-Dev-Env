#!/usr/bin/python3
import os
import subprocess
import urllib3
import bugzilla
import re
import json
import requests

urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs="/etc/ssl/certs/ca-bundle.trust.crt")


def product_finder():
    try:
        URL = "bugzilla.redhat.com/"

        r = requests.get(f"http://{URL}/rest/product_selectable")

        data_set = r.json()

        json_id = json.dumps(data_set, indent=2)

        with open('id_advisories.json', 'w') as e:
            e.write(json_id)

        with open("id_advisories.json", 'r') as e:
            id_object = json.loads(e.read())

        for x in range(0, id_object):
            product_id = id_object['ids'][x]

            r = requests.get(f"http://{URL}rest/product/{product_id}")

            new_set = r.json()

            json_id = json.dumps(new_set, indent=2)

            print(json_id)

    except IndexError:
        pass


def bugz_finder():
    try:
        expanded_path = os.path.expandvars('/root/.bashrc')

        result = subprocess.run(
            ['bash', '-c', f'source {expanded_path} && echo $BUGZILLA_API_KEY'],
            capture_output=True,
            text=True
        )
        api_key = result.stdout.strip()

        if api_key:
            api_key = api
            print("API key set from bashrc\n")

        if api_key == "":
            api_key_file = "/home/src/API-Scripts/temp-holder.txt"
            print("No API key found, setting temporary placeholder.")
            input_user = input("\nCopy and paste your open API key\n ")
            set_key = subprocess.run([f"echo {input_user} > {api_key_file}"], shell=True, check=True)
            user_key = subprocess.check_output(["cat", api_key_file], text=True).strip()
            api_key = user_key


        URL = "bugzilla.redhat.com/"

        bzapi = bugzilla.Bugzilla(URL, api_key=api_key, force_rest=True)
        assert bzapi.logged_in

        query = bzapi.build_query(product="Fedora",
                                  component="kernel",
                                  limit=5
                                  )

        bugs = bzapi.query(query)

        print(f"\nFound {len(bugs)} bugs in query")

        for i in range(0, len(bugs)):
            matches = re.findall(r"[#]\d{1,10}", str(bugs[i]))

            bug_num = matches[0]
            bug_id = bug_num[1:len(bug_num) - 1 + 1]
            link = "https://bugzilla.redhat.com/show_bug.cgi?id=" + bug_id

            print(bugs[i], "\n", link, "\n")

        temp_file = f"/home/src/API-Scripts/temp-holder.txt"
        if len(str(temp_file)) > 0:
            with open(temp_file, 'w') as f:
                f.write('')
                os.remove(temp_file)
                
    except IndexError:
        pass

if __name__ == '__main__':
    bugz_finder()


