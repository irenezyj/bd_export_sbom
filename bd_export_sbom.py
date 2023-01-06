'''
Created on Jan 6, 2023

@author: irenez

Generate SBOM report for a given project-version, report type and report format

'''

from blackduck import Client

import argparse
import json
import logging
import sys
import time

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s"
)


parser = argparse.ArgumentParser("A program to create a SBOM report for a given project-version")
parser.add_argument("bd_url", help="Hub server URL e.g. https://your.blackduck.url")
parser.add_argument("token_file", help="containing access token")
parser.add_argument("project_name")
parser.add_argument("version_name")
parser.add_argument("-t", "--type", type=str, nargs='?', default="SPDX_22", choices=["SPDX_22", "CYCLONEDX_13", "CYCLONEDX_14"], help="Choose the type of SBOM report")
parser.add_argument("-f", "--format", type=str, nargs='?', default="JSON", choices=["JSON", "YAML", "RDF", "TAGVALUE"], help="Choose the format of SBOM SPDX report")
parser.add_argument('-r', '--retries', default=10, type=int, help="How many times to retry checking report status, i.e. wait for the report to be generated")
parser.add_argument('-s', '--sleep_time', default=5, type=int, help="The amount of time to sleep in-between (re-)tries to check report status")
parser.add_argument('--no-verify', dest='verify', action='store_false', help="disable TLS certificate verification")

args = parser.parse_args()

if args.type == "SPDX_22" and args.format not in ["YAML", "RDF", "TAGVALUE"]:
    print(f"Wrong combined report type: {args.type} and report format: {args.format}")
    sys.exit(2)

if (args.type == "CYCLONEDX_13" or args.type == "CYCLONEDX_14") and args.format != "JSON":
    print(f"Wrong combined report type: {args.type} and report format: {args.format}")
    sys.exit(2)

   
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', stream=sys.stderr, level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("blackduck").setLevel(logging.WARNING)

def check_report_status(bd_client, location, retries=args.retries):
    report_id = location.split("/")[-1]
    if retries:
        logging.debug(f"Checking generating report process status...")
        response = bd.session.get(location)
        report_status = response.json().get('status', 'Not Ready')
        if response.status_code == 200 and report_status == 'COMPLETED':
            logging.info(f"Report {report_id} is ready") 
        else:
            logging.debug("Report is not ready yet, waiting 5 seconds then checking again...")
            time.sleep(args.sleep_time)
            retries -= 1
            check_report_status(bd_client, location, retries)
    else:
        logging.info(f"report {report_id} is still not generated")

with open(args.token_file, 'r') as tf:
    access_token = tf.readline().strip()

bd = Client(base_url=args.bd_url, token=access_token, verify=args.verify)

params = {
    'q': [f"name:{args.project_name}"]
}
projects = [p for p in bd.get_resource('projects', params=params) if p['name'] == args.project_name]
assert len(projects) == 1, f"There should be one, and only one project named {args.project_name}. We found {len(projects)}"
project = projects[0]

params = {
    'q': [f"versionName:{args.version_name}"]
}
versions = [v for v in bd.get_resource('versions', project, params=params) if v['versionName'] == args.version_name]
assert len(versions) == 1, f"There should be one, and only one version named {args.version_name}. We found {len(versions)}"
version = versions[0]

logging.debug(f"Found {project['name']}:{version['versionName']}")


#
# Generate SBOM report from BD server
#
post_data = {
        'reportFormat': args.format,
        'reportType': 'SBOM',
        'sbomType': args.type,	
}
sbom_reports_url = version['_meta']['href'] + "/sbom-reports"

r = bd.session.post(sbom_reports_url, json=post_data)
r.raise_for_status()
location = r.headers.get('Location')
logging.debug(f"POST request {location}")
logging.debug(f"payload {post_data}")

check_report_status(bd, location)
logging.info(f"Created SBOM report of type {args.type} and format {args.format} for project {args.project_name}, version {args.version_name} at location {location}")
 