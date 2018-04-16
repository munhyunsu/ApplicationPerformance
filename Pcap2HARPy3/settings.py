pages = True

# bodies of http responses, that is
drop_bodies = False

# Whether HTTP parsing should case whether the content length matches the
# content-length header.
strict_http_parse_body = False

# Whether to pad missing data in TCP flows with 0 bytes
pad_missing_tcp_data = False

# Whether to keep requests with missing responses. Could break consumers
# that assume every request has a response.
keep_unfulfilled_requests = False
