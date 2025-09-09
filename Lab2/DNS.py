import dns.resolver

def dns_lookup():
    try:
        d = "example.com"
        f = open("dns.txt", "w")

        for r in dns.resolver.resolve(d, "A"): f.write(str(r)+"\n")
        for r in dns.resolver.resolve(d, "MX"): f.write(str(r)+"\n")
        try:
            for r in dns.resolver.resolve(d, "CNAME"): f.write(str(r)+"\n")
        except: f.write("No CNAME\n")

        f.close()
        print("Saved to dns.txt")
    except Exception as e:
        print("Error:", e)

dns_lookup()
