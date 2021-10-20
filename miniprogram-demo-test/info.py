import minium
mini = minium.Minium({
    "project_path": "/Users/yuanyuanhe/WeChatProjects",  # 小程序项目目录地址
    "dev_tool_path": "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"      # 开发者工具cli地址，如果没有修改过默认安装路径可不填此项
})
print(mini.get_system_info())