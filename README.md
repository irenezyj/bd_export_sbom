# Synopsys Black Duck - bd_export_sbom.py version 1.0

This script is for generating SBOM report (SPDX2.2, CycloneDX 1.3, CycloneDX 1.4) from blackduck server

# OVERVIEW

This script is provided under an OSS license (specified in the LICENSE file) to allow users to export SBOM reports in various formats from Black Duck projects.

If you have comments or issues, please raise a GitHub issue here. Synopsys support is not able to respond to support tickets for this OSS utility.

# DESCRIPTION

The script is designed to export SBOM reports from a Black Duck project.

It relies on the Black Duck `hub-rest-api-python` package to access the Black Duck APIs (see prerequisites below to install and configure this package).

The project name and version need to be specified. If the project name is not matched in the server then the list of projects matching the supplied project string will be displayed (and the script will terminate). If the version name is not matched for the specified project, then the list of all versions will be displayed  (and the script will terminate).

The output file in SPDX report (JSON, YAML, RDF, TAGVALUE) or CycloneDX report (JSON). format can optionally be specified; the project name and version name with corresponding extension will be used for the default filename if nor specified. If the output file already exists, it will be renamed using a numeric extension (for example `.001`).


Other options can be specified to reduce the number of API calls to speed up script execution.


# PREREQUISITES

1. Pip 3 must be installed.

1. Set the BLACKDUCK_URL and BLACKDUCK_API_TOKEN environment variables to connect to the Black Duck server (alternatively use the `--blackduck_url` and `--blackduck_api_token` options)

# INSTALLATION

Install the package using the command:

        pip3 install bd-export-sbom

# USAGE

The program can be invoked as follows:

       usage: bd-export-spdx [-h] [-v] [-o OUTPUT] [-r] [--download_loc] [--no_copyrights] [--no_files] [-b] [--blackduck_url BLACKDUCK_URL]
                               [--blackduck_api_token BLACKDUCK_API_TOKEN] [--blackduck_trust_certs]
                               project_name project_version

       Export SPDX JSON format file for the given project and version

       positional arguments:
         project_name          Black Duck project name
         project_version       Black Duck version name

       other arguments:
         --blackduck_url BLACKDUCK_URL
                               Black Duck server URL including https://
         --blackduck_api_token BLACKDUCK_API_TOKEN
                               Black Duck API token
         --blackduck_trust_certs
                               Trust Black Duck server certificates if unsigned
         -h, --help            show this help message and exit
         -v, --version         Print script version and exit
         -t, --type            SBOM report type ["SPDX_22", "CYCLONEDX_13", "CYCLONEDX_14"]
         -f, --format          Report format SPDX ["JSON", "YAML", "RDF", "TAGVALUE"], CycloneDx ["JSON"] (default = JSON)
         -r, --retries,        How many times to retry checking report status (default = 10)
         -s, --sleep_time,     The amount of time to sleep in-between (re-)tries to check report status (default=5)
         --debug               Add reporting of processed components

If `project_name` does not match a single project then all matching projects will be listed and the script will terminate.

If `version` does not match a single project version then all matching versions will be listed and the script will terminate.

The script will use the environment variables BLACKDUCK_URL and BLACKDUCK_API_TOKEN if they are set. Alternatively use the options `--blackduck_url` and `--blackduck_api_token` to specify them on the command line.

Use the `--blackduck_trust_certs` option to trust the SSL certificate on the Black Duck server if unsigned.

The `--output out_file` or `-o out_file` option specifies the output file. If this file already exists, the previous version will be renamed with a unique number (e.g. .001). The default file name `<project>-<version>.spdx` will be used if not specified.


# PACKAGE SUPPLIER NAME CONFIGURATION

For custom components in the BOM, users will need to manually populate this.
Create a custom fields for 'BOM Component' entries with name 'PackageSupplier' and type 'Text'.
Updating the custom field for custom (or KB) components will replace the value in the output SPDX file.
