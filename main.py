
import subprocess #allows to spawn new processes, connect to their input/output/error pipes and obtain return codes
import optparse #module for parsing command-line options, generates usage and help messages
import re #regular expression operations module

def get_arguments():#parse the user input and return the arguments and values entered by user.
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")#help options
    parser.add_option("-m", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()#values entered by the user
    if not options.interface:#if user didn't put a value for interface
        parser.error("[-] No value for interface (eth0, wlan0, lo), use --help for more info.")
    elif not options.new_mac:#if user didn't enter a value for MAC address
        parser.error("[-] You didn't set up mac correctly, use --help for more info.")
    return options#if reaches through if statements, returns options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def current_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    regular_expression_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    #returns the "ifconfig" command's mac address. If there's not a mac address, prints "Unable to read MAC address"
    if regular_expression_result:
        return regular_expression_result.group(0)
    else:
        print("[-] Unable to read MAC address.")






options = get_arguments()#capture the value of options (returns from the get arguments)

current_mac = current_mac_address(options.interface) #Get's the current mac address
print("Mac address is : " + str(current_mac)) #prints to terminal as a string .

change_mac(options.interface, options.new_mac)#calls change_mac function and executes all commands in it.

current_mac = current_mac_address(options.interface)
if current_mac == options.new_mac:
    print("[+] Mac was changed. New mac is: " + current_mac)
else:
    print("[+] Unable to change mac address")
