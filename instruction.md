There's an Apache-style access log at /app/access.log. Parse it and write a summary
report to /app/report.json as a single JSON object with exactly these fields:

1. The file /app/report.json exists and contains a valid JSON object.
2. "total_requests" (integer) equals the total number of log lines in /app/access.log.
3. "unique_ips" (integer) equals the number of distinct client IP addresses that
   appear in /app/access.log.
4. "top_path" (string) equals the request path (e.g. "/index.html") that appears
   most often across all requests in /app/access.log. If multiple paths are tied
   for the most requests, use whichever of them appears first in the file.
