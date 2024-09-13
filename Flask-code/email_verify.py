import smtplib
import dns.resolver


class VerifyEmail:
    def email_verify_smtp(self, em):
        try:
            # Extract domain from the email address
            domain = em.split('@')[1]

            # Perform DNS MX lookup for the domain
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_record = str(mx_records[0].exchange)

            # Set up an SMTP connection
            server = smtplib.SMTP(timeout=10)
            server.set_debuglevel(0)  # Set to 1 for detailed debugging info

            # Connect to the mail server using the first MX record
            server.connect(mx_record)
            server.helo(server.local_hostname)  # Handshake step
            server.mail('noreply@example.com')  # Use a valid sender email for handshake
            code, message = server.rcpt(em)  # Verify if the recipient exists
            server.quit()

            # Return True if the server returns a 250 code, meaning success
            if code == 250:
                return True
            else:
                return False

        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            domain = em.split('@')[1]
            print(f"Domain '{domain}' does not exist or no MX record found.")
            return False

        except smtplib.SMTPServerDisconnected:
            print("Failed to connect to the email server.")
            return False

        except Exception as e:
            print(f"An error occurred: {e}")
            return False


# Example usage:
verifier = VerifyEmail()
email = "prayeshgodhani.aids21@scet.ac.in"  # Replace with the email you want to verify
is_valid = verifier.email_verify_smtp(email)

if is_valid:
    print(f"The email '{email}' is valid.")
else:
    print(f"The email '{email}' is invalid.")
