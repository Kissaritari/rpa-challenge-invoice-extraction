variant = r'(?P<variant>^\w+)'
aenean = {
    "InvoiceDate": r'(?P<InvoiceDate>\d{4}-[01]?\d-[0-3]?\d)',
    "CompanyName": r'(?P<CompanyName>^[a-z]* LLC)',
    "InvoiceNro": r'# ?(?P<InvoiceNo>\d*)',
    "TotalDue": r"^Total:? \D?(?P<TotalDue>\d*[0-9.,]*)$"
}
sit_amet = {
    "InvoiceDate": r'(?P<InvoiceDate>\w+ [0-3]?\d, \d{4})',
    "CompanyName": r'(?P<CompanyName>^\w+ \D+ Corp.$)',
    "InvoiceNo": r'# ?(?P<InvoiceNo>\d*)',
    "TotalDue": r"^Total:? \D?(?P<TotalDue>\d*[0-9.,]*)$"
}
