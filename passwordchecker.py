import requests
import hashlib

def request_api_data(query_char):
  url = 'https://api.pwnedpasswords.com/range/' + query_char
  res = requests.get(url)
  if res.status_code != 200:
    raise RuntimeError(f"Error fetching: {res.status_code}, check the API and try again")
  return res

def read_response(res, tail):
  hashes = [line.split(":") for line in res.text.splitlines()]
  for h, count in hashes:
    if h == tail:
      return count
  return 0

def pwned_api_check(password):
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
  first_five, tail = sha1password[:5], sha1password[5:]
  response = request_api_data(first_five)
  return read_response(response, tail)

def read_file(password=None, file_loc=None):
  if file_loc:
    f = open(file_loc, "r")
    for password in f.read().split():
      count = pwned_api_check(password)
      if count:
        return f"Your {'*'*len(password)} was found {count} times...It's risky to use :("
      else:
        return f"Your {'*'*len(password)} was NOT FOUND. That's amazing. Congratulations... :)"
    f.close()
  else:
    count = pwned_api_check(password)
    if count:
      return f"Your {'*'*len(password)} was found {count} times...It's risky to use :("
    else:
      return f"Your {'*'*len(password)} was NOT FOUND. That's amazing. Congratulations... :)"


