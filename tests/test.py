import unittest
import subprocess


class WikipediaPlagiariserTests(unittest.TestCase):

  def get_program_output(self, *args: str) -> tuple[str]:
    result = subprocess.run(
      executable='python',
      args=['python', 'main.py', *args],
      capture_output=True
    )

    return result.stdout, result.stderr


  def test_no_colour(self):
    output, error = self.get_program_output('201')
    self.assertEqual(output, b'\xf0\x9f\x94\x8d Results for "201"\x1b[0m\n\x1b[36m --------------------------------------------------\x1b[0m\n\x1b[92m\x1b[1m 201 - Created\x1b[0m\n\x1b[92m The request has been fulfilled, resulting in the creation of a new resource.\x1b[0m\n\n')
    self.assertEqual(error, b'')

    output, error = self.get_program_output('201', '--no-colour')
    self.assertEqual(output, b' Results for "201"\n --------------------------------------------------\n 201 - Created\n The request has been fulfilled, resulting in the creation of a new resource.\n\n')
    self.assertEqual(error, b'')

  def test_json(self):
    output, error = self.get_program_output('418')
    self.assertEqual(output, b'\xf0\x9f\x94\x8d Results for "418"\x1b[0m\n\x1b[36m --------------------------------------------------\x1b[0m\n\x1b[91m\x1b[1m 418 - I\'m a teapot\x1b[0m\n\x1b[91m This code was defined in 1998 as one of the traditional IETF April Fools\' jokes, in RFC 2324, Hyper Text Coffee Pot Control Protocol, and is not expected to be implemented by actual HTTP servers. The RFC specifies this code should be returned by teapots requested to brew coffee. This HTTP status is used as an Easter egg in some websites, such as Google.com\'s \'I\'m a teapot\' easter egg. Sometimes, this status code is also used as a response to a blocked request, instead of the more appropriate 403 Forbidden.\x1b[0m\n\n')
    self.assertEqual(error, b'')

    output, error = self.get_program_output('201', '--no-colour', '--output-as-json')
    self.assertEqual(output, b'[\n  {\n    "code": "201",\n    "message": "Created",\n    "desc": "The request has been fulfilled, resulting in the creation of a new resource."\n  }\n]\n')
    self.assertEqual(error, b'')

  def test_json_indent(self):
    output, error = self.get_program_output('418')
    self.assertEqual(output, b'\xf0\x9f\x94\x8d Results for "418"\x1b[0m\n\x1b[36m --------------------------------------------------\x1b[0m\n\x1b[91m\x1b[1m 418 - I\'m a teapot\x1b[0m\n\x1b[91m This code was defined in 1998 as one of the traditional IETF April Fools\' jokes, in RFC 2324, Hyper Text Coffee Pot Control Protocol, and is not expected to be implemented by actual HTTP servers. The RFC specifies this code should be returned by teapots requested to brew coffee. This HTTP status is used as an Easter egg in some websites, such as Google.com\'s \'I\'m a teapot\' easter egg. Sometimes, this status code is also used as a response to a blocked request, instead of the more appropriate 403 Forbidden.\x1b[0m\n\n')
    self.assertEqual(error, b'')

    output, error = self.get_program_output('201', '--no-colour', '--output-as-json', '--indent-size', '1')
    self.assertEqual(output, b'[\n {\n  "code": "201",\n  "message": "Created",\n  "desc": "The request has been fulfilled, resulting in the creation of a new resource."\n }\n]\n')
    self.assertEqual(error, b'')

    output, error = self.get_program_output('201', '--no-colour', '--output-as-json', '--indent-size', '10')
    self.assertEqual(output, b'[\n          {\n                    "code": "201",\n                    "message": "Created",\n                    "desc": "The request has been fulfilled, resulting in the creation of a new resource."\n          }\n]\n')
    self.assertEqual(error, b'')

  def test_no_pretty(self):
    output, error = self.get_program_output('418')
    self.assertEqual(output, b'\xf0\x9f\x94\x8d Results for "418"\x1b[0m\n\x1b[36m --------------------------------------------------\x1b[0m\n\x1b[91m\x1b[1m 418 - I\'m a teapot\x1b[0m\n\x1b[91m This code was defined in 1998 as one of the traditional IETF April Fools\' jokes, in RFC 2324, Hyper Text Coffee Pot Control Protocol, and is not expected to be implemented by actual HTTP servers. The RFC specifies this code should be returned by teapots requested to brew coffee. This HTTP status is used as an Easter egg in some websites, such as Google.com\'s \'I\'m a teapot\' easter egg. Sometimes, this status code is also used as a response to a blocked request, instead of the more appropriate 403 Forbidden.\x1b[0m\n\n')
    self.assertEqual(error, b'')

    output, error = self.get_program_output('201', '--no-colour', '--output-as-json', '--no-pretty')
    self.assertEqual(output, b'[{"code": "201", "message": "Created", "desc": "The request has been fulfilled, resulting in the creation of a new resource."}]\n')
    self.assertEqual(error, b'')

  def test_wildcard(self):
    output, error = self.get_program_output('x', '--no-colour', '--output-as-json', '--no-pretty')
    self.assertEqual(output, b'[{"code": "100", "message": "Continue", "desc": "The server has received the request headers and the client should proceed to send the request body (in the case of a request for which a body needs to be sent; for example, a POST request). Sending a large request body to a server after a request has been rejected for inappropriate headers would be inefficient. To have a server check the request\'s headers, a client must send Expect: 100-continue as a header in its initial request and receive a 100 Continue status code in response before sending the body. If the client receives an error code such as 403 (Forbidden) or 405 (Method Not Allowed) then it should not send the request\'s body. The response 417 Expectation Failed indicates that the request should be repeated without the Expect header as it indicates that the server does not support expectations (this is the case, for example, of HTTP/1.0 servers)."}, {"code": "101", "message": "Switching Protocols", "desc": "The requester has asked the server to switch protocols and the server has agreed to do so."}, {"code": "102", "message": "Processing", "desc": "A WebDAV request may contain many sub-requests involving file operations, requiring a long time to complete the request. This code indicates that the server has received and is processing the request, but no response is available yet. This prevents the client from timing out and assuming the request was lost. The status code is deprecated."}, {"code": "103", "message": "Early Hints", "desc": "Used to return some response headers before final HTTP message."}, {"code": "200", "message": "OK", "desc": "Standard response for successful HTTP requests. The actual response will depend on the request method used. In a GET request, the response will contain an entity corresponding to the requested resource. In a POST request, the response will contain an entity describing or containing the result of the action."}, {"code": "201", "message": "Created", "desc": "The request has been fulfilled, resulting in the creation of a new resource."}, {"code": "202", "message": "Accepted", "desc": "The request has been accepted for processing, but the processing has not been completed. The request might or might not be eventually acted upon, and may be disallowed when processing occurs."}, {"code": "203", "message": "Non-Authoritative Information (since HTTP/1.1)", "desc": "The server is a transforming proxy (e.g. a Web accelerator) that received a 200 OK from its origin, but is returning a modified version of the origin\'s response."}, {"code": "204", "message": "No Content", "desc": "The server successfully processed the request, and is not returning any content."}, {"code": "205", "message": "Reset Content", "desc": "The server successfully processed the request, asks that the requester reset its document view, and is not returning any content."}, {"code": "206", "message": "Partial Content", "desc": "The server is delivering only part of the resource (byte serving) due to a range header sent by the client. The range header is used by HTTP clients to enable resuming of interrupted downloads, or split a download into multiple simultaneous streams."}, {"code": "207", "message": "Multi-Status", "desc": "The message body that follows is by default an XML message and can contain a number of separate response codes, depending on how many sub-requests were made."}, {"code": "208", "message": "Already Reported", "desc": "The members of a DAV binding have already been enumerated in a preceding part of the (multistatus) response, and are not being included again."}, {"code": "226", "message": "IM Used", "desc": "The server has fulfilled a request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance."}, {"code": "300", "message": "Multiple Choices", "desc": "Indicates multiple options for the resource from which the client may choose (via agent-driven content negotiation). For example, this code could be used to present multiple video format options, to list files with different filename extensions, or to suggest word-sense disambiguation."}, {"code": "301", "message": "Moved Permanently", "desc": "This and all future requests should be directed to the given URI."}, {"code": "302", "message": "Found (Previously \'Moved temporarily\')", "desc": "Tells the client to look at (browse to) another URL. The HTTP/1.0 specification required the client to perform a temporary redirect with the same method (the original describing phrase was \'Moved Temporarily\'), but popular browsers implemented 302 redirects by changing the method to GET. Therefore, HTTP/1.1 added status codes 303 and 307 to distinguish between the two behaviours."}, {"code": "303", "message": "See Other (since HTTP/1.1)", "desc": "The response to the request can be found under another URI using the GET method. When received in response to a POST (or PUT/DELETE), the client should presume that the server has received the data and should issue a new GET request to the given URI."}, {"code": "304", "message": "Not Modified", "desc": "Indicates that the resource has not been modified since the version specified by the request headers If-Modified-Since or If-None-Match. In such case, there is no need to retransmit the resource since the client still has a previously-downloaded copy."}, {"code": "305", "message": "Use Proxy (since HTTP/1.1)", "desc": "The requested resource is available only through a proxy, the address for which is provided in the response. For security reasons, many HTTP clients (such as Mozilla Firefox and Internet Explorer) do not obey this status code."}, {"code": "306", "message": "Switch Proxy", "desc": "No longer used. Originally meant \'Subsequent requests should use the specified proxy.\'"}, {"code": "307", "message": "Temporary Redirect (since HTTP/1.1)", "desc": "In this case, the request should be repeated with another URI; however, future requests should still use the original URI. In contrast to how 302 was historically implemented, the request method is not allowed to be changed when reissuing the original request. For example, a POST request should be repeated using another POST request."}, {"code": "308", "message": "Permanent Redirect", "desc": "This and all future requests should be directed to the given URI. 308 parallel the behaviour of 301, but does not allow the HTTP method to change. So, for example, submitting a form to a permanently redirected resource may continue smoothly."}, {"code": "400", "message": "Bad Request", "desc": "The server cannot or will not process the request due to an apparent client error (e.g., malformed request syntax, size too large, invalid request message framing, or deceptive request routing)."}, {"code": "401", "message": "Unauthorized", "desc": "Similar to 403 Forbidden, but specifically for use when authentication is required and has failed or has not yet been provided. The response must include a WWW-Authenticate header field containing a challenge applicable to the requested resource. See Basic access authentication and Digest access authentication. 401 semantically means \'unauthorised\', the user does not have valid authentication credentials for the target resource. Some sites incorrectly issue HTTP 401 when an IP address is banned from the website (usually the website domain) and that specific address is refused permission to access a website.[citation needed]"}, {"code": "402", "message": "Payment Required", "desc": "Reserved for future use. The original intention was that this code might be used as part of some form of digital cash or micropayment scheme, as proposed, for example, by GNU Taler, but that has not yet happened, and this code is not widely used. Google Developers API uses this status if a particular developer has exceeded the daily limit on requests. Sipgate uses this code if an account does not have sufficient funds to start a call. Shopify uses this code when the store has not paid their fees and is temporarily disabled. Stripe uses this code for failed payments where parameters were correct, for example blocked fraudulent payments."}, {"code": "403", "message": "Forbidden", "desc": "The request contained valid data and was understood by the server, but the server is refusing action. This may be due to the user not having the necessary permissions for a resource or needing an account of some sort, or attempting a prohibited action (e.g. creating a duplicate record where only one is allowed). This code is also typically used if the request provided authentication by answering the WWW-Authenticate header field challenge, but the server did not accept that authentication. The request should not be repeated."}, {"code": "404", "message": "Not Found", "desc": "The requested resource could not be found but may be available in the future. Subsequent requests by the client are permissible."}, {"code": "405", "message": "Method Not Allowed", "desc": "A request method is not supported for the requested resource; for example, a GET request on a form that requires data to be presented via POST, or a PUT request on a read-only resource."}, {"code": "406", "message": "Not Acceptable", "desc": "The requested resource is capable of generating only content not acceptable according to the Accept headers sent in the request. See Content negotiation."}, {"code": "407", "message": "Proxy Authentication Required", "desc": "The client must first authenticate itself with the proxy."}, {"code": "408", "message": "Request Timeout", "desc": "The server timed out waiting for the request. According to HTTP specifications: \'The client did not produce a request within the time that the server was prepared to wait. The client MAY repeat the request without modifications at any later time.\'"}, {"code": "409", "message": "Conflict", "desc": "Indicates that the request could not be processed because of conflict in the current state of the resource, such as an edit conflict between multiple simultaneous updates."}, {"code": "410", "message": "Gone", "desc": "Indicates that the resource requested was previously in use but is no longer available and will not be available again. This should be used when a resource has been intentionally removed and the resource should be purged. Upon receiving a 410 status code, the client should not request the resource in the future. Clients such as search engines should remove the resource from their indices. Most use cases do not require clients and search engines to purge the resource, and a \'404 Not Found\' may be used instead."}, {"code": "411", "message": "Length Required", "desc": "The request did not specify the length of its content, which is required by the requested resource."}, {"code": "412", "message": "Precondition Failed", "desc": "The server does not meet one of the preconditions that the requester put on the request header fields."}, {"code": "413", "message": "Payload Too Large", "desc": "The request is larger than the server is willing or able to process. Previously called \'Request Entity Too Large\'."}, {"code": "414", "message": "URI Too Long", "desc": "The URI provided was too long for the server to process. Often the result of too much data being encoded as a query-string of a GET request, in which case it should be converted to a POST request. Called \'Request-URI Too Long\' previously."}, {"code": "415", "message": "Unsupported Media Type", "desc": "The request entity has a media type which the server or resource does not support. For example, the client uploads an image as image/svg+xml, but the server requires that images use a different format."}, {"code": "416", "message": "Range Not Satisfiable", "desc": "The client has asked for a portion of the file (byte serving), but the server cannot supply that portion. For example, if the client asked for a part of the file that lies beyond the end of the file. Called \'Requested Range Not Satisfiable\' previously."}, {"code": "417", "message": "Expectation Failed", "desc": "The server cannot meet the requirements of the Expect request-header field."}, {"code": "418", "message": "I\'m a teapot", "desc": "This code was defined in 1998 as one of the traditional IETF April Fools\' jokes, in RFC 2324, Hyper Text Coffee Pot Control Protocol, and is not expected to be implemented by actual HTTP servers. The RFC specifies this code should be returned by teapots requested to brew coffee. This HTTP status is used as an Easter egg in some websites, such as Google.com\'s \'I\'m a teapot\' easter egg. Sometimes, this status code is also used as a response to a blocked request, instead of the more appropriate 403 Forbidden."}, {"code": "421", "message": "Misdirected Request", "desc": "The request was directed at a server that is not able to produce a response (for example because of connection reuse)."}, {"code": "422", "message": "Unprocessable Content", "desc": "The request was well-formed (i.e., syntactically correct) but could not be processed."}, {"code": "423", "message": "Locked", "desc": "The resource that is being accessed is locked."}, {"code": "424", "message": "Failed Dependency", "desc": "The request failed because it depended on another request and that request failed (e.g., a PROPPATCH)."}, {"code": "425", "message": "Too Early", "desc": "Indicates that the server is unwilling to risk processing a request that might be replayed."}, {"code": "426", "message": "Upgrade Required", "desc": "The client should switch to a different protocol such as TLS/1.3, given in the Upgrade header field."}, {"code": "428", "message": "Precondition Required", "desc": "The origin server requires the request to be conditional. Intended to prevent the \'lost update\' problem, where a client GETs a resource\'s state, modifies it, and PUTs it back to the server, when meanwhile a third party has modified the state on the server, leading to a conflict."}, {"code": "429", "message": "Too Many Requests", "desc": "The user has sent too many requests in a given amount of time. Intended for use with rate-limiting schemes."}, {"code": "431", "message": "Request Header Fields Too Large", "desc": "The server is unwilling to process the request because either an individual header field, or all the header fields collectively, are too large."}, {"code": "451", "message": "Unavailable For Legal Reasons", "desc": "A server operator has received a legal demand to deny access to a resource or to a set of resources that includes the requested resource. The code 451 was chosen as a reference to the novel Fahrenheit 451 (see the Acknowledgements in the RFC)."}, {"code": "500", "message": "Internal Server Error", "desc": "A generic error message, given when an unexpected condition was encountered and no more specific message is suitable."}, {"code": "501", "message": "Not Implemented", "desc": "The server either does not recognize the request method, or it lacks the ability to fulfil the request. Usually this implies future availability (e.g., a new feature of a web-service API)."}, {"code": "502", "message": "Bad Gateway", "desc": "The server was acting as a gateway or proxy and received an invalid response from the upstream server."}, {"code": "503", "message": "Service Unavailable", "desc": "The server cannot handle the request (because it is overloaded or down for maintenance). Generally, this is a temporary state."}, {"code": "504", "message": "Gateway Timeout", "desc": "The server was acting as a gateway or proxy and did not receive a timely response from the upstream server."}, {"code": "505", "message": "HTTP Version Not Supported", "desc": "The server does not support the HTTP version used in the request."}, {"code": "506", "message": "Variant Also Negotiates (RFC 2295)", "desc": "Transparent content negotiation for the request results in a circular reference."}, {"code": "507", "message": "Insufficient Storage (WebDAV; RFC 4918)", "desc": "The server is unable to store the representation needed to complete the request."}, {"code": "508", "message": "Loop Detected (WebDAV; RFC 5842)", "desc": "The server detected an infinite loop while processing the request (sent instead of 208 Already Reported)."}, {"code": "510", "message": "Not Extended (RFC 2774)", "desc": "Further extensions to the request are required for the server to fulfil it."}, {"code": "511", "message": "Network Authentication Required (RFC 6585)", "desc": "The client needs to authenticate to gain network access. Intended for use by intercepting proxies used to control access to the network (e.g., \'captive portals\' used to require agreement to Terms of Service before granting full Internet access via a Wi-Fi hotspot)."}]\n')
    self.assertEqual(error, b'')



if __name__ == '__main__':
  unittest.main()