import requests

def get_ip_info(ip_address, api_key):
    url = f"https://ipinfo.io/{ip_address}/json?token={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'bogon' in data:
            return "Invalid or private IP address."
        
        asn_info = data.get("asn", {})
        asn_domain = asn_info.get("domain", "N/A")
        
        ip_info = {
            "IP": ip_address,
            "City": data.get("city", "N/A"),
            "Region": data.get("region", "N/A"),
            "Country": data.get("country", "N/A"),
            "ASN Domain": asn_domain
        }
        
        return ip_info
    
    except Exception as e:
        return f"Error retrieving data: {e}"

def run():
    ask=input("give me the file: ")
    api_key = "6c183ccb81af52"  
    with open(ask, "r") as f:
        for line in f:
            ip_address = line.strip() 
            if ip_address:
                ip_info = get_ip_info(ip_address, api_key)
                print(f"Processing IP: {ip_address}")

                if isinstance(ip_info, dict):
                    with open("file.txt", "a",encoding="utf-8") as output_file:
                        for key, value in ip_info.items():
                            output_file.write(f"{key}: {value}\n")
                        output_file.write("\n\n")
                else:
                    with open("file.txt", "a",encoding="utf-8") as output_file:
                        output_file.write(f"Error for IP {ip_address}: {ip_info}\n")
                        output_file.write("\n\n")

run()
