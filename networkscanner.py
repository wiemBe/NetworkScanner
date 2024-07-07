from scapy.all import srp, Ether, ARP 
from rich.live import Live
from rich.table import Table

def ScanNetwork(IpRange):
    ARPRequest = ARP(pdst=IpRange)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / ARPRequest
    result = srp(packet, timeout=4, verbose=False)[0]
    devices = []
    
    for sent, received in result:
        devices.append({"ip":received.psrc, "mac":received.hwsrc})
    
    return devices


if __name__ =="__main__":
        print("sometimes it doesn't shows all ip address's wait just couple of secs to refresh")
        deviceMacList=[]
        deviceIpList=[]
        table = Table()
        table.add_column("IP")
        table.add_column("Mac Address")
        

        KeyboardInput = "R"
        while KeyboardInput.capitalize() == "R":
            with Live(table, refresh_per_second=1):  # update 4 times a second to feel fluid
                IpRange = "192.168.1.0/24" 
                devices = ScanNetwork(IpRange)
                seen_ips = set()
                unique_devices = [device for device in devices if device['ip'] not in seen_ips and not seen_ips.add(device['ip'])]
                for device in unique_devices:
                    table.add_row(f"{device["ip"]}", f"{device["mac"]} ")
            KeyboardInput = input("for refresh press R if you wanna exit press q: ")

        if KeyboardInput.capitalize() =="Q":
            print("exiting")

           