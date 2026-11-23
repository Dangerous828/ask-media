# 让任意 python 脚本脱离 SSH 会话运行（SSH 断开后不会被回收）。
# 用法：powershell -NoProfile -ExecutionPolicy Bypass -File launch_detached.ps1 -Script <py脚本> -Py <python路径> -WorkDir <工作目录> -Log <日志路径>
param([Parameter(Mandatory=$true)][string]$Script,
      [Parameter(Mandatory=$true)][string]$Py,
      [Parameter(Mandatory=$true)][string]$WorkDir,
      [Parameter(Mandatory=$true)][string]$Log)
# $Py = 渲染机上 ComfyUI 内嵌 python 的完整路径，由调用方传入，不内置默认值。
$py = $Py
$cmd = 'cmd.exe /c ""{0}" -u "{1}" >> "{2}" 2>&1"' -f $py, $Script, $Log
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $cmd; CurrentDirectory = $WorkDir }
"rc=$($r.ReturnValue) pid=$($r.ProcessId)"
