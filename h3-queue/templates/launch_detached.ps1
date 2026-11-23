# 让任意 python 脚本脱离 SSH 会话运行（SSH 断开后不会被回收）。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File launch_detached.ps1 -Script <py路径> -WorkDir <工作目录> -Log <日志路径>
param([Parameter(Mandatory=$true)][string]$Script,
      [Parameter(Mandatory=$true)][string]$WorkDir,
      [Parameter(Mandatory=$true)][string]$Log)
$py = 'E:\ComfyUI\ComfyUI_windows_portable\python_embeded\python.exe'
$cmd = 'cmd.exe /c ""{0}" -u "{1}" >> "{2}" 2>&1"' -f $py, $Script, $Log
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $cmd; CurrentDirectory = $WorkDir }
"rc=$($r.ReturnValue) pid=$($r.ProcessId)"
