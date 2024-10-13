from flask import Blueprint, render_template
from flask_socketio import emit
from app import socketio  # นำเข้า socketio จาก app.py
import paramiko
import time

cli_blueprint = Blueprint('cli', __name__)

ssh_client = None  # เก็บ SSH session ที่เปิดอยู่
shell = None       # สำหรับ interactive shell

@cli_blueprint.route('/cli')
def cli():
    """แสดงหน้า CLI"""
    return render_template('cli.html')

@cli_blueprint.route('/connect', methods=['POST'])
def connect(ip, username, password):
    """ฟังก์ชันสำหรับเชื่อมต่อ SSH หลังจาก Login สำเร็จ"""
    global ssh_client, shell
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, username=username, password=password)

        # เปิด interactive shell
        shell = ssh_client.invoke_shell()
        return "Connected", 200
    except Exception as e:
        return f"<h1>Error Connecting to Device: {str(e)}</h1>"

@socketio.on('send_command')
def handle_command(data):
    """รับคำสั่งจากหน้าเว็บและส่งไปยังอุปกรณ์"""
    command = data['command'] + '\n'
    if shell:
        shell.send(command)  # ส่งคำสั่งไปยังอุปกรณ์

        # อ่านผลลัพธ์จากอุปกรณ์และส่งกลับไปยังหน้าเว็บ
        time.sleep(1)  # รอผลลัพธ์
        if shell.recv_ready():
            output = shell.recv(1024).decode('utf-8')
            emit('cli_output', {'output': output})  # ส่งผลลัพธ์ผ่าน WebSocket
