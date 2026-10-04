import base64
import os
import shutil
import subprocess


_POWERSHELL_NOTIFICATION = r'''
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$notify = New-Object System.Windows.Forms.NotifyIcon
try {
    $notify.Icon = [System.Drawing.SystemIcons]::Information
    $notify.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
    $notify.BalloonTipTitle = $env:COMFY_NOTIFICATION_TITLE
    $notify.BalloonTipText = $env:COMFY_NOTIFICATION_DESCRIPTION
    $notify.Text = 'ComfyUI'
    $notify.Visible = $true
    $notify.ShowBalloonTip(5000)
    [System.Media.SystemSounds]::Asterisk.Play()
    Start-Sleep -Milliseconds 1500
}
catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}
finally {
    $notify.Visible = $false
    $notify.Dispose()
}
'''


class AnyType(str):
    def __ne__(self, other):
        return False


ANY_TYPE = AnyType("*")


class WindowsNotification:
    CATEGORY = "utils/notifications"
    FUNCTION = "notify"
    RETURN_TYPES = (ANY_TYPE,)
    RETURN_NAMES = ("value",)
    OUTPUT_NODE = True
    DESCRIPTION = "Show a Windows notification and play the system notification sound."

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "value": (ANY_TYPE,),
            "title": ("STRING", {"default": "ComfyUI", "multiline": False}),
            "description": ("STRING", {
                "default": "Seu workflow terminou.",
                "multiline": True,
            }),
        }}

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    def notify(self, value, title, description):
        if os.name != "nt":
            raise RuntimeError("ComfyUI Notifications funciona apenas no Windows.")

        powershell = shutil.which("powershell.exe")
        if powershell is None:
            raise RuntimeError("Não encontrei powershell.exe para exibir a notificação do Windows.")

        script = base64.b64encode(_POWERSHELL_NOTIFICATION.encode("utf-16le")).decode("ascii")
        env = os.environ.copy()
        env["COMFY_NOTIFICATION_TITLE"] = title
        env["COMFY_NOTIFICATION_DESCRIPTION"] = description
        try:
            result = subprocess.run(
                [powershell, "-NoLogo", "-NoProfile", "-NonInteractive", "-STA",
                 "-WindowStyle", "Hidden", "-EncodedCommand", script],
                env=env,
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("O Windows demorou demais para exibir a notificação.") from exc

        if result.returncode:
            details = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(f"Falha ao exibir a notificação do Windows: {details}")
        return (value,)


NODE_CLASS_MAPPINGS = {
    "ComfyUIWindowsNotification": WindowsNotification,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUIWindowsNotification": "Windows Notification",
}
