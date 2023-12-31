#!/usr/bin/python
from boofuzz import *
import time

# Boofuzz template modified from https://github.com/philkeeble

# Function for grabbing the banner each time it connects
def get_banner(target, my_logger, session, *args, **kwargs):
  # Set the function banner_template as the string we expect to see on connection
  banner_template = b"Welcome to Vulnerable Server! Enter HELP for help."
  try:
    # Recieve buffer from the target
    banner = target.recv(10000)
  except:
    # If nothing recieved from the target, print and exit
    print("Unable to connect. Target is down. Exiting.")
    exit(1)

  # Printing to our log to let us know its recieving something
  my_logger.log_check('Receiving banner..')
  # Check that what we recieved contains the string we expected
  if banner_template in banner:
    my_logger.log_pass('banner received')
  else:
    # If it doesn't contain the string we expected, fail and exit
    my_logger.log_fail('No banner received')
    print("No banner received, exiting..")
    exit(1)

# Main function
def main():

  # This is a boofuzz standard piece of code and is on their docs as a template
  session = Session(
	sleep_time=1,
    target=Target(
      # This sets the connection host and port for vulnserver
      connection=SocketConnection("10.0.2.15", 9999, proto='tcp')
    ),
  )

  # Setup request
  s_initialize(name="Request")
  with s_block("Host-Line"):
    # Send TRUN command to vulnserver
    s_static("TRUN", name='command name')
    # Add a space after TRUN
    s_delim(" ")
    # After TRUN and the space, add the fuzzing payloads
    s_string("FUZZ",  name='trun variable content')
    # Add a new line after the fuzzing payload (so that it sends)
    s_delim("\r\n")

  # Fuzzing
  session.connect(s_get("Request"), callback=get_banner)
  session.fuzz()

# Calls main
if __name__ == "__main__":
	main()
