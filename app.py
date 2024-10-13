from flask import Flask, render_template, request, redirect, url_for
from netmiko import ConnectHandler
import time
import threading

app = Flask(__name__)

# เก็บข้อมูลการเชื่อมต่อ SSH
net_connect = None

def get_hostname():
    global net_connect
    try:
        output = net_connect.send_command("show running-config")
        print("Output of show running-config:")
        print(output)  # แสดงผลลัพธ์ใน console
        lines = output.splitlines()
        hostname_line = next((line for line in lines if line.startswith("hostname")), None)
        hostname = hostname_line.split()[-1] if hostname_line else "Unknown"
        return hostname
    except Exception as e:
        print(f"Error getting hostname: {e}")
        return "Unknown"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    global net_connect
    ip = request.form['ip']
    username = request.form['username']
    password = request.form['password']
    
    router = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
        'secret': password,
    }

    try:
        net_connect = ConnectHandler(**router)
        net_connect.enable()
        
        # ดึง hostname จากเราเตอร์
        hostname = get_hostname()  # เรียกใช้ฟังก์ชันนี้เพื่อดึง hostname
        prompt = net_connect.find_prompt()

        # ส่ง hostname ไปยังหน้า command_center.html
        return render_template('command_center.html', output="", prompt=prompt, hostname=hostname)
    except Exception as e:
        return f'<h1>Error Connecting to Device: {str(e)}</h1>'

@app.route('/run_command', methods=['POST'])
def run_command():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    
    command = request.form['command']
    try:
        output = net_connect.send_command(command)
        prompt = net_connect.find_prompt()
        return render_template('command_center.html', output=output, prompt=prompt)
    except Exception as e:
        return f'<h1>Error Running Command</h1><p>{str(e)}</p>'

@app.route('/show_version', methods=['POST'])
def show_version():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1><p>Please connect first.</p>'

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    try:
        output = net_connect.send_command('show version')
        prompt = net_connect.find_prompt()
        return render_template('show_commands.html', output=output, prompt=prompt,hostname=hostname)
    except Exception as e:
        return f'<h1>Error Showing Version</h1><p>{str(e)}</p>'

@app.route('/show_running_config', methods=['POST'])
def show_running_config():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    try:
        output = net_connect.send_command('show running-config')
        prompt = net_connect.find_prompt()
        return render_template('show_commands.html', output=output, prompt=prompt,hostname=hostname)
    except Exception as e:
        return f'<h1>Error Showing Running Config</h1><p>{str(e)}</p>'

@app.route('/show_startup_config', methods=['POST'])
def show_startup_config():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        output = net_connect.send_command('show startup-config')
        prompt = net_connect.find_prompt()
        return render_template('show_commands.html', output=output, prompt=prompt, hostname=hostname)
    except Exception as e:
        return f'<h1>Error Showing Startup Config</h1><p>{str(e)}</p>'

@app.route('/show_ip_interface_brief', methods=['POST'])
def show_ip_interface_brief():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    if not net_connect:
        return redirect(url_for('index'))
    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        output = net_connect.send_command('show ip interface brief')
        prompt = net_connect.find_prompt()
        return render_template('show_commands.html', output=output, prompt=prompt, hostname=hostname)
    except Exception as e:
        return f'<h1>Error Showing IP Interface Brief</h1><p>{str(e)}</p>'

@app.route('/show_interfaces', methods=['POST'])
def show_interfaces():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    try:
        output = net_connect.send_command('show interfaces')
        prompt = net_connect.find_prompt()
        return render_template('show_commands.html', output=output, prompt=prompt, hostname=hostname)
    except Exception as e:
        return f'<h1>Error Showing Interfaces</h1><p>{str(e)}</p>'

@app.route('/show_ip_route', methods=['POST'])
def show_ip_route():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        output = net_connect.send_command('show ip route')
        prompt = net_connect.find_prompt()
        return render_template('show_commands.html', output=output, prompt=prompt,hostname=hostname)
    except Exception as e:
        return f'<h1>Error Showing IP Route</h1><p>{str(e)}</p>'

# เพิ่มคำสั่ง "show" ใหม่ที่เหลือ
@app.route('/show_arp', methods=['POST'])
def show_arp():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    output = net_connect.send_command('show arp')
    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    return render_template('show_commands.html', output=output,hostname=hostname)

@app.route('/show_protocols', methods=['POST'])
def show_protocols():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    output = net_connect.send_command('show protocols')
    return render_template('show_commands.html', output=output, hostname=hostname)

@app.route('/show_clock', methods=['POST'])
def show_clock():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    output = net_connect.send_command('show clock')
    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    return render_template('show_commands.html', output=output, hostname=hostname)

@app.route('/show_users', methods=['POST'])
def show_users():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    output = net_connect.send_command('show users')

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    return render_template('show_commands.html', output=output, hostname=hostname)

@app.route('/show_history', methods=['POST'])
def show_history():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    output = net_connect.send_command('show history')

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    return render_template('show_commands.html', output=output,hostname=hostname)

@app.route('/show_vlan_brief', methods=['POST'])
def show_vlan_brief():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    
    # ใช้คำสั่ง show version เพื่อตรวจสอบว่าเป็น Router หรือ Switch
    version_output = net_connect.send_command('show version')

    # ตรวจสอบว่าผลลัพธ์มีคำว่า 'vios_l2' ซึ่งบ่งบอกว่าเป็น Switch
    if 'vios_l2' in version_output:
        # ถ้าเป็น Switch ให้แสดงผลลัพธ์ของคำสั่ง show vlan brief
        output = net_connect.send_command('show vlan brief')
    else:
        # ถ้าไม่ใช่ Switch ให้แสดงข้อความว่าไม่ใช่ Switch
        output = 'You are not connected to a Switch. VLAN information is not available.'

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    return render_template('show_commands.html', output=output,hostname=hostname)

@app.route('/back', methods=['POST'])
def back():
    return redirect(url_for('command_center'))

@app.route('/command_center')
def command_center():
    global net_connect
    if not net_connect:
        return redirect(url_for('index'))

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    return render_template('command_center.html', output="", hostname=hostname)


@app.route('/show_commands', methods=['GET'])
def show_commands():
    global net_connect
    if not net_connect:
        return redirect(url_for('index'))

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    return render_template('show_commands.html', output="", hostname=hostname)

@app.route('/all_config', methods=['GET'])
def all_config():
    global net_connect
    if not net_connect:
        return redirect(url_for('index'))

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    return render_template('all_config.html', output="", hostname=hostname)

def erase_and_reload_router():
    """ฟังก์ชันนี้ทำงานใน Background เพื่อ Erase และ Reload Router"""
    global net_connect
    try:
        output = net_connect.send_command_timing('write erase')
        time.sleep(2)

        if 'Erasing the nvram filesystem' in output or 'Continue? [confirm]' in output:
            output += net_connect.send_command_timing('\n')
            time.sleep(2)

        reload_output = net_connect.send_command_timing('reload')
        time.sleep(2)

        if 'System configuration has been modified. Save? [yes/no]:' in reload_output:
            reload_output += net_connect.send_command_timing('no\n')
            time.sleep(2)

        if 'Proceed with reload' in reload_output or 'confirm' in reload_output:
            reload_output += net_connect.send_command_timing('y\n')
            time.sleep(2)
            reload_output += "\nConfiguration erased and router is reloading...\n"
        else:
            reload_output += "\nReload command failed due to restrictions on Telnet/SSH sessions.\n"
            reload_output += "Please manually reload the router using the console connection."

        print(output + reload_output)  # Log output สำหรับ debugging
    except Exception as e:
        print(f"Error during erase/reload: {str(e)}")
    finally:
        net_connect.disconnect()
        net_connect = None

@app.route('/erase_router', methods=['POST'])
def erase_router():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    threading.Thread(target=erase_and_reload_router).start()
    return render_template('all_config.html', 
                           output="Erase command sent. Router is reloading...")

@app.route('/apply_router_interface_config', methods=['POST'])
def apply_router_interface_config():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    
    interface = request.form['interface']
    ip_address = request.form['ip_address']
    subnet_mask = request.form['subnet_mask']
    
    commands = [
        f"interface {interface}",
        "no ip address",  # ลบ IP เดิม (ถ้ามี)
        f"ip address {ip_address} {subnet_mask}",
        "no shutdown",
        "exit",
    ]
    try:
        interfaces = get_interfaces() 
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        output = net_connect.send_config_set(commands)
        prompt = net_connect.find_prompt()
        return render_template('conf_router.html', output=output, prompt=prompt, hostname=hostname,interfaces=interfaces)
    except Exception as e:
        return f'<h1>Error Applying Router Interface Config</h1><p>{str(e)}</p>'


@app.route('/apply_switch_interface_config', methods=['POST'])
def apply_switch_interface_config():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    
    interface = request.form['interface']
    ip_address = request.form['ip_address']
    subnet_mask = request.form['subnet_mask']
    
    commands = [
        f"interface {interface}",
        "no switchport",  # Remove switchport to enable IP
        f"ip address {ip_address} {subnet_mask}",
        "no shutdown",
        "exit"
    ]
    try:
        interfaces = get_interfaces() 
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    try:
        output = net_connect.send_config_set(commands)
        prompt = net_connect.find_prompt()
        return render_template('conf_switch.html', output=output, prompt=prompt,hostname=hostname,interfaces=interfaces)
    except Exception as e:
        return f'<h1>Error Applying Switch Interface Config</h1><p>{str(e)}</p>'


@app.route('/remove_router_ip_interface', methods=['POST'])
def remove_router_ip_interface():
    """ลบ IP Address ออกจากอินเทอร์เฟซของ Router"""
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    interface = request.form['interface']

    commands = [
        f"interface {interface}",
        "no ip address",  # ลบ IP address
        "exit"
    ]
    try:
        hostname = get_hostname()
        interfaces = get_interfaces() 
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        output = net_connect.send_config_set(commands)
        prompt = net_connect.find_prompt()
        return render_template('conf_router.html', output=output, prompt=prompt,hostname=hostname,interfaces=interfaces)
    except Exception as e:
        return f'<h1>Error Removing Router IP Address</h1><p>{str(e)}</p>'


@app.route('/remove_switch_ip_interface', methods=['POST'])
def remove_switch_ip_interface():
    """ลบ IP Address ออกจากอินเทอร์เฟซของ Switch"""
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    interface = request.form['interface']

    commands = [
        f"interface {interface}",
        "no ip address",  # ลบ IP address
        "exit"
    ]
    try:
        hostname = get_hostname()
        interfaces = get_interfaces() 
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    try:
        output = net_connect.send_config_set(commands)
        output += "\n" + net_connect.send_command(f"show ip interface brief | include {interface}")
        prompt = net_connect.find_prompt()
        return render_template('conf_switch.html', output=output, prompt=prompt,hostname=hostname, interfaces=interfaces)
    except Exception as e:
        return f'<h1>Error Removing Switch IP Address</h1><p>{str(e)}</p>'
    
@app.route('/ip_route')
def ip_route():
    global net_connect
    if not net_connect:
        return redirect(url_for('index'))

    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    return render_template('ip_route.html', hostname=hostname)

@app.route('/submit_ip_route', methods=['POST'])
def submit_ip_route():
    global net_connect  # Use the global connection established earlier
    if not net_connect:
        return '<h1>Not connected</h1>'  # Ensure we are connected to the device

    network = request.form['network']
    subnet_mask = request.form['subnet_mask']
    nexthop = request.form['nexthop']
    
    # สร้างคำสั่งสำหรับเพิ่ม route
    route_command = f"ip route {network} {subnet_mask} {nexthop}"

    output = ""

    try:
        # เข้าสู่โหมด configuration
        net_connect.config_mode()

        # ส่งคำสั่งไปยังอุปกรณ์
        output = net_connect.send_config_set(route_command)

        # ถ้าไม่มีข้อผิดพลาดเกิดขึ้น แสดงผลลัพธ์
        output = f"Route added: {network}/{subnet_mask} via {nexthop}\n{output}"

    except Exception as e:
        output = f"Failed to add route: {str(e)}"
    try:
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    return render_template('ip_route.html', output=output, hostname=hostname)

@app.route('/conf_router', methods=['GET'])
def conf_router():
    global net_connect
    if not net_connect:
        return redirect(url_for('index'))

    try:
        hostname = get_hostname()
        interfaces = get_interfaces()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี

    return render_template('conf_router.html', hostname=hostname, interfaces=interfaces)

@app.route('/conf_switch', methods=['GET'])
def conf_switch():
    global net_connect
    if not net_connect:
        return redirect(url_for('index'))

    try:
        vlan_ids = get_vlan_ids()
        hostname = get_hostname()
        interfaces = get_interfaces()  
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    return render_template('conf_switch.html', hostname=hostname, interfaces=interfaces,vlan_ids=vlan_ids)

@app.route('/add_vlan', methods=['POST'])
def add_vlan():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    vlan_id = request.form['vlan_id']
    vlan_name = request.form['vlan_name']
    interface = request.form['interface']

    commands = [
        f"vlan {vlan_id}",
        f"name {vlan_name}",
        "exit",
        f"interface {interface}",
        f"switchport access vlan {vlan_id}",
        "exit"
    ]
    try:
        vlan_ids = get_vlan_ids()
        interfaces = get_interfaces() 
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        # ส่งคำสั่งสำหรับเพิ่ม VLAN
        net_connect.send_config_set(commands)
        output = net_connect.send_config_set(commands)
        output += net_connect.send_command(f"show vlan brief | include {vlan_id}")
        prompt = net_connect.find_prompt()
        return render_template('conf_switch.html', output=output, prompt=prompt,hostname=hostname, interfaces=interfaces, vlan_ids=vlan_ids)
    except Exception as e:
        return f'<h1>Error Adding VLAN</h1><p>{str(e)}</p>'


@app.route('/remove_vlan', methods=['POST'])
def remove_vlan():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    
    vlan_id = request.form['vlan_id']
    
    commands = [
        f"no vlan {vlan_id}"
    ]
    try:
        vlan_ids = get_vlan_ids()
        interfaces = get_interfaces() 
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        output = net_connect.send_config_set(commands)
        output += net_connect.send_command(f"show vlan brief")
        prompt = net_connect.find_prompt()
        return render_template('conf_switch.html', output=output, prompt=prompt,hostname=hostname, interfaces=interfaces, vlan_ids=vlan_ids)
    except Exception as e:
        return f'<h1>Error Remove Vlan</h1><p>{str(e)}</p>'

@app.route('/add_ip_vlan', methods=['POST'])
def add_ip_vlan():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    vlan_id = request.form['vlan_id']
    ip_address = request.form['ip_address']
    subnet_mask = request.form['subnet_mask']

    commands = [
        f"interface vlan {vlan_id}",
        f"ip address {ip_address} {subnet_mask}",
        "no shutdown",
        "exit"
    ]
    try:
        vlan_ids = get_vlan_ids()
        interfaces = get_interfaces() 
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        output = net_connect.send_config_set(commands)
        output += net_connect.send_command(f"show ip interface brief | include Vlan{vlan_id}")
        prompt = net_connect.find_prompt()
        return render_template('conf_switch.html', output=output, prompt=prompt,hostname=hostname, interfaces=interfaces, vlan_ids=vlan_ids)
    except Exception as e:
        return f'<h1>Error Adding IP to VLAN</h1><p>{str(e)}</p>'

@app.route('/add_port_to_vlan', methods=['POST'])
def add_port_to_vlan():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'

    interface = request.form['interface']
    vlan_id = request.form['vlan_id']

    commands = [
        f"interface {interface}",
        f"switchport access vlan {vlan_id}",
        "no shutdown",
        "exit"
    ]
    try:
        vlan_ids = get_vlan_ids()
        interfaces = get_interfaces() 
        hostname = get_hostname()
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        output = net_connect.send_config_set(commands)
        output += net_connect.send_command(f"show vlan brief | include {vlan_id}")
        prompt = net_connect.find_prompt()
        return render_template('conf_switch.html', output=output, prompt=prompt,hostname=hostname, interfaces=interfaces, vlan_ids=vlan_ids)
    except Exception as e:
        return f'<h1>Error Adding Port to VLAN</h1><p>{str(e)}</p>'

# ฟังก์ชันสำหรับแสดง VLANs ในหน้า conf_switch
@app.route('/show_vlans', methods=['POST'])
def show_vlans():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    try:
        vlan_ids = get_vlan_ids()
        hostname = get_hostname()
        interfaces = get_interfaces() 
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        # ส่งคำสั่ง 'show vlan brief' ไปยังอุปกรณ์
        output = net_connect.send_command('show vlan brief')
        prompt = net_connect.find_prompt()
        # ส่งผลลัพธ์ไปยังหน้า conf_switch.html และใช้ตัวแปร combined_output
        return render_template('conf_switch.html', output=output, prompt=prompt,hostname=hostname, interfaces=interfaces,vlan_ids=vlan_ids)
    except Exception as e:
        return f'<h1>Error Showing VLANs</h1><p>{str(e)}</p>'

# ฟังก์ชันสำหรับแสดง interfaces ในหน้า conf_switch
@app.route('/show_interfaces_switch', methods=['POST'])
def show_interfaces_switch():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    try:
        vlan_ids = get_vlan_ids()
        hostname = get_hostname()
        interfaces = get_interfaces() 
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        # ส่งคำสั่ง 'show interfaces' ไปยังอุปกรณ์
        output = net_connect.send_command('show ip interface brief')
        prompt = net_connect.find_prompt()
        # ส่งผลลัพธ์ไปยังหน้า conf_switch.html และใช้ตัวแปร combined_output
        return render_template('conf_switch.html', output=output, prompt=prompt,hostname=hostname, interfaces=interfaces, vlan_ids=vlan_ids)
    except Exception as e:
        return f'<h1>Error Showing Interfaces</h1><p>{str(e)}</p>'

@app.route('/show_interfaces_router', methods=['POST'])
def show_interfaces_router():
    global net_connect
    if not net_connect:
        return '<h1>Not connected</h1>'
    try:
        hostname = get_hostname()
        interfaces = get_interfaces() 
        print(f"Hostname: {hostname}")  # แสดง hostname ใน console
    except Exception as e:
        print(f"Error: {e}")  # แสดง error ถ้ามี
    try:
        # ส่งคำสั่ง 'show interfaces' ไปยังอุปกรณ์
        output = net_connect.send_command('show ip interface brief')
        prompt = net_connect.find_prompt()
        # ส่งผลลัพธ์ไปยังหน้า con_router.html และใช้ตัวแปร combined_output
        return render_template('conf_router.html', output=output, prompt=prompt,hostname=hostname, interfaces=interfaces)
    except Exception as e:
        return f'<h1>Error Showing Interfaces</h1><p>{str(e)}</p>'

def get_interfaces():
    global net_connect
    try:
        output = net_connect.send_command("show ip interface brief")
        lines = output.splitlines()
        interfaces = []
        for line in lines[1:]:  # ข้ามหัวข้อ
            parts = line.split()
            if len(parts) > 0:
                interface = parts[0]
                interfaces.append(interface)
        return interfaces
    except Exception as e:
        print(f"Error getting interfaces: {e}")
        return []

def get_vlan_ids():
    try:
        output = net_connect.send_command("show vlan brief")
        vlan_lines = output.splitlines()
        vlan_ids = []
        for line in vlan_lines:
            if line and "VLAN" not in line:  # ข้ามบรรทัดที่มีคำว่า "VLAN"
                parts = line.split()
                if len(parts) > 0:
                    vlan_ids.append(parts[0])  # แค่เก็บ VLAN ID
        return vlan_ids
    except Exception as e:
        print(f"Error retrieving VLAN IDs: {e}")
        return []

def validate_input(add_ip, delay):
    """Validate IP address and delay factor."""
    # Basic IP address validation (could be extended to use regex)
    if not add_ip or len(add_ip.split('.')) != 4:
        return False, "Invalid IP address format."
    
    # Validate delay factor
    try:
        delay = float(delay)
        if delay <= 0:
            return False, "Delay factor must be greater than 0."
    except ValueError:
        return False, "Invalid delay factor. Must be a number."
    
    return True, None


def get_router_details():
    """Retrieve the hostname or router prompt details."""
    try:
        hostname = get_hostname()  # Function to get hostname of router
        prompt = net_connect.find_prompt()  # Get router prompt
        return hostname, prompt, None
    except Exception as e:
        return None, None, str(e)  # Return error message if hostname fetching fails



#@app.route('/cli')
#def cli():
#    global net_connect
#    if not net_connect:
#        return redirect(url_for('index'))

#    prompt = net_connect.find_prompt()
#    return render_template('cli.html', output="", prompt=prompt)

if __name__ == '__main__':
    app.run(debug=True)
