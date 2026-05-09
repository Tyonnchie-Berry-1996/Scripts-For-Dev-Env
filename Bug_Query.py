#!/usr/bin/python3
import os
import subprocess
import urllib3
import bugzilla
import re
import json
import requests

urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs="/etc/ssl/certs/ca-bundle.trust.crt")


def bugz_finder():
    try:
        expanded_path = os.path.expandvars('$HOME/.bashrc')

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
            api_key_file = "/home/src/Scripts-For-Dev-Env/temp-holder.txt"
            print("\nNo API key found, setting temporary placeholder.")
            
            input_user = input("\nCopy and paste your Bugzilla API key\n ")
            subprocess.run([f"echo {input_user} > {api_key_file}"], shell=True, check=True)
            
            user_key = subprocess.check_output(["cat", api_key_file], text=True).strip()
            api_key = user_key

            subprocess.run(["clear"])


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

        temp_file = f"/home/src/Scripts-For-Dev-Env/temp-holder.txt"
        if len(str(temp_file)) > 0:
            with open(temp_file, 'w') as f:
                f.write('')
                  
    except IndexError:
        pass

if __name__ == '__main__':
    bugz_finder()


