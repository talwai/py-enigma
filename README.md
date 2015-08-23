### Py-enigma

Py-enigma is a simple Python client for the [enigma.io API](https://app.enigma.io/api). Enigma is a service that allows users to
> quickly search and analyze billions of public records published by governments, companies and organizations.

The Py-enigma client supports the Metadata, Data, Stats and Export API endpoints.

#### Support
The `py-enigma` client support Python 2.7+ and Python 3.3+. The client may not behave as expected in other versions of Python

#### Installation
`pip install py-enigma`

```
>>> import enigma
>>> enigma.__version__
'0.1.0'
```

#### How-tos
You must authenticate using your Enigma.io API key before you can make requests against the API.
```
ENIGMA_API_KEY = "my_api_key"
client = enigma.Client(ENIGMA_API_KEY)
```

##### Metadata
```
>>> datapath = "us.gov.whitehouse.visitor-list"
>>> params = {"search": "john", "select": ["namefull", "appt_made_date"], "limit": 20}
>>> result = client.Metadata.query(datapath, params)
>>> type(result)
<class 'enigma.Metadata'>
>>> result.datapath, result.info, result.result
```

##### Data
```
>>> datapath = "us.gov.whitehouse.visitor-list"
>>> params = {"search": "john", "select": ["namefull", "appt_made_date"], "limit": 20}
>>> result = client.Data.query(datapath, params)
>>> type(result)
<class 'enigma.Data'>
>>> result.datapath, result.info, result.result
```

##### Stats
```
>>> datapath = "us.gov.whitehouse.visitor-list"
>>> params = {"search": "john", "select": ["namefull", "appt_made_date"], "limit": 20}
>>> result = client.Stats.query(datapath, params)
>>> type(result)
<class 'enigma.Stats'>
>>> result.datapath, result.info, result.result
```

##### Exports
```
>>> datapath = "us.gov.whitehouse.visitor-list"
>>> params = {"search": "john", "select": ["namefull", "appt_made_date"], "limit": 20}
>>> result = client.ExportRequest.new(datapath, params).wait()
>>> type(result)
<class 'enigma.ExportRequest'>
>>> result.export_url
https://enigma-api-export.s3.amazonaws.com/enigma-us.gov.whitehouse.visitor-list-2ed4528c65781e70692ce73ce34b17cd.csv.gz?Expires=REDACTED&AWSAccessKeyId=REDACTED&Signature=REDACTED
>>> result.ready
False
>>> result.wait() # Blocking call that waits for the export file to be ready for download
>>> result.ready
True
>>> result.export_url # Now points to a file ready for download
https://enigma-api-export.s3.amazonaws.com/enigma-us.gov.whitehouse.visitor-list-2ed4528c65781e70692ce73ce34b17cd.csv.gz?Expires=REDACTED&AWSAccessKeyId=REDACTED&Signature=REDACTED
```
